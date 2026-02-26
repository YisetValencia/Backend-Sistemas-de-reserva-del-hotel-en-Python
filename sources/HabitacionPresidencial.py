from sources.Habitacion import Habitacion


class HabitacionPresidencial(Habitacion):
    """
    Representa una habitación presidencial con servicio opcional
    de cine integrado.
    """

    def __init__(
        self,
        id,
        numero_habitacion,
        tipo_habitacion,
        precio=450000,
        servicio_cine_integrado: bool = False,
    ):
        super().__init__(id, numero_habitacion, tipo_habitacion, precio)
        self.servicio_cine_integrado = servicio_cine_integrado

    def calcular_costo(self, dias: int) -> float:
        """
        Calcula el costo del servicio adicional (cine integrado)
        y retorna el valor total

        """
        valor_servicio_cine = 300000

        if self.servicio_cine_integrado:
            return (self.precio * dias) + valor_servicio_cine

        return self.precio * dias
