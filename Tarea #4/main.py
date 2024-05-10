import csv
from MatrizDispersa import MatrizDispersa
from GeneradorDeGrafico import visualize_sparse_matrix

def load_from_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Salta la primera fila (encabezados)
        for row in reader:
            data.append([float(val) for val in row])
    return data

def manual_input():
    print("Ingrese los datos de la matriz dispersa:")
    rows = int(input("Número de filas: "))
    cols = int(input("Número de columnas: "))
    data = []
    for i in range(rows):
        row = []
        for j in range(cols):
            val = float(input(f"Ingrese el valor para [{i},{j}]: "))
            row.append(val)
        data.append(row)
    return data

def main():
    print("Bienvenido al programa de creación de matriz dispersa.")
    print("Seleccione una opción:")
    print("1. Cargar desde archivo CSV")
    print("2. Entrada manual")
    choice = input("Opción: ")
    
    if choice == "1":
        file_path = input("Ingrese la ruta del archivo CSV: ")
        data = load_from_csv(file_path)
    elif choice == "2":
        data = manual_input()
    else:
        print("Opción no válida. Saliendo del programa.")
        return
    
    sparse_matrix = MatrizDispersa(data)
    sparse_matrix.print_matrix()
    
    print("¿Cómo le gustaría visualizar la matriz dispersa?")
    print("1. Por consola")
    print("2. Utilizando Graphviz")
    visualize_choice = input("Opción: ")
    
    if visualize_choice == "1":
        sparse_matrix.print_matrix()
    elif visualize_choice == "2":
        visualize_sparse_matrix(sparse_matrix)
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    main()
