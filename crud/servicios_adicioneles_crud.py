from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.servicios_adicionales import Servicios_Adicionales
from datetime import date

class ServiciosAdicionalesCRUD:
    """
    Clase que implementa las operaciones CRUD para la entidad
    Servicios_Adicionales dentro del sistema del hotel.

    Permite registrar, consultar, actualizar y eliminar los
    servicios extra disponibles para los huéspedes, asegurando
    validaciones básicas como nombre válido, precio positivo
    y que no existan duplicados.
    """
    def __init__(self, db):
        self.db = db
    @staticmethod
    def crear_servicio(db: Session, servicio: Servicios_Adicionales):

        """
        Crea un nuevo servicio adicional en la base de datos.

        Verifica que el nombre no esté vacío, que el precio
        sea mayor a cero y que no exista otro servicio con
        el mismo nombre antes de guardarlo.
        """

        if not servicio.nombre_servicio or not servicio.nombre_servicio.strip():
            raise ValueError("El nombre del servicio no puede estar vacío")
        if servicio.precio <= 0:
            raise ValueError("El precio del servicio debe ser mayor a 0")
        
        existente = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.nombre_servicio == servicio.nombre_servicio).first()
        if existente:
            raise ValueError("El servicio adicional ya existe")

        db.add(servicio)
        db.commit()
        db.refresh(servicio)
        return servicio

    @staticmethod
    def obtener_servicio(db: Session, id_servicio: UUID):
        """
        Obtiene un servicio adicional específico a partir
        de su identificador único.

        Si no se encuentra el registro, se lanza un error.
        """
        servicio = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.id_servicio == id_servicio).first()
        if not servicio:
            raise ValueError("Servicio no encontrado")
        return servicio

    @staticmethod
    def obtener_servicios(db: Session):
        """
        Recupera la lista completa de servicios adicionales
        almacenados en la base de datos.
        """
        return db.query(Servicios_Adicionales).all()
    
    @staticmethod
    def actualizar_servicio(db, servicio: Servicios_Adicionales, id_usuario_edita: int, fecha_edita: date):
        """
        Actualiza la información de edición del servicio,
        registrando el usuario que realizó el cambio y
        la fecha correspondiente.
        """
        servicio.id_usuario_edita = id_usuario_edita
        servicio.fecha_edita = fecha_edita
        db.commit()
        db.refresh(servicio)
        return servicio

    @staticmethod
    def eliminar_servicio(db: Session, id_servicio: UUID) -> bool:
        """
        Elimina un servicio adicional de la base de datos
        usando su identificador.

        Devuelve True si la operación se realiza correctamente
        o genera un error si el servicio no existe.
        """
        servicio = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.id_servicio == id_servicio).first()
        if not servicio:
            raise ValueError("Servicio no encontrado")
        db.delete(servicio)
        db.commit()
        return True
