from sources.Hotel import Hotel
from sources.HabitacionPresidencial import HabitacionPresidencial
from sources.HabitacionPremium import HabitacionPremium
from sources.HabitacionEstandar import HabitacionEstandar

habitacionEsta = HabitacionEstandar
habitacionPresi = HabitacionPresidencial
habitacionPre = HabitacionPremium


def menu() -> None:
    """
    Ejecuta el ciclo principal del sistema de reservas.

    Gestiona la interfaz de usuario por consola para:
    1. Crear reservas (seleccionando tipo de habitación y servicios extra).
    2. Cancelar reservas existentes mediante el documento.
    3. Listar todas las reservas actuales.
    4. Finalizar el programa.
    """
    hotel = Hotel()
    while True:
        print("\n===== SISTEMA DE RESERVAS DE HOTEL =====")
        print("1. Reservar habitación")
        print("2. Cancelar reserva")
        print("3. Mostrar reservas")
        print("4. Salir")

        while True:
            opcion = input("Seleccione una opción (1-4): ")
            if validar_opcion(opcion):
                print(f"Opción válida: {opcion}")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

        if opcion == "1":
            print("\n==========")
            print("Reservar habitación")
            cliente = validar_cadena_solo_letras("Nombre del cliente: ")
            documento = validar_id("Documento del cliente: ")
            noches = validar_numero_entero("Número de noches: ")
            while True:
                print("Tipos de habitación:")
                print("1. Estándar ($200000/noche)")
                print("2. Premiun ($300000/noche)")
                print("3. Presidencial ($450000/noche)")
                tipo = input("Seleccione tipo: ")

                if tipo.isdigit():
                    tipo = int(tipo)
                    if 1 <= tipo <= 3:
                        print("Opción válida:", tipo)
                        break
                    else:
                        print("El número debe estar entre 1 y 3.")
                else:
                    print("Debes ingresar un número válido.")
            if tipo == 1:
                nueva_reserva = hotel.reservar(
                    cliente, documento, noches, HabitacionEstandar
                )

                while True:
                    opcion_television = input(
                        "¿Desea agregar servicio de televisión por $20000 adicional al total? (si/no): "
                    )
                    if validar_opcion_yes(opcion_television):
                        if opcion_television.lower() == "si".lower():
                            nueva_reserva.habitacion.servicio_television = True
                        costo_habitacion_estandar = (
                            nueva_reserva.habitacion.calcular_costo(noches)
                        )
                        print(
                            f"Costo total de la habitación estándar: ${costo_habitacion_estandar}"
                        )
                        break
                    else:
                        print("Opción no válida. Intente nuevamente.")
            elif tipo == 2:
                nueva_reserva = hotel.reservar(
                    cliente, documento, noches, HabitacionPremium
                )

                while True:
                    opcion_jacuzzi = input(
                        "¿Desea agregar servicio de jacuzzi por $50000 adicional al total? (si/no): "
                    )
                    if validar_opcion_yes(opcion_jacuzzi):
                        if opcion_jacuzzi.lower() == "si".lower():
                            nueva_reserva.habitacion.servicio_yacuzzi = True
                        costo_habitacion_premium = (
                            nueva_reserva.habitacion.calcular_costo(noches)
                        )
                        print(
                            f"Costo total de la habitación premium: ${costo_habitacion_premium}"
                        )
                        break
                    else:
                        print("Opción no válida. Intente nuevamente.")
            elif tipo == 3:
                nueva_reserva = hotel.reservar(
                    cliente, documento, noches, HabitacionPresidencial
                )

                while True:
                    opcion_cine = input(
                        "¿Desea agregar servicio de cine por $300000 adicional al total? (si/no): "
                    )
                    if validar_opcion_yes(opcion_cine):
                        if opcion_cine.lower() == "si".lower():
                            nueva_reserva.habitacion.servicio_cine_integrado = True
                        costo_habitacion_presidencial = (
                            nueva_reserva.habitacion.calcular_costo(noches)
                        )
                        print(
                            f"Costo total de la habitación presidencial: ${costo_habitacion_presidencial}"
                        )
                        break
                    else:
                        print("Opción no válida. Intente nuevamente.")
            else:
                print("Tipo inválido.")

        elif opcion == "2":
            documento = input(
                "Ingrese el documento del cliente para cancelar la reserva: "
            )
            hotel.cancelar_reserva(documento)
        elif opcion == "3":
            hotel.mostrar_reservas()
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    menu()
