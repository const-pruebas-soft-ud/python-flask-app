import os
from datetime import datetime

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from database import get_supabase_client

app = Flask(__name__)

# Cliente de Supabase
supabase = get_supabase_client()

# Contadores de visitas (en memoria, para compatibilidad)
visit_count = 0
greeting_count = 0


def register_visitor(name: str, ip_address: str = None) -> dict:
    """
    Registra o actualiza un visitante en la base de datos
    
    Args:
        name: Nombre del visitante
        ip_address: Dirección IP del visitante (opcional)
    
    Returns:
        dict: Datos del visitante registrado
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

if __name__ == '__main__':
   app.run(port=80)
