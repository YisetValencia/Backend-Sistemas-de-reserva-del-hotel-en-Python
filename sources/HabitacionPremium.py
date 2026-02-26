from sources.Habitacion import Habitacion

""" Importamos la clase Habitacion desde el módulo Habitacion para que la clase HabitacionPremium pueda heredar de ella. """


class HabitacionPremium(Habitacion):
    def __init__(
        self,
        id,
        numero_habitacion,
        tipo_habitacion,
        precio=300000,
        servicio_yacuzzi: bool = False,
    ):
        super().__init__(id, numero_habitacion, tipo_habitacion, precio)
        self.servicio_yacuzzi = servicio_yacuzzi

    """ El método _init_ de la clase HabitacionPremium llama al método _init_ de la clase base Habitacion para inicializar los atributos heredados, y luego inicializa el atributo servicio_yacuzzi para indicar si el servicio de jacuzzi está habilitado. """

    def calcular_costo(self, noches) -> float:

        valor_jacuzzi = 50000
        """Calcula el precio total de la habitación premium, incluyendo el servicio de jacuzzi si está habilitado."""
        if self.servicio_yacuzzi:
            return self.precio * noches + valor_jacuzzi
        return self.precio * noches

    """ La  clase HabitacionPremium hereda de la clase Habitacion y agrega un atributo adicional para indicar si el servicio de jacuzzi está habilitado. Además, incluye un método para calcular el precio total de la habitación premium, sumando el costo del servicio de jacuzzi si está habilitado. """
