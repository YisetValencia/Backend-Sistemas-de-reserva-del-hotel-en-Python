class Habitacion:
    """
    Representa una habitación dentro del sistema de reservas del hotel.

    Contiene información básica como identificador, número, tipo,
    precio por día y estado de disponibilidad.
    """

    def __init__(
        self, id: str, numero_habitacion: int, tipo_habitacion: str, precio: int
    ):
        """
        Inicializa una nueva habitación con sus datos principales.

        id: Identificador único de la habitación.
        numero_habitacion: Número asignado a la habitación.
        tipo_habitacion: Tipo de habitación (ej. estándar, premium, suite).
        precio: Precio por día de la habitación.

        """
        self.id = id
        self.numero = numero_habitacion
        self.tipo = tipo_habitacion
        self.precio = precio
        self.__disponible = True

    def esta_disponible(self) -> bool:
        """
        Indica si la habitación se encuentra disponible.

        return: True si está disponible, False en caso contrario.
        """
        return self.__disponible

    def ocupar(self) -> None:
        """
        Marca la habitación como ocupada.

        Si la habitación ya está ocupada, muestra un mensaje informativo.
        """
        if not self.__disponible:
            print(f"La habitación {self.numero} no está disponible.")
        self.__disponible = False

    def liberar(self) -> None:
        """
        Marca la habitación como disponible.

        Si la habitación ya está disponible, muestra un mensaje informativo.
        """
        if self.__disponible:
            print(f"La habitación {self.numero} ya está disponible.")
        self.__disponible = True

    def calcular_costo(self, dias: int) -> float:
        """
        Calcula el costo total de la estadía según la cantidad de días.

        dias: Número de días de hospedaje.
        return: Costo total de la estadía. Retorna 0 si los días son inválidos.
        """
        if dias <= 0:
            print("El número de días debe ser mayor que cero.")
            return 0
        return dias * self.precio

    def __str__(self) -> str:
        """
        Devuelve una representación en texto de la habitación..

        return: Cadena con la información principal y su disponibilidad.
        """
        disponibilidad = "Disponible" if self.__disponible else "Ocupada"
        return f"ID: {self.id} - Habitación {self.numero} - Tipo: {self.tipo} - Precio: ${self.precio:.2f} - {disponibilidad}"
