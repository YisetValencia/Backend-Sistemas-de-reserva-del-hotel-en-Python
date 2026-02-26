from sources.Habitacion import Habitacion


class Reserva:
    """Representa una reserva de una habitación para un cliente."""

    def __init__(
        self,
        habitacion: Habitacion,
        cliente: str,
        documento: str,
        noches: int,
    ):
        """Crea una reserva y marca la habitación como ocupada."""
        self.habitacion = habitacion
        self.cliente = cliente
        self.documento = documento
        self.noches = noches
        self.habitacion.ocupar()

    def get_costo_total(self) -> float:
        """Retorna el costo total de la reserva."""
        return self.habitacion.calcular_costo(self.noches)

    def cancelar(self) -> None:
        """Cancela la reserva y libera la habitación."""
        self.habitacion.liberar()

    def __str__(self) -> str:
        """Devuelve una representación en texto de la reserva."""
        return (
            f"Reserva de {self.cliente} con documento {self.documento} en {self.habitacion}"
            f" por  {self.noches} noches"
            f" Costo total: ${self.get_costo_total()}"
        )
