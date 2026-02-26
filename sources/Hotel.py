from sources.HabitacionEstandar import HabitacionEstandar
from sources.HabitacionPremium import HabitacionPremium
from sources.HabitacionPresidencial import HabitacionPresidencial
from sources.Reserva import Reserva
from sources.Habitacion import Habitacion


class Hotel:
    """
    Representa un hotel que gestiona habitaciones y reservas.

    El hotel contiene habitaciones de tipo estándar, presidencial
    y premium, además de una lista de reservas activas.
    """

    def __init__(self):
        """
        Inicializa el hotel creando las habitaciones disponibles
        y la lista de reservas vacía.
        """
        self.habitaciones = []
        for i in range(101, 200):
            self.habitaciones.append(HabitacionEstandar(str(i), i, "estandar"))

        for i in range(201, 300):
            self.habitaciones.append(HabitacionPremium(str(i), i, "premium"))

        for i in range(301, 400):
            self.habitaciones.append(HabitacionPresidencial(str(i), i, "presidencial"))
        self.reservas = []

    def reservar(
        self, cliente: str, documento: str, noches: int, tipo_habitacion
    ) -> Reserva | None:
        """
        Realiza una reserva si existe una habitación disponible
        del tipo solicitado.

        cliente: Nombre del cliente.
        documento: Documento de identificación del cliente.
        noches: Cantidad de noches de estadía.
        tipo_habitacion: Clase del tipo de habitación solicitada.
        return: Objeto Reserva si se realiza con éxito, de lo contrario None.
        """
        for habitacion in self.habitaciones:
            if isinstance(habitacion, tipo_habitacion) and habitacion.esta_disponible():
                reserva = Reserva(habitacion, cliente, documento, noches)
                self.reservas.append(reserva)
                print("Reserva realizada con éxito")
                return reserva

        print("No hay habitaciones disponibles de este tipo.")
        return None

    def cancelar_reserva(self, documento: str) -> None:
        """
        Cancela una reserva asociada al documento proporcionado.

        documento: Documento del cliente cuya reserva se desea cancelar.
        """
        for reserva in self.reservas:
            if reserva.documento == documento:
                reserva.cancelar()
                self.reservas.remove(reserva)
                print("Reserva cancelada correctamente.")
                return

        print("No se encontró una reserva con este documento.")

    def mostrar_reservas(self) -> None:
        """
        Muestra en consola todas las reservas activas del hotel.
        """
        if not self.reservas:
            print("No hay reservas activas.")
        else:
            for r in self.reservas:
                print(r)
