# language: es
Característica: Listado completo de visitantes
  Para conocer quiénes han usado la aplicación y con qué frecuencia
  Como administrador
  Quiero ver un listado con totales y ordenado por última visita

  Antecedentes:
    Dado que la base de datos contiene visitantes:
      | name        | first_visit              | last_visit               | visit_count |
      | Ana Pérez   | 2025-10-28T09:10:00Z     | 2025-10-30T10:30:00Z     | 3           |
      | Luis Gómez  | 2025-10-27T08:00:00Z     | 2025-10-29T12:00:00Z     | 5           |
      | Carla Ríos  | 2025-10-26T07:30:00Z     | 2025-10-31T08:15:00Z     | 1           |

  @visitors @smoke
  Escenario: Ver listado ordenado y totales
    Cuando visito la ruta "/visitors"
    Entonces veo "Visitantes únicos: 3"
    Y veo "Total de visitas: 9"
    Y la primera fila de la tabla corresponde a "Carla Ríos"  # Última visita más reciente
