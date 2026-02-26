from sources.Habitacion import Habitacion


class HabitacionEstandar(Habitacion):
    """
    Representa una habitación de categoría estándar dentro del sistema.

    Esta clase hereda de la clase base Habitacion y proporciona una
    implementación específica para mostrar la información del inmueble.
    """

    def __init__(
        self,
        id,
        numero_habitacion,
        tipo_habitacion,
        precio=200000.0,
        servicio_television: bool = False,
    ):
        """
        Inicializa una nueva instancia de Habitacion_Estandar.

        Args:
            id (int/str): Identificador único de la habitación.
            numero_habitacion (int): El número asignado físicamente a la habitación.
            tipo_habitacion (str): El tipo de habitación (por ejemplo, "Individual", "Doble").
            precio (float): El costo por noche de la habitación.
        """
        super().__init__(id, numero_habitacion, tipo_habitacion, precio)
        self.servicio_television = servicio_television

    def calcular_costos(self, noches: int) -> float:
        """Calcula el precio total de la habitación estándar, incluyendo el servicio de televisión si está habilitado."""

        valor_servicio_television = 20000
        if self.servicio_television:
            return (self.precio * noches) + valor_servicio_television
        return self.precio * noches
