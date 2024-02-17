class Nodo:
    def __init__(self, nombre, apellido, carnet):
        self.nombre = nombre
        self.apellido = apellido
        self.carnet = carnet
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.inicio = None
        self.fin = None

    def insertar_al_principio(self, nombre, apellido, carnet):
        nuevo_nodo = Nodo(nombre, apellido, carnet)
        if self.inicio is None:
            self.inicio = self.fin = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.inicio
            self.inicio.anterior = nuevo_nodo
            self.inicio = nuevo_nodo

    def insertar_al_final(self, nombre, apellido, carnet):
        nuevo_nodo = Nodo(nombre, apellido, carnet)
        if self.fin is None:
            self.inicio = self.fin = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.fin
            self.fin.siguiente = nuevo_nodo
            self.fin = nuevo_nodo

    def eliminar_por_valor(self, carnet):
        actual = self.inicio
        while actual is not None:
            if actual.carnet == carnet:
                if actual.anterior is not None:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.inicio = actual.siguiente

                if actual.siguiente is not None:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.fin = actual.anterior

                return
            actual = actual.siguiente

    def mostrar_lista(self):
        actual = self.inicio
        lista_str = "None <- "
        while actual is not None:
            lista_str += f"{actual.nombre} {actual.apellido} ({actual.carnet}) <-> "
            actual = actual.siguiente
        lista_str += "None"
        print(lista_str)

def menu():
    lista = ListaDoblementeEnlazada()
    while True:
        print("\nMenu:")
        print("1. Insertar al principio")
        print("2. Insertar al final")
        print("3. Eliminar por valor")
        print("4. Mostrar lista")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            carnet = input("Ingrese el carnet: ")
            lista.insertar_al_principio(nombre, apellido, carnet)
        elif opcion == "2":
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            carnet = input("Ingrese el carnet: ")
            lista.insertar_al_final(nombre, apellido, carnet)
        elif opcion == "3":
            carnet = input("Ingrese el carnet del estudiante a eliminar: ")
            lista.eliminar_por_valor(carnet)
        elif opcion == "4":
            lista.mostrar_lista()
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    menu()
