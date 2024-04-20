import os
import csv
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

# Información de los integrantes del grupo
integrantes = [
    {
        'nombre': 'Keily Andrea Tobar Morales',
        'carne': '9490-22-4796',
        'contribuciones': 'Implementación de la funcionalidad de inserción de registros y pruebas de la API.'
    },
    {
        'nombre': 'Luis Eduardo González Alvarado',
        'carne': '9490-22-14408',
        'contribuciones': 'Desarrollo de la funcionalidad de búsqueda de registros y documentación del proyecto.'
    }
]

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = TreeNode(data)
        else:
            self._insert_recursively(self.root, data)

    def _insert_recursively(self, node, data):
        for key, value in data.items():
            if isinstance(value, dict):
                self._insert_recursively(node, value)
            else:
                if key not in node.data:
                    node.data[key] = value
                elif isinstance(node.data[key], list):
                    node.data[key].append(value)
                else:
                    node.data[key] = [node.data[key], value]

# Función para cargar un archivo CSV en un árbol binario
def cargar_csv(file_path):
    start_time = time.time()
    binary_tree = BinaryTree()

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                binary_tree.insert(row)

        elapsed_time = time.time() - start_time
        return binary_tree, elapsed_time
    except Exception as e:
        return None, str(e)

binary_tree = None
carga_time = None

# Ruta para cargar un archivo CSV en un árbol binario
@app.route('/cargar_csv', methods=['POST'])
def cargar_csv_route():
    global binary_tree, carga_time

    # Verificamos si se proporcionó un archivo CSV
    if 'file' not in request.files:
        return jsonify({'error': 'No se proporcionó ningún archivo CSV'}), 400
    
    file = request.files['file']
    if file:
        try:
            file_path = "data.csv"
            file.save(file_path)

            binary_tree, carga_time = cargar_csv(file_path)
            if binary_tree:
                return jsonify({'message': 'Archivo CSV cargado correctamente'}), 200
            else:
                return jsonify({'error': carga_time}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'No se proporcionó ningún archivo CSV'}), 400

# Ruta para obtener la información cargada en el árbol binario
@app.route('/info_cargada', methods=['GET'])
def info_cargada():
    global binary_tree, carga_time
    if not binary_tree:
        return jsonify({'message': 'No hay información cargada en el árbol binario'}), 404

    def get_nodes(node):
        if not node:
            return []
        if node.data is None:
            return []
        return [node.data] + get_nodes(node.left) + get_nodes(node.right)

    nodos = get_nodes(binary_tree.root)
    return jsonify({'nodos': [n for n in nodos if n], 'tiempo_carga': carga_time}), 200

registros_manual = []  # Lista para almacenar registros manuales

# Ruta para agregar un nuevo registro manualmente
@app.route('/registro_manual', methods=['POST'])
def add_registro_manual():
    data = request.json
    registros_manual.append(data)
    return jsonify({'message': 'Registro agregado correctamente'}), 200

# Ruta para buscar un registro manual por su ID
@app.route('/buscar_manual/<int:id>', methods=['GET'])
def buscar_registro_manual(id):
    for registro in registros_manual:
        if registro['ID'] == id:
            return jsonify({'registro': registro}), 200
    
    return jsonify({'message': 'Registro no encontrado'}), 404

# Ruta para obtener los integrantes del grupo
@app.route('/integrantes', methods=['GET'])
def get_integrantes():
    return jsonify(integrantes), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')