Feature: Ver estadísticas de visitantes
  Como administrador
  Quiero ver estadísticas resumidas y top de visitantes
  Para analizar el uso de la aplicación

  Scenario: Visualizar estadísticas cuando hay datos
    Given que existen visitantes registrados
    When visito la ruta "/stats"
    Then debería ver "Estadísticas Generales"
    And debería ver "Top 10 Visitantes"

  Scenario: Visualizar mensaje cuando no hay datos
    Given que no existen visitantes registrados
    When visito la ruta "/stats"
    Then debería ver "No hay datos de visitantes"
