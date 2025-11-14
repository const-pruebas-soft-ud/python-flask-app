import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from database import get_supabase_client

app = Flask(__name__)

# Cliente de Supabase
supabase = get_supabase_client()

# Contadores de visitas (en memoria, para compatibilidad)
visit_count = 0
greeting_count = 0


def register_visitor(name: str, ip_address: str = None) -> Optional[dict]:
    """
    Registra o actualiza un visitante en la base de datos
    
    Args:
        name: Nombre del visitante
        ip_address: Dirección IP del visitante (opcional)
    
    Returns:
        Optional[dict]: Datos del visitante registrado, o None si hubo error
    """
    try:
        # Buscar si el visitante ya existe
        response = supabase.table('visitors').select('*').eq('name', name).execute()
        
        if response.data and len(response.data) > 0:
            # El visitante ya existe, actualizar visit_count y last_visit
            visitor = response.data[0]
            updated_visitor = supabase.table('visitors').update({
                'visit_count': visitor['visit_count'] + 1,
                'last_visit': datetime.now().isoformat(),
                'ip_address': ip_address or visitor['ip_address']
            }).eq('id', visitor['id']).execute()
            
            print(f"✅ Visitante actualizado: {name} (visita #{visitor['visit_count'] + 1})")
            return updated_visitor.data[0] if updated_visitor.data else visitor
        else:
            # Nuevo visitante, crear registro
            new_visitor = supabase.table('visitors').insert({
                'name': name,
                'visit_count': 1,
                'first_visit': datetime.now().isoformat(),
                'last_visit': datetime.now().isoformat(),
                'ip_address': ip_address
            }).execute()
            
            print(f"✅ Nuevo visitante registrado: {name}")
            return new_visitor.data[0] if new_visitor.data else None
            
    except Exception as e:
        print(f"❌ Error al registrar visitante: {str(e)}")
        return None


@app.route('/')
def index():
   global visit_count
   visit_count += 1
   print('Request for index page received')
   return render_template('index.html', visits=visit_count)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   global greeting_count
   name = request.form.get('name')

   if name:
       # Obtener la IP del visitante
       ip_address = request.remote_addr
       
       # Registrar o actualizar visitante en la base de datos
       visitor = register_visitor(name, ip_address)
       
       # Incrementar contador en memoria (para compatibilidad)
       greeting_count += 1
       
       # Obtener datos del visitante desde la BD o usar valores por defecto
       visit_number = visitor['visit_count'] if visitor else greeting_count
       
       print(f'Request for hello page received with name={name}, visit #{visit_number}')
       
       return render_template('hello.html', 
                            name=name, 
                            greetings=greeting_count,
                            visit_number=visit_number,
                            visitor=visitor)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

# --- NUEVA RUTA: Reset counters ---
@app.post("/reset")
def reset_counters():
    global visit_count, greeting_count
    visit_count = 0
    greeting_count = 0
    # volvemos al home con un indicador para mostrar un mensaje en la UI
    return redirect(url_for("index", reset=1))

# --- NUEVA RUTA: Listado de visitantes ---
@app.get("/visitors")
def list_visitors():
    """
    Muestra:
      - Tabla con: nombre, primera visita, última visita, contador
      - Total de visitantes únicos
      - Total de visitas acumuladas
    Orden: última visita (desc, más reciente primero)
    Si no hay registros: mensaje informativo
    """
    try:
        # Traer campos necesarios y ordenar por last_visit DESC
        response = supabase.table('visitors') \
            .select('name, first_visit, last_visit, visit_count') \
            .order('last_visit', desc=True) \
            .execute()
        rows = response.data or []
    except Exception as e:
        # En caso de fallo de conexión, no romper la UI
        print(f"❌ Error consultando visitors: {e}")
        rows = []

    total_unique = len(rows)
    total_visits = sum(int(r.get('visit_count', 0) or 0) for r in rows)

    # Normalizar ISO 8601 → strings amigables (opcional)
    def fmt(dt_str):
        if not dt_str:
            return "-"
        # Evitar crash si viene con/ sin zona horaria
        try:
            return dt_str.replace('T', ' ').split('+')[0].split('Z')[0]
        except Exception:
            return dt_str

    for r in rows:
        r['first_visit_fmt'] = fmt(r.get('first_visit'))
        r['last_visit_fmt'] = fmt(r.get('last_visit'))

    return render_template(
        "visitors.html",
        visitors=rows,
        total_unique=total_unique,
        total_visits=total_visits
    )

@app.get("/stats")
def stats():
    """
    Muestra estadísticas generales y el top de visitantes.
    No falla si la tabla está vacía o no responde Supabase.
    """
    try:
        response = supabase.table('visitors').select('*').execute()
        visitors = response.data or []
    except Exception as e:
        print(f"❌ Error consultando estadísticas: {e}")
        visitors = []

    # --- Si no hay registros ---
    if not visitors:
        print("⚠️ No hay visitantes registrados aún.")
        return render_template("stats.html", empty=True)

    # --- Cálculos base ---
    total_usuarios = len(visitors)
    total_visitas = sum(int(v.get("visit_count", 0) or 0) for v in visitors)
    promedio_visitas = total_visitas / total_usuarios if total_usuarios else 0

    # --- Top 10 (evita crash si lista vacía) ---
    top_10 = sorted(visitors, key=lambda v: v.get("visit_count", 0), reverse=True)[:10]
    top_user = top_10[0] if top_10 else {"name": "N/A", "visit_count": 0}

    # --- Últimas 24h ---
    ahora = datetime.now(timezone.utc)
    hace_24h = ahora - timedelta(hours=24)

    def parse_iso(date_str):
        try:
            return datetime.fromisoformat(date_str.replace("Z", ""))
        except Exception:
            return None

    nuevos_24h = 0
    visitas_24h = 0
    for v in visitors:
        first_visit = parse_iso(v.get("first_visit", ""))
        last_visit = parse_iso(v.get("last_visit", ""))
        if first_visit and first_visit > hace_24h:
            nuevos_24h += 1
        if last_visit and last_visit > hace_24h:
            visitas_24h += 1

    # --- Armar datos para la plantilla ---
    stats_data = {
        "total_usuarios": total_usuarios,
        "total_visitas": total_visitas,
        "promedio_visitas": round(promedio_visitas, 2),
        "top_10": top_10,
        "top_user": top_user.get("name"),
        "nuevos_24h": nuevos_24h,
        "visitas_24h": visitas_24h
    }

    print("📊 Estadísticas generadas correctamente:", stats_data)
    return render_template("stats.html", stats=stats_data)



if __name__ == '__main__':
   app.run(port=80)
