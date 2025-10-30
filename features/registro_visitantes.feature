# language: es
Característica: Registro automático de visitantes
  Para llevar control de quién usa la aplicación
  necesito que cada visita se registre en la base de datos.

  Antecedentes:
    Dado que la base de datos está vacía

  Escenario: Primera visita de un usuario nuevo
    Dado que visito la página principal
    Cuando envío el formulario con el nombre "Carlos Méndez"
    Entonces se crea un nuevo registro en la base de datos
    Y el registro tiene nombre "Carlos Méndez"
    Y el campo "visit_count" es 1
    Y los campos "first_visit" y "last_visit" tienen la fecha actual
    Y veo el mensaje "Hello Carlos Méndez"

  Escenario: Segunda visita del mismo usuario
    Dado que existe un visitante "Ana Torres" con 1 visita registrada hace "2 horas"
    Cuando envío el formulario con el nombre "Ana Torres"
    Entonces no se crea un registro nuevo
    Y el campo "visit_count" se incrementa a 2
    Y el campo "last_visit" se actualiza a la fecha actual
    Y el campo "first_visit" permanece sin cambios

  Escenario: Múltiples visitas del mismo usuario
    Dado que existe un visitante "Luis Gómez" con 5 visitas
    Cuando envío el formulario con el nombre "Luis Gómez"
    Entonces el campo "visit_count" se incrementa a 6
    Y el campo "last_visit" se actualiza a la fecha actual

  Escenario: Rechazar nombre vacío
    Dado que visito la página principal
    Cuando envío el formulario con el nombre ""
    Entonces no se registra ninguna visita en la base de datos
    Y soy redirigido a la página principal

  Escenario: Captura de dirección IP
    Dado que visito la página principal desde la IP "192.168.1.50"
    Cuando envío el formulario con el nombre "Pedro Ruiz"
    Entonces el registro almacena la IP "192.168.1.50"
