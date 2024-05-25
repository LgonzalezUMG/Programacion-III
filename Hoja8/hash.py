import random
import string
import csv

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        return hash(key) % self.size

    def generate_key(self):
        letter = random.choice(string.ascii_uppercase)
        number = random.randint(0, 9999)
        key = f"{letter}#{number}"
        return key

    def insert(self, value):
        key = self.generate_key()
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                return key
        self.table[index].append([key, value])
        return key

    def search_by_key(self, key):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        return None

    def search_by_value(self, value):
        results = []
        for bucket in self.table:
            for item in bucket:
                if item[1] == value:
                    results.append(item[0])
        return results

    def display(self):
        for index, bucket in enumerate(self.table):
            print(f"Index {index}: {bucket}")

    def load_from_csv(self, file_path):
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Skip header row
            for row in csv_reader:
                for value in row:  # Insert each field individually
                    self.insert(value)

# Funciones de ayuda para la interacción del usuario
def manual_insertion(ht):
    value = input("Ingrese el valor: ")
    key = ht.insert(value)
    print(f"Insertado: clave = {key}, valor = {value}")

def search_by_key(ht):
    key = input("Ingrese la clave a buscar: ")
    result = ht.search_by_key(key)
    if result:
        print(f"Valor encontrado: {result}")
    else:
        print("Clave no encontrada.")

def search_by_value(ht):
    value = input("Ingrese el valor a buscar: ")
    results = ht.search_by_value(value)
    if results:
        print(f"Claves encontradas: {results}")
    else:
        print("Valor no encontrado.")

def main():
    ht = HashTable(size=10)
    while True:
        print("\nOpciones:")
        print("1. Inserción manual")
        print("2. Búsqueda por clave")
        print("3. Búsqueda por valor")
        print("4. Cargar desde archivo CSV")
        print("5. Mostrar tabla hash")
        print("6. Salir")

        option = int(input("Seleccione una opción: "))

        if option == 1:
            manual_insertion(ht)
        elif option == 2:
            search_by_key(ht)
        elif option == 3:
            search_by_value(ht)
        elif option == 4:
            file_path = input("Ingrese la ruta del archivo CSV: ")
            ht.load_from_csv(file_path)
            print("Datos cargados desde el archivo.")
        elif option == 5:
            ht.display()
        elif option == 6:
            break
        else:
            print("Opción no válida, intente nuevamente.")

if __name__ == "__main__":
    main()
