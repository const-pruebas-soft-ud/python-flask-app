# language: es
Característica: Estadísticas y top de visitantes
  Como administrador de la aplicación
  Quiero ver estadísticas resumidas y los visitantes más frecuentes
  Para analizar el uso de la aplicación e identificar usuarios recurrentes

  @stats @smoke
  Escenario: Ver estadísticas generales y top 10 de visitantes
    Cuando visito la ruta "/stats"
    Entonces veo "📊 Estadísticas Generales"
    Y veo "🏅 Top 10 Visitantes"
    Y veo "Total visitantes únicos:"
    Y veo "Total visitas acumuladas:"
    Y veo "Promedio de visitas por usuario:"
    Y veo "Visitante con más visitas:"
    Y veo "Visitantes nuevos (últimas 24h):"
    Y veo "Visitas (últimas 24h):"
