def convertir_a_binario(numero):
    if numero > 1:
        convertir_a_binario(numero // 2)
    print(numero % 2, end='')

def contar_digitos(numero):
    if numero == 0:
        return 0
    return 1 + contar_digitos(numero // 10)

def calcular_raiz_cuadrada(numero, estimacion=0):
    if estimacion**2 == numero:
        return estimacion
    elif estimacion**2 > numero:
        return estimacion - 1
    else:
        return calcular_raiz_cuadrada(numero, estimacion + 1)

def raiz_cuadrada_entera(numero):
    if numero < 0:
        return "No se puede calcular la raíz cuadrada de un número negativo"
    elif numero == 0:
        return 0
    else:
        return calcular_raiz_cuadrada(numero)

def convertir_a_decimal_romano(romano):
    romanos = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    if len(romano) == 1:
        return romanos[romano]

    if romanos[romano[0]] < romanos[romano[1]]:
        return -romanos[romano[0]] + convertir_a_decimal_romano(romano[1:])
    else:
        return romanos[romano[0]] + convertir_a_decimal_romano(romano[1:])

def suma_numeros_enteros(numero):
    if numero == 0:
        return 0
    return numero + suma_numeros_enteros(numero - 1)

def mostrar_menu():
    print("\nMenú:")
    print("1. Convertir a binario")
    print("2. Contar dígitos")
    print("3. Raíz cuadrada entera")
    print("4. Convertir a decimal desde romano")
    print("5. Suma de números enteros")
    print("0. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "0":
            print("¡Hasta luego!")
            break
        elif opcion == "1":
            numero = int(input("Ingrese un número entero: "))
            print("El número en binario es:", end=' ')
            convertir_a_binario(numero)
        elif opcion == "2":
            numero = int(input("Ingrese un número entero: "))
            print("El número de dígitos es:", contar_digitos(numero))
        elif opcion == "3":
            numero = int(input("Ingrese un número entero: "))
            print("La raíz cuadrada entera es:", raiz_cuadrada_entera(numero))
        elif opcion == "4":
            romano = input("Ingrese un número romano: ").upper()
            print("El número decimal equivalente es:", convertir_a_decimal_romano(romano))
        elif opcion == "5":
            numero = int(input("Ingrese un número entero positivo: "))
            print("La suma de los números enteros desde 0 hasta", numero, "es:", suma_numeros_enteros(numero))
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()