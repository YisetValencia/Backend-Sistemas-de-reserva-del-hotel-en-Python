from database.config import SessionLocal, create_tables
from crud.reserva_crud import ReservaCRUD
from crud.tipo_habitacion_crud import TipoHabitacionCRUD
from crud.usuario_crud import UsuarioCRUD
from crud.habitacion_crud import HabitacionCRUD
from crud.servicios_adicioneles_crud import ServiciosAdicionalesCRUD
from entities.servicios_adicionales import Servicios_Adicionales
from entities.reserva_servicios import Reserva_Servicios
from entities.usuario import Usuario
from entities.reserva import Reserva
from entities.habitacion import Habitacion
import getpass
from typing import Optional
from datetime import date, timedelta, datetime


class SistemaGestion:
    def __init__(self):
        """Inicializa el sistema de gestión estableciendo la conexión con la base
        de datos y creando las instancias necesarias para realizar las
        operaciones CRUD de cada módulo del sistema."""
        self.db = SessionLocal()
        self.usuario_crud = UsuarioCRUD(self.db)
        self.habitacion_crud = HabitacionCRUD(self.db)
        self.reserva_crud = ReservaCRUD(self.db)
        self.servicios_adicionales_crud = ServiciosAdicionalesCRUD(self.db)
        self.tipo_habitacion_crud = TipoHabitacionCRUD(self.db)
        self.usuario_actual: Optional[Usuario] = None

    def __enter__(self):
        """Permite utilizar la clase dentro de un bloque with, retornando la instancia
        actual del sistema para que pueda ejecutarse de forma controlada.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Se ejecuta al salir del bloque with. Cierra correctamente la conexión con
        la base de datos para liberar recursos y evitar errores de conexión."""
        self.db.close()

    def mostrar_pantalla_login(self) -> bool:
        """Muestra la interfaz de inicio de sesión y solicita las credenciales del
        usuario. Verifica que el nombre y la contraseña sean válidos y permite un
        máximo de intentos antes de denegar el acceso."""
        print("\n" + "=" * 50)
        print("        SISTEMA DE GESTIÓN DEL HOTEL")
        print("=" * 50)
        print("INICIAR SESIÓN")
        print("=" * 50)

        intentos = 0
        max_intentos = 3
        while intentos < max_intentos:
            try:
                print(f"\nIntento {intentos + 1} de {max_intentos}")
                nombre_usuario = input("Nombre de usuario: ").strip()
                if not nombre_usuario:
                    print("ERROR: El nombre de usuario es obligatorio")
                    intentos += 1
                    continue
                contrasena = getpass.getpass("Contraseña: ")
                if not contrasena:
                    print("ERROR: La contraseña es obligatoria")
                    intentos += 1
                    continue
                usuario = self.usuario_crud.autenticar_usuario(
                    nombre_usuario, contrasena
                )
                if usuario:
                    self.usuario_actual = usuario
                    print(f"\nÉXITO: ¡Bienvenido, {usuario.nombre}!")
                    if usuario.tipo_usuario == "Administrador":
                        print("INFO: Tienes privilegios de administrador")
                    return True
                else:
                    print("ERROR: Credenciales incorrectas o usuario inactivo")
                    intentos += 1
            except KeyboardInterrupt:
                print("\n\nINFO: Operación cancelada por el usuario")
                return False
            except Exception as e:
                print(f"ERROR: Error durante el login: {e}")
                intentos += 1
        print(
            f"\nERROR: Máximo de intentos ({max_intentos}) excedido. Acceso denegado."
        )
        return False

    def mostrar_menu_principal_autenticado(self) -> None:
        """Despliega el menú principal adaptado al rol del usuario autenticado.
        Dependiendo de si es administrador o cliente, presenta diferentes opciones
        de gestión y dirige la ejecución hacia las funciones correspondientes."""
        if not self.usuario_actual:
            return
        print("\n" + "=" * 50)
        print("    SISTEMA DE GESTIÓN DEL HOTEL")
        print("=" * 50)
        print(f"Usuario: {self.usuario_actual.nombre} {self.usuario_actual.apellidos}")
        print(f"Rol: {self.usuario_actual.tipo_usuario}")
        print("=" * 50)

        if self.usuario_actual.tipo_usuario == "Administrador":
            print("1. Gestión de Usuarios")
            print("2. Gestión de Habitaciones")
            print("3. Gestión de Reservas")
            print("4. Gestión de Servicios Adicionales")
            print("5. Mi Perfil")
            print("6. Actualizar perfil")
            print("7 Cerrar Sesión")
            while True:
                opcion = input("Elige una opción (1-7): ")
                if opcion.isdigit():
                    opcion = int(opcion)
                    if 1 <= opcion <= 7:
                        print("Opción válida:", opcion)
                        break
                    else:
                        print("El número debe estar entre 1 y 7.")
                else:
                    print("Debes ingresar un número válido.")
            if opcion == 1:
                self.mostrar_menu_usuarios()
            elif opcion == 2:
                self.mostrar_menu_habitaciones()
            elif opcion == 3:
                self.mostrar_menu_reservas()
            elif opcion == 4:
                self.mostrar_menu_servicios()
            elif opcion == 5:
                self.mostrar_perfil()
            elif opcion == 6:
                self.actualizar_perfil()
            elif opcion == 7:
                print("\n¡Hasta luego!")
                self.usuario_actual = None
                return
        elif self.usuario_actual.tipo_usuario == "Cliente":
            print("1. Reservar Habitación")
            print("2. Mostrar Mis Reservas")
            print("3. Cancelar Reserva")
            print("4. Mi Perfil")
            print("5. Actualizar perfil")
            print("6. Cerrar Sesión")
            while True:
                opcion = input("Elige una opción (1-6): ")
                if opcion.isdigit():
                    opcion = int(opcion)
                    if 1 <= opcion <= 6:
                        print("Opción válida:", opcion)
                        break
                    else:
                        print("El número debe estar entre 1 y 6.")
                else:
                    print("Debes ingresar un número válido.")
            if opcion == 1:
                self.reservar_habitacion()
            elif opcion == 2:
                self.mostrar_reservas()
            elif opcion == 3:
                self.cancelar_reserva()
            elif opcion == 4:
                self.mostrar_perfil()
            elif opcion == 5:
                self.actualizar_perfil()
            elif opcion == 6:
                print("\n¡Hasta luego!")
                self.usuario_actual = None
                return
            else:
                print("Opción inválida.")
        else:
            print("ERROR: Rol no reconocido. Contacte al administrador.")
        print("=" * 50)

    def reservar_habitacion(self):
        """
        Permite a un cliente autenticado reservar una habitación dentro del sistema.
        El proceso guía al usuario solicitando la duración de la estancia, número de
        huéspedes, tipo de habitación y fecha de ingreso. Con estos datos se calcula
        el costo total y se muestra un resumen antes de solicitar confirmación.

        Si el usuario confirma, la reserva se almacena en la base de datos, la
        habitación seleccionada se marca como no disponible y se ofrece la posibilidad
        de añadir servicios adicionales a la reserva.

        Requisitos:
        - El usuario debe haber iniciado sesión como cliente.
        - Deben existir habitaciones disponibles del tipo seleccionado.

        Entradas solicitadas:
        - Número de noches y personas.
        - Tipo de habitación.
        - Fecha de entrada válida.
        - Confirmación de la reserva y opción de servicios extra.

        Resultados:
        - Creación de una nueva reserva.
        - Actualización de la disponibilidad de la habitación.
        - Posible asociación de servicios adicionales.
        """
        if not self.usuario_actual:
            print("Debes iniciar sesión como cliente para reservar.")
            return

        while True:
            noches = input("Número de noches: ")
            if noches.isdigit():
                noches = int(noches)
                if noches > 0:
                    break
                else:
                    print("Debe ser mayor a cero.")
            else:
                print("Debes ingresar un número válido.")
        while True:
            numero_de_personas = input("Número de personas: ")
            if numero_de_personas.isdigit():
                numero_de_personas = int(numero_de_personas)
                if numero_de_personas > 0:
                    break
                else:
                    print("Debe ser mayor a cero.")
            else:
                print("Debes ingresar un número válido.")
        tipos_disponibles = self.tipo_habitacion_crud.obtener_tipos_habitacion(self.db)
        print("Tipos de habitación disponibles:")
        for idx, t in enumerate(tipos_disponibles, start=1):
            print(f"{idx}. {t.nombre_tipo} | {t.descripcion}")
        while True:
            tipo_input = input(
                f"Selecciona el tipo de habitación (1-{len(tipos_disponibles)}): "
            )
            if tipo_input.isdigit():
                tipo_input = int(tipo_input)
                if 1 <= tipo_input <= len(tipos_disponibles):
                    break
                print(f"Debes seleccionar entre 1 y {len(tipos_disponibles)}.")
            else:
                print("Debes ingresar un número válido.")
        tipo_seleccionado = tipos_disponibles[tipo_input - 1]
        nombre_tipo = tipo_seleccionado.nombre_tipo
        habitacion = (
            self.db.query(Habitacion)
            .filter_by(tipo=nombre_tipo, disponible=True)
            .first()
        )
        if not habitacion:
            print("No hay habitaciones disponibles de ese tipo.")
            return
        precio_noche = habitacion.precio
        total = precio_noche * noches
        while True:
            fecha_entrada_str = input(
                "Ingrese la fecha de entrada (AAAA-MM-DD): "
            ).strip()
            try:
                fecha_entrada = datetime.strptime(fecha_entrada_str, "%Y-%m-%d").date()
                if fecha_entrada < date.today():
                    print("La fecha de entrada no puede ser anterior a hoy.")
                else:
                    break
            except ValueError:
                print("Formato inválido. Usa AAAA-MM-DD.")
        fecha_salida = fecha_entrada + timedelta(days=noches)
        fecha_creacion = datetime.now()
        print(f"\nFecha entrada: {fecha_entrada}")
        print(f"Fecha salida: {fecha_salida}")
        print(f"Total: {noches} noches x ${precio_noche:,} = ${total:,}")
        while True:
            confirmar = input("¿Desea confirmar la reserva? (1. Sí / 2. No): ")
            if confirmar.isdigit():
                confirmar = int(confirmar)
                if confirmar in (1, 2):
                    break
                else:
                    print("Opción inválida. Debe ser 1 o 2.")
            else:
                print("Debes ingresar un número válido.")
        if confirmar == 2:
            print("Reserva cancelada")
            return
        id_habitacion = habitacion.id_habitacion
        reserva = Reserva(
            id_usuario=self.usuario_actual.id_usuario,
            id_habitacion=id_habitacion,
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            estado_reserva="Activa",
            numero_de_personas=numero_de_personas,
            noches=noches,
            costo_total=total,
            id_usuario_crea=self.usuario_actual.id_usuario,
            fecha_creacion=fecha_creacion,
        )
        self.reserva_crud.crear_reserva(self.db, reserva)
        habitacion.disponible = False
        self.db.commit()
        print(
            f"\nReserva creada para {self.usuario_actual.nombre} {self.usuario_actual.apellidos}"
        )
        print(f"Habitación {habitacion.numero} - Total: ${total:,}")
        print(f"Del {fecha_entrada} al {fecha_salida}")
        while True:
            opcion_servicio = input(
                "¿Deseas servicios adicionales? (1. Sí / 2. No): "
            ).strip()
            if not opcion_servicio.isdigit():
                print("Debes ingresar un número válido (1 o 2).")
                continue
            opcion_servicio = int(opcion_servicio)
            if opcion_servicio == 1:
                print("Agregando servicios adicionales...")
                self.reservar_servicios()
                break
            elif opcion_servicio == 2:
                print("No se agregaron servicios adicionales.")
                break
            else:
                print("Opción inválida. Solo puedes elegir 1 o 2.")

    def cancelar_reserva(self):
        """
        Permite al usuario autenticado cancelar una de sus reservas activas.
        El método muestra las reservas vigentes asociadas al usuario y le permite
        seleccionar cuál desea cancelar. Antes de realizar la operación, se solicita
        confirmación para evitar cancelaciones accidentales.

        Si el usuario confirma, el estado de la reserva se actualiza a "Cancelada",
        la habitación vuelve a quedar disponible y se registra la información de la
        modificación realizada.

        Entradas:
        - Selección de la reserva a cancelar.
        - Confirmación de la acción.

        Resultados:
        - Actualización del estado de la reserva.
        - Liberación de la habitación asociada.
        - Mensajes informativos sobre el resultado del proceso.
        """
        reservas = (
            self.db.query(Reserva)
            .filter_by(
                id_usuario=self.usuario_actual.id_usuario, estado_reserva="Activa"
            )
            .all()
        )
        if not reservas:
            print("No tienes reservas activas.")
            return
        print("Tus reservas activas:")
        for i, reserva in enumerate(reservas, 1):
            habitacion = (
                self.db.query(Habitacion)
                .filter_by(id_habitacion=reserva.id_habitacion)
                .first()
            )
            if habitacion:
                print(
                    f"{i}. Habitación {habitacion.numero} del {reserva.fecha_entrada} al {reserva.fecha_salida} - Total: ${reserva.costo_total:,.0f}"
                )
            else:
                print(
                    f"{i}. Habitación no encontrada para la reserva del {reserva.fecha_entrada} al {reserva.fecha_salida}"
                )
        opcion = input("Selecciona el número de la reserva que deseas cancelar: ")
        try:
            opcion = int(opcion)
            if opcion < 1 or opcion > len(reservas):
                print("Opción inválida.")
                return
        except ValueError:
            print("Debes ingresar un número.")
            return
        reserva = reservas[opcion - 1]
        while True:
            confirmar = input("¿Desea confirmar la reserva? (1. Sí / 2. No): ")
            if confirmar.isdigit():
                confirmar = int(confirmar)
                if confirmar in (1, 2):
                    break
                else:
                    print("Opción inválida. Debe ser 1 o 2.")
            else:
                print("Debes ingresar un número válido.")
        if confirmar == 1:
            habitacion = self.db.get(Habitacion, reserva.id_habitacion)
            if habitacion:
                habitacion.disponible = True
            reserva.estado_reserva = "Cancelada"
            reserva.fecha_edicion = datetime.now()
            reserva.id_usuario_edita = self.usuario_actual.id_usuario
            self.db.commit()
            print("Reserva cancelada con éxito.")
        else:
            print("Cancelación abortada.")

    def mostrar_reservas(self):
        """
        Permite al usuario visualizar todas las reservas asociadas a su cuenta.
        El método consulta la base de datos para recuperar los registros creados
        por el usuario autenticado. Si no se encuentran reservas, se muestra un
        mensaje indicándolo; de lo contrario, se presenta un listado con la
        información principal de cada reserva, como la habitación asignada,
        duración de la estancia y su estado actual.
        """
        reservas = (
            self.db.query(Reserva)
            .filter_by(id_usuario=self.usuario_actual.id_usuario)
            .all()
        )
        if not reservas:
            print("No tienes reservas registradas.")
            return
        print("\nTus reservas:")
        for r in reservas:
            habitacion = self.db.get(Habitacion, r.id_habitacion)
            numero = habitacion.numero if habitacion else "N/A"
            print(
                f"Habitación {numero} - {r.noches} noches - Estado: {r.estado_reserva} - Del {r.fecha_entrada} al {r.fecha_salida}"
            )

    def reservar_servicios(self):
        """
        Permite al usuario añadir servicios adicionales a una de sus reservas activas.
        El método primero muestra las reservas vigentes del usuario y solicita que
        seleccione una. Luego presenta el listado de servicios disponibles para que
        pueda elegir uno o varios. Los servicios seleccionados se asocian a la reserva
        y el costo total se actualiza en consecuencia.

        Durante el proceso se validan las entradas del usuario y se gestionan posibles
        errores. En caso de presentarse una excepción, la operación se revierte para
        mantener la integridad de la información.

        Excepciones:
        - Puede generar un error si ocurre algún problema al registrar los servicios
        en la reserva.
        """
        reservas = (
            self.db.query(Reserva)
            .filter_by(id_usuario=self.usuario_actual.id_usuario)
            .all()
        )
        if not reservas:
            print("No tienes reservas activas.")
            return
        print("\nTus reservas activas:")
        for i, r in enumerate(reservas, start=1):
            habitacion = self.db.get(Habitacion, r.id_habitacion)
            print(
                f"{i}. Habitación {habitacion.numero if habitacion else 'N/A'} del {r.fecha_entrada} al {r.fecha_salida}"
            )
        idx = int(input("Selecciona la reserva a la que agregar servicios: ")) - 1
        reserva_seleccionada = reservas[idx]
        servicios = self.db.query(Servicios_Adicionales).all()
        if not servicios:
            print("No hay servicios adicionales disponibles.")
            return
        print("\nServicios disponibles:")
        for i, s in enumerate(servicios, start=1):
            print(f"{i}. {s.nombre_servicio} - ${s.precio:,.0f} - {s.descripcion}")
        seleccion = input("Selecciona los servicios separados por coma (ej: 1,3): ")
        seleccion_indices = [
            int(x.strip()) - 1 for x in seleccion.split(",") if x.strip().isdigit()
        ]
        try:
            for i in seleccion_indices:
                servicio = servicios[i]
                subtotal = servicio.precio
                reserva_servicio = Reserva_Servicios(
                    id_reserva=reserva_seleccionada.id_reserva,
                    id_servicio=servicio.id_servicio,
                )
                self.db.add(reserva_servicio)
                reserva_seleccionada.costo_total = (
                    reserva_seleccionada.costo_total or 0
                ) + subtotal
            self.db.commit()
            print("Servicios agregados correctamente a tu reserva.")
        except Exception as e:
            self.db.rollback()
            print(f"Error al agregar servicios: {e}")

    def ejecutar(self) -> None:
        """
        Inicia la ejecución del sistema principal, gestionando el proceso de
        autenticación del usuario antes de permitir el acceso a las funciones
        disponibles dentro de la aplicación.
        """
        try:
            print("Iniciando Sistema de Gestión del Hotel...")
            print("Configurando base de datos...")
            create_tables()
            print("Sistema listo para usar.")
            while True:
                if not self.usuario_actual:
                    if not self.mostrar_pantalla_login():
                        break
                self.mostrar_menu_principal_autenticado()
        except KeyboardInterrupt:
            print("\n\nSistema interrumpido por el usuario.")
        except Exception as e:
            print(f"\nError crítico: {e}")
        finally:
            self.db.close()

    def mostrar_menu_habitaciones(self) -> None:
        """
        Presenta el menú de administración de habitaciones y procesa la opción
        seleccionada por el usuario. Desde este menú se pueden realizar acciones
        como registrar nuevas habitaciones, consultar las existentes, modificar
        su información o eliminarlas, además de regresar al menú principal.

        El método valida que la opción ingresada sea correcta y ejecuta la
        función correspondiente según la elección realizada.
        """
        print("\n--- GESTIÓN DE HABITACIONES ---")
        print("1. Agregar habitación")
        print("2. Listar habitaciones")
        print("3. Actualizar habitación")
        print("4. Eliminar habitación")
        print("5. Volver al menú principal")
        while True:
            opcion = input("Elige una opción (1-5): ")
            if opcion.isdigit():
                opcion = int(opcion)
                if 1 <= opcion <= 5:
                    print("Opción válida:", opcion)
                    break
                else:
                    print("El número debe estar entre 1 y 4.")
            else:
                print("Debes ingresar un número válido.")
        if opcion == 1:
            self.agregar_habitacion()
        elif opcion == 2:
            self.listar_habitaciones()
        elif opcion == 3:
            self.actualizar_habitacion()
        elif opcion == 4:
            self.eliminar_habitacion()
        elif opcion == 5:
            print("Volviendo al menu principal...")
            self.mostrar_menu_principal_autenticado()

    def mostrar_menu_reservas(self) -> None:
        """
        Despliega el menú de administración de reservas y permite al usuario
        seleccionar la acción que desea realizar. El método solicita una opción,
        verifica que sea válida y ejecuta la funcionalidad correspondiente,
        como consultar, gestionar o eliminar reservas según la elección.
        """
        print("\n--- GESTIÓN DE RESERVAS ---")
        print("1. Listar reservas")
        print("2. Consultar reservas activas")
        print("3. Eliminar reserva")
        print("4. Volver al menú principal")
        while True:
            opcion = input("Elige una opción (1-4): ")
            if opcion.isdigit():
                opcion = int(opcion)
                if 1 <= opcion <= 4:
                    print("Opción válida:", opcion)
                    break
                else:
                    print("El número debe estar entre 1 y 4.")
            else:
                print("Debes ingresar un número válido.")
        if opcion == 1:
            self.listar_reservas()
        elif opcion == 2:
            self.listar_reservas_activas()
        elif opcion == 3:
            self.eliminar_reserva()
        elif opcion == 4:
            print("Volviendo al menu principal...")
            self.mostrar_menu_principal_autenticado()

    def mostrar_menu_servicios(self) -> None:
        """
        Presenta el menú de administración de servicios adicionales y procesa
        la opción seleccionada por el usuario. Desde este menú es posible crear,
        consultar, modificar o eliminar servicios, además de regresar al menú
        principal del sistema.

        El método valida la entrada para asegurar que corresponda a una opción
        válida y ejecuta la acción asociada según la elección realizada.
        """
        print("\n--- GESTIÓN DE SERVICIOS ADICIONALES ---")
        print("1. Agregar servicio")
        print("2. Listar servicios")
        print("3. Actualizar servicio")
        print("4. Eliminar servicio")
        print("5. Volver al menú principal")
        while True:
            opcion = input("Elige una opción (1-5): ")
            if opcion.isdigit():
                opcion = int(opcion)
                if 1 <= opcion <= 5:
                    print("Opción válida:", opcion)
                    break
                else:
                    print("El número debe estar entre 1 y 4.")
            else:
                print("Debes ingresar un número válido.")
        if opcion == 1:
            self.agregar_servicio()
        elif opcion == 2:
            self.listar_servicios()
        elif opcion == 3:
            self.actualizar_servicio()
        elif opcion == 4:
            self.eliminar_servicio()
        elif opcion == 5:
            print("Volviendo al menu principal...")
            self.mostrar_menu_principal_autenticado()

    def mostrar_menu_usuarios(self) -> None:
        """
        Despliega el menú de administración de usuarios y permite seleccionar
        la acción a realizar. El método solicita una opción dentro del rango
        disponible, valida que sea correcta y ejecuta la funcionalidad asociada,
        como crear, consultar o eliminar usuarios.

        Si la entrada no corresponde a una opción válida, se solicita nuevamente
        hasta que el usuario ingrese un valor correcto.
        """
        print("\n--- GESTIÓN DE USUARIOS ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Eliminar usuario")
        print("4. Volver al menú principal")
        while True:
            opcion = input("Elige una opción (1-5): ")
            if opcion.isdigit():
                opcion = int(opcion)
                if 1 <= opcion <= 5:
                    print("Opción válida:", opcion)
                    break
                else:
                    print("El número debe estar entre 1 y 5.")
            else:
                print("Debes ingresar un número válido.")
        if opcion == 1:
            self.crear_usuario()
        elif opcion == 2:
            self.listar_usuarios()
        elif opcion == 3:
            self.eliminar_usuario()
        elif opcion == 4:
            print("Volviendo al menú principal...")
            self.mostrar_menu_principal_autenticado()

    def mostrar_perfil(self):
        """
        Muestra los datos principales del usuario que ha iniciado sesión.
        El método imprime en consola la información básica del perfil,
        incluyendo su nombre completo, el identificador o teléfono utilizado
        como usuario y el rol que posee dentro del sistema.
        """
        print("\n--- MI PERFIL ---")
        print(f"Nombre: {self.usuario_actual.nombre} {self.usuario_actual.apellidos}")
        print(f"Usuario: {self.usuario_actual.telefono}")
        print(f"Rol: {self.usuario_actual.tipo_usuario}")

    def agregar_habitacion(self):
        """
        Permite registrar una nueva habitación en el sistema a partir de la
        información ingresada por el usuario. El método muestra los tipos de
        habitación disponibles, solicita seleccionar uno y asigna automáticamente
        un número de habitación libre dentro del rango correspondiente.

        Posteriormente, pide el precio por noche y crea el registro en la base
        de datos con los datos proporcionados. Al finalizar, informa si la
        operación se realizó correctamente o si ocurrió algún problema durante
        el proceso, manejando posibles errores de entrada o fallos inesperados.
        """
        try:
            rangos = {
                "Estándar": range(101, 200),
                "Suite": range(201, 300),
                "Premium": range(301, 400),
            }
            tipos_disponibles = self.tipo_habitacion_crud.obtener_tipos_habitacion(
                self.db
            )
            print("Tipos de habitación disponibles:")
            for i, t in enumerate(tipos_disponibles, start=1):
                print(f"{i}. {t.nombre_tipo}")
            while True:
                opcion = input("Elige el número del tipo de habitación: ").strip()
                if opcion.isdigit():
                    opcion = int(opcion)
                    if 1 <= opcion <= len(tipos_disponibles):
                        tipo = tipos_disponibles[opcion - 1]
                        break
                    else:
                        print("Número inválido. Debe estar en el rango mostrado.")
                else:
                    print("Debes ingresar un número válido.")
            fecha_creacion = datetime.now()
            habitaciones_existentes = [
                h.numero for h in self.habitacion_crud.obtener_habitaciones(self.db)
            ]
            numero_asignado = next(
                (
                    n
                    for n in rangos[tipo.nombre_tipo]
                    if n not in habitaciones_existentes
                ),
                None,
            )
            if not numero_asignado:
                print(
                    f"No hay más habitaciones disponibles en el rango de {tipo.nombre_tipo}."
                )
                return
            while True:
                try:
                    precio = float(input("Precio por noche: "))
                    break
                except ValueError:
                    print("Debes ingresar un número válido para el precio.")
            nueva_habitacion = Habitacion(
                numero=numero_asignado,
                id_tipo=tipo.id_tipo,
                tipo=tipo.nombre_tipo,
                precio=precio,
                disponible=True,
                id_usuario_crea=self.usuario_actual.id_usuario,
                fecha_creacion=fecha_creacion,
            )
            self.habitacion_crud.crear_habitacion(self.db, nueva_habitacion)
            print(
                f"Habitación {numero_asignado} ({tipo.nombre_tipo}) agregada exitosamente."
            )
        except Exception as e:
            print(f"Error al agregar habitación: {e}")

    def listar_habitaciones(self):
        """
        Muestra en consola el listado completo de habitaciones registradas en
        el sistema. El método obtiene los datos desde la base de datos mediante
        el módulo correspondiente y presenta la información principal de cada
        habitación, como su identificador, número, tipo, precio, estado de
        disponibilidad y datos de creación o edición.

        Si no existen registros, se informa al usuario. También se gestionan
        posibles errores durante la consulta, mostrando un mensaje adecuado en
        caso de que ocurra alguna excepción.
        """
        try:
            habitaciones = self.habitacion_crud.obtener_habitaciones(self.db)
            if not habitaciones:
                print("No hay habitaciones registradas.")
            else:
                for h in habitaciones:
                    print(
                        f"""
                    ============================
                    ID: {h.id_habitacion}
                    Número: {h.numero}
                    Tipo: {h.tipo} (ID tipo: {h.id_tipo})
                    Precio: ${h.precio}
                    Disponible: {"Sí" if h.disponible else "No"}
                    Usuario Creador: {h.id_usuario_crea}
                    Usuario Editor: {h.id_usuario_edita}
                    Fecha Creación: {h.fecha_creacion}
                    Fecha Edición: {h.fecha_edicion}
                    ============================
                    """
                    )
        except Exception as e:
            print(f"Error al listar habitaciones: {e}")

    def actualizar_habitacion(self):
        """
        Permite modificar el precio por noche de una habitación existente.
        El método muestra las habitaciones disponibles, solicita al usuario
        seleccionar una y registrar el nuevo valor. Al realizar el cambio,
        se actualizan también los datos de edición, como la fecha y el usuario
        responsable de la modificación.

        Si ocurre algún problema durante la actualización, se informa el error
        y se revierte la operación para mantener la consistencia de la base
        de datos.
        """
        try:
            habitaciones = self.habitacion_crud.obtener_habitaciones(self.db)
            if not habitaciones:
                print("No hay habitaciones registradas.")
                return
            for i, u in enumerate(habitaciones, start=1):
                print(f"{i}. {u.numero} | ({u.tipo}) | ({u.precio})")
            opcion = input("Elige el número de la habitación a actualizar: ").strip()
            if (
                not opcion.isdigit()
                or int(opcion) < 1
                or int(opcion) > len(habitaciones)
            ):
                print("Opción inválida.")
                return
            habitacion_a_actualizar = habitaciones[int(opcion) - 1]
            nuevo_precio = float(
                input(f"Nuevo precio (actual: {habitacion_a_actualizar.precio}): ")
            )
            fecha_edicion = (datetime.now(),)
            self.habitacion_crud.actualizar_habitacion(
                self.db,
                id_habitacion=habitacion_a_actualizar.id_habitacion,
                id_usuario_edita=self.usuario_actual.id_usuario,
                fecha_edicion=fecha_edicion,
                precio=nuevo_precio,
            )
            print(
                f"Habitación '{habitacion_a_actualizar.numero}' actualizada exitosamente."
            )
        except Exception as e:
            print(f"Error al actualizar habitación: {e}")
            self.db.rollback()

    def eliminar_habitacion(self):
        """
        Permite eliminar una habitación existente del sistema a partir de la
        selección realizada por el usuario. El método muestra el listado de
        habitaciones registradas, solicita elegir una y ejecuta su eliminación
        mediante el módulo correspondiente.

        Si no hay habitaciones disponibles o la opción ingresada no es válida,
        se informa al usuario. En caso de presentarse algún error durante el
        proceso, se muestra un mensaje y se revierte la operación para evitar
        inconsistencias en la base de datos.
        """
        try:
            habitaciones = self.habitacion_crud.obtener_habitaciones(self.db)
            if not habitaciones:
                print("No hay habitaciones registradas.")
                return
            for i, u in enumerate(habitaciones, start=1):
                print(f"{i}. {u.numero} | ({u.tipo_habitacion}) | ")
            opcion = input("Elige el número del usuario a eliminar: ").strip()
            if (
                not opcion.isdigit()
                or int(opcion) < 1
                or int(opcion) > len(habitaciones)
            ):
                print("Opción inválida.")
                return
            habitacion_a_eliminar = habitaciones[int(opcion) - 1]
            self.habitacion_crud.eliminar_habitacion(
                self.db, habitacion_a_eliminar.id_habitacion
            )
            print(
                f"Habitación '{habitacion_a_eliminar.numero}' eliminado exitosamente."
            )
        except Exception as e:
            print(f"Error al eliminar la habitación: {e}")
            self.db.rollback()

    def listar_reservas(self):
        """
        Muestra el listado completo de reservas registradas en el sistema.
        El método consulta la base de datos para obtener todos los registros
        de reservas y presenta su información principal, como estado,
        fechas de inicio y fin, costo total, cantidad de personas y duración
        de la estancia.

        Si no existen reservas almacenadas, se informa al usuario mediante
        un mensaje. En caso de producirse algún problema durante la consulta,
        se notifica el error correspondiente.
        """
        try:
            reservas = self.reserva_crud.obtener_reservas(self.db)
            if not reservas:
                print("No hay habitaciones registradas.")
            else:
                for i, h in enumerate(reservas, start=1):
                    print(
                        f"{i}. Estado: {h.estado_reserva} | Fecha Entrada: {h.fecha_entrada} | Fecha Salida: {h.fecha_salida} | Total: {h.costo_total} | Numero de Personas: {h.numero_de_personas} | Numero de noches: {h.noches} "
                    )
        except Exception as e:
            print(f"Error al listar habitaciones: {e}")

    def listar_reservas_activas(self):
        """
        Muestra en pantalla todas las reservas que se encuentran activas en el
        sistema. El método consulta la base de datos para recuperar únicamente
        las reservas vigentes y presenta su información principal, como el
        identificador de la reserva, cliente, habitación asignada, fechas de
        inicio y fin, y su estado actual.

        Si no se encuentran reservas activas, se informa al usuario mediante
        un mensaje. En caso de error durante la consulta, se notifica el
        problema correspondiente.
        """
        try:
            reservas = self.reserva_crud.obtener_reservas_activas(self.db)
            if not reservas:
                print("No hay reservas activas.")
                return
            for r in reservas:
                cliente = self.db.get(Usuario, r.id_usuario)
                cliente_nombre = (
                    f"{cliente.nombre} {cliente.apellidos}"
                    if cliente
                    else "Desconocido"
                )
                print(
                    f"Reserva {r.id_reserva} | Cliente: {cliente_nombre} | Habitación: {r.id_habitacion} | {r.fecha_entrada} → {r.fecha_salida} | Estado: {r.estado_reserva}"
                )
        except Exception as e:
            print(f"Error al obtener reservas activas: {e}")

    def actualizar_perfil(self):
        """
        Permite al usuario modificar su información personal desde la consola.
        El método solicita nuevos datos como nombre, apellidos, teléfono,
        usuario y contraseña, mostrando previamente los valores actuales y
        permitiendo conservarlos si no se introduce información nueva.

        Si se detectan cambios válidos, el perfil se actualiza en la base de
        datos y se notifica al usuario. En caso contrario, se informa que no
        hubo modificaciones. También se validan ciertos datos, como la longitud
        de la contraseña, y se gestionan posibles errores realizando rollback
        si ocurre alguna falla durante el proceso.
        """
        try:
            usuario = self.usuario_crud.actualizar_usuario(
                self.db, self.usuario_actual.id_usuario
            )
            if not usuario:
                print("Usuario no encontrado.")
                return
            print("\n=== ACTUALIZAR PERFIL ===")
            nuevo_nombre = input(
                f"Nuevo nombre (actual: {usuario.nombre}) [Enter para mantener]: "
            ).strip()
            nuevos_apellidos = input(
                f"Nuevos apellidos (actual: {usuario.apellidos}) [Enter para mantener]: "
            ).strip()
            nuevo_telefono = input(
                f"Nuevo teléfono (actual: {usuario.telefono}) [Enter para mantener]: "
            ).strip()
            nuevo_usuario = input(
                f"Nuevo nombre de usuario (actual: {usuario.nombre_usuario}) [Enter para mantener]: "
            ).strip()
            nueva_clave = getpass.getpass("Nueva clave (Enter para mantener): ").strip()
            fecha_edita = datetime.now()
            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre
            if nuevos_apellidos:
                cambios["apellidos"] = nuevos_apellidos
            if nuevo_telefono:
                cambios["telefono"] = nuevo_telefono
            if nuevo_usuario:
                cambios["nombre_usuario"] = nuevo_usuario
            if nueva_clave:
                if len(nueva_clave) > 10:
                    print("La clave no puede exceder 10 caracteres.")
                    return
                cambios["clave"] = nueva_clave
            if cambios:
                self.usuario_crud.actualizar_usuario(
                    self.db,
                    id_usuario=self.usuario_actual.id_usuario,
                    id_usuario_edita=self.usuario_actual.id_usuario,
                    fecha_edicion=fecha_edita,
                    **cambios,
                )
                print("Perfil actualizado correctamente.")
            else:
                print("No se realizaron cambios.")
        except Exception as e:
            print(f"Error al actualizar perfil: {e}")
            self.db.rollback()

    def crear_usuario(self):
        """
        Permite registrar un nuevo usuario en el sistema mediante la entrada
        de datos por consola. El método solicita información personal como
        nombre, apellidos y teléfono, además del tipo de cuenta, nombre de
        usuario y contraseña (con una longitud máxima permitida).

        Se valida que el tipo de usuario ingresado sea correcto y luego se
        crea el registro con la fecha actual. Posteriormente, se intenta
        guardar el usuario en la base de datos utilizando el módulo
        correspondiente.

        Si ocurre algún problema durante el proceso, se muestra un mensaje
        de error y se revierte la operación para mantener la consistencia
        de la información almacenada.
        """
        try:
            print("\n=== CREAR USUARIO ===")
            nombre = input("Nombre: ").strip()
            apellidos = input("Apellidos: ").strip()
            telefono = input("Teléfono: ").strip()
            while True:
                tipo_usuario = (
                    input("Tipo de usuario (Administrador/Cliente): ")
                    .strip()
                    .capitalize()
                )
                if tipo_usuario in ["Administrador", "Cliente"]:
                    break
                print("Opción inválida. Debes ingresar 'Administrador' o 'Cliente'.")
            nombre_usuario = input("Nombre de usuario: ").strip()
            clave = getpass.getpass("Contraseña: ")
            fecha_creacion = datetime.now()
            nuevo_usuario = Usuario(
                nombre=nombre,
                apellidos=apellidos,
                telefono=telefono,
                tipo_usuario=tipo_usuario,
                nombre_usuario=nombre_usuario,
                clave=clave,
                fecha_creacion=fecha_creacion,
            )
            self.usuario_crud.crear_usuario(self.db, nuevo_usuario)
            print("Usuario creado exitosamente.")
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            self.db.rollback()

    def listar_usuarios(self):
        """
        Muestra en pantalla el listado de usuarios registrados en el sistema.
        El método consulta la base de datos para obtener todos los usuarios y
        presenta su información principal de forma ordenada y comprensible.

        Si no existen registros, se informa al usuario mediante un mensaje.
        También se gestionan posibles errores durante la consulta, mostrando
        una notificación adecuada en caso de que ocurra alguna excepción.
        """
        try:
            print("\n=== LISTA DE USUARIOS ===")
            usuarios = self.usuario_crud.obtener_usuarios(self.db)
            if not usuarios:
                print("No hay usuarios registrados.")
                return
            for i, u in enumerate(usuarios, start=1):
                print(
                    f"{i}. Tipo: {u.tipo_usuario} | Nombre: {u.nombre} {u.apellidos} | Telefono: {u.telefono}"
                )
        except Exception as e:
            print(f"Error al listar usuarios: {e}")

    def eliminar_usuario(self):
        """
        Permite eliminar un usuario existente del sistema a partir de la
        selección realizada por el operador. El método muestra el listado
        de usuarios registrados, solicita elegir uno y procede a borrar
        su registro de la base de datos.

        Si no hay usuarios disponibles, se informa al usuario mediante un
        mensaje. En caso de producirse algún error durante la operación,
        se notifica el problema y se revierte la transacción para evitar
        inconsistencias en la información.
        """
        try:
            print("\n=== ELIMINAR USUARIO ===")
            usuarios = self.usuario_crud.obtener_usuarios(self.db)
            if not usuarios:
                print("No hay usuarios registrados.")
                return
            for i, u in enumerate(usuarios, start=1):
                print(f"{i}. {u.nombre} | ({u.apellidos}) | {u.tipo_usuario}")
            opcion = input("Elige el número del usuario a eliminar: ").strip()
            if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(usuarios):
                print("Opción inválida.")
                return
            usuario_a_eliminar = usuarios[int(opcion) - 1]
            self.usuario_crud.eliminar_usuario(self.db, usuario_a_eliminar.id_usuario)
            print(
                f"Usuario '{usuario_a_eliminar.nombre_usuario}' eliminado exitosamente."
            )
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            self.db.rollback()

    def agregar_servicio(self):
        """
        Permite registrar un nuevo servicio adicional dentro del sistema.
        El método solicita al usuario la información básica del servicio,
        como su nombre, descripción y precio, y posteriormente crea el
        registro correspondiente en la base de datos para que pueda ser
        utilizado en las reservas.
        """
        try:
            print("\n=== AGREGAR SERVICIO ADICIONAL ===")
            nombre_servicio = input("Nombre del servicio: ").strip()
            fecha_creacion = datetime.now()
            descripcion = input("Descripción del servicio: ").strip()
            if not nombre_servicio:
                print("El nombre es obligatorio.")
                return
            while True:
                try:
                    precio = float(input("Precio del servicio: "))
                    break
                except ValueError:
                    print("Debes ingresar un número válido para el precio.")
            servicio = Servicios_Adicionales(
                nombre_servicio=nombre_servicio,
                precio=precio,
                descripcion=descripcion,
                id_usuario_crea=self.usuario_actual.id_usuario,
                fecha_creacion=fecha_creacion,
            )
            self.servicios_adicionales_crud.crear_servicio(self.db, servicio)
            print(f"Servicio '{servicio.nombre_servicio}' agregado exitosamente.")
        except Exception as e:
            print(f"Error al agregar servicio: {e}")
            self.db.rollback()

    def listar_servicios(self):
        """
        Muestra en pantalla el listado de servicios adicionales disponibles
        en el sistema, presentando la información principal de cada uno para
        facilitar su consulta.
        """
        try:
            servicios = self.servicios_adicionales_crud.obtener_servicios(self.db)
            if not servicios:
                print("No hay servicios registrados.")
                return
            print("\n=== LISTA DE SERVICIOS ADICIONALES ===")
            for s in servicios:
                print(
                    f"- ID: {s.id_servicio} | Nombre: {s.nombre_servicio} | Precio: ${s.precio} | Descripcion: {s.descripcion}"
                )
        except Exception as e:
            print(f"Error al listar servicios: {e}")

    def actualizar_servicio(self):
        """
        Permite modificar la información de un servicio adicional ya registrado
        en el sistema. El método muestra los servicios disponibles, solicita al
        usuario seleccionar uno y permite actualizar sus datos principales,
        como nombre, descripción o precio, guardando posteriormente los cambios.
        """
        try:
            servicios = self.servicios_adicionales_crud.obtener_servicios(self.db)
            if not servicios:
                print("No hay servicios registrados.")
                return
            for i, s in enumerate(servicios, start=1):
                print(f"{i}. {s.nombre_servicio} - ${s.precio} - {s.descripcion}")
            opcion = input("Selecciona el número del servicio a actualizar: ").strip()
            if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(servicios):
                print("Opción inválida.")
                return
            servicio = servicios[int(opcion) - 1]
            nuevo_nombre = input(
                f"Nuevo nombre (actual: {servicio.nombre_servicio}) [Enter para mantener]: "
            ).strip()
            nuevo_precio_input = input(
                f"Nuevo precio (actual: {servicio.precio}) [Enter para mantener]: "
            ).strip()
            descripcion_nueva = input(
                f"Descripcion (actual: {servicio.descripcion}) [Enter para mantener]: "
            ).strip()
            fecha_edita = date.today()
            id_usuario_edita = self.usuario_actual.id_usuario
            if nuevo_nombre:
                servicio.nombre_servicio = nuevo_nombre
            if nuevo_precio_input:
                try:
                    servicio.precio = float(nuevo_precio_input)
                except ValueError:
                    print("Precio inválido. Se mantiene el valor actual.")
            if descripcion_nueva:
                servicio.descripcion = descripcion_nueva
            self.servicios_adicionales_crud.actualizar_servicio(
                self.db, servicio, id_usuario_edita, fecha_edita
            )
            print("Servicio actualizado correctamente.")
        except Exception as e:
            print(f"Error al actualizar servicio: {e}")
            self.db.rollback()

    def eliminar_servicio(self):
        """
        Permite eliminar un servicio adicional del sistema a partir de la
        selección realizada por el usuario. El método muestra el listado de
        servicios disponibles, solicita elegir uno y procede a borrar su
        registro de la base de datos.

        Si ocurre algún problema durante la operación, se informa mediante
        un mensaje y se revierte la transacción para mantener la integridad
        de la información almacenada.
        """
        try:
            servicios = self.servicios_adicionales_crud.obtener_servicios(self.db)
            if not servicios:
                print("No hay servicios registrados.")
                return
            for i, s in enumerate(servicios, start=1):
                print(f"{i}. {s.nombre_servicio} - ${s.precio}")
            opcion = input("Selecciona el número del servicio a eliminar: ").strip()
            if not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(servicios):
                print("Opción inválida.")
                return
            servicio = servicios[int(opcion) - 1]
            self.servicios_adicionales_crud.eliminar_servicio(
                self.db, servicio.id_servicio
            )
            print(f"Servicio '{servicio.nombre_servicio}' eliminado exitosamente.")
        except Exception as e:
            print(f"Error al eliminar servicio: {e}")
            self.db.rollback()

    def eliminar_reserva(self):
        """
        Permite eliminar una reserva existente seleccionada por el usuario.
        El método muestra las reservas registradas, solicita elegir una y
        pide confirmación antes de realizar la operación para evitar
        eliminaciones accidentales.

        Si la eliminación se confirma, la reserva se borra de la base de
        datos y, en caso de estar asociada a una habitación, esta vuelve a
        marcarse como disponible. También se gestionan posibles errores,
        como selecciones inválidas o fallos durante el proceso.
        """
        reservas = self.db.query(Reserva).all()
        if not reservas:
            print("No hay reservas registradas.")
            return
        print("=== Reservas registradas ===")
        for i, reserva in enumerate(reservas, 1):
            habitacion = self.db.get(Habitacion, reserva.id_habitacion)
            habitacion_num = habitacion.numero if habitacion else "No asignada"
            cliente = self.db.get(Usuario, reserva.id_usuario)
            cliente_nombre = (
                f"{cliente.nombre} {cliente.apellidos}" if cliente else "Desconocido"
            )
            print(
                f"{i}. Cliente: {cliente_nombre} | Habitación: {habitacion_num} | Del {reserva.fecha_entrada} al {reserva.fecha_salida} - Total: ${reserva.costo_total:,.0f}"
            )
        opcion = input(
            "Selecciona el número de la reserva que deseas eliminar: "
        ).strip()
        if not opcion.isdigit() or not (1 <= int(opcion) <= len(reservas)):
            print("Opción inválida.")
            return
        reserva_seleccionada = reservas[int(opcion) - 1]
        confirmar = input("¿Deseas confirmar la eliminación? (1. Sí / 2. No): ").strip()
        if confirmar != "1":
            print("Eliminación cancelada.")
            return
        if reserva_seleccionada.id_habitacion:
            habitacion = self.db.get(Habitacion, reserva_seleccionada.id_habitacion)
            if habitacion:
                habitacion.disponible = True
        try:
            self.reserva_crud.eliminar_reserva(self.db, reserva_seleccionada.id_reserva)
            print("Reserva eliminada exitosamente.")
        except ValueError as e:
            print(f"Error: {e}")


def main():
    """Función principal"""
    with SistemaGestion() as sistema:
        sistema.ejecutar()


if __name__ == "__main__":
    main()
