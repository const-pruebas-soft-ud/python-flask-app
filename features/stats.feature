# language: es
Característica: Estadísticas y top de visitantes
  Para analizar el uso de la aplicación y conocer los visitantes más frecuentes
  Como administrador
  Quiero ver estadísticas generales y el top 10 de visitantes

  Antecedentes:
    Dado que la base de datos contiene visitantes:
      | name         | first_visit              | last_visit               | visit_count |
      | Ana Pérez    | 2025-10-28T09:10:00Z     | 2025-10-30T10:30:00Z     | 3           |
      | Luis Gómez   | 2025-10-27T08:00:00Z     | 2025-10-29T12:00:00Z     | 5           |
      | Carla Ríos   | 2025-10-26T07:30:00Z     | 2025-10-31T08:15:00Z     | 1           |

  @stats @smoke
  Escenario: Ver estadísticas generales y top de visitantes
    Cuando visito la ruta "/stats"
    Entonces veo "Estadísticas Generales"
    Y veo "Top 10 Visitantes"
    Y veo "Total visitantes únicos: 3"
    Y veo "Total visitas acumuladas: 9"
    Y veo "Visitante con más visitas: Luis Gómez"

  @stats
  Escenario: Ver mensaje cuando no hay datos
    Dado que no existen visitantes registrados
    Cuando visito la ruta "/stats"
    Entonces veo "No hay datos de visitantes"
