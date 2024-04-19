from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

# Clase para el nodo del árbol AVL
class AVLNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

# Clase para el árbol AVL
class AVLTree:
    def __init__(self):
        self.root = None

    # Función para insertar un nodo en el árbol
    def insert(self, key, data):
        if not self.root:
            self.root = AVLNode(key, data)
        else:
            self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if not node:
            return AVLNode(key, data)
        elif key < node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        if balance > 1 and key < node.left.key:
            return self._rotate_right(node)
        if balance < -1 and key > node.right.key:
            return self._rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _rotate_left(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _rotate_right(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

# Función para cargar registros desde un archivo CSV
def load_records_from_csv(file_path):
    records = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)
    return records

# Ruta para cargar registros desde un archivo CSV
@app.route('/load_records', methods=['POST'])
def load_records():
    file_path = 'data.csv'  # Ruta relativa al archivo CSV
    records = load_records_from_csv(file_path)
    for record in records:
        avl_tree.insert(int(record['id']), record)
    return jsonify({'message': 'Records loaded successfully'})

# Ruta para insertar un registro manualmente
@app.route('/insert_record', methods=['POST'])
def insert_record():
    data = request.get_json()
    record_id = data.get('id')
    record_data = data.get('data')
    avl_tree.insert(record_id, record_data)
    return jsonify({'message': 'Record inserted successfully'})

# Ruta para buscar un registro por su identificador
@app.route('/search_record/<int:record_id>', methods=['GET'])
def search_record(record_id):
    found_record_data = search_record_in_tree(avl_tree.root, record_id)
    if found_record_data:
        return jsonify({'message': 'Record found', 'data': found_record_data})
    else:
        return jsonify({'message': 'Record not found'})

# Función auxiliar para buscar un registro en el árbol AVL
def search_record_in_tree(node, record_id):
    if not node:
        return None
    if node.key == record_id:
        return node.data
    elif record_id < node.key:
        return search_record_in_tree(node.left, record_id)
    else:
        return search_record_in_tree(node.right, record_id)

# Ruta para mostrar información del grupo
@app.route('/group_info', methods=['GET'])
def group_info():
    group_info = {
        'members': [
            {'name': 'Nombre1', 'carnet': 'Carnet1', 'contributions': 'Contribuciones1'},
            {'name': 'Nombre2', 'carnet': 'Carnet2', 'contributions': 'Contribuciones2'},
            # Agregar más miembros según sea necesario
        ]
    }
    return jsonify(group_info)

if __name__ == '__main__':
    avl_tree = AVLTree()  # Inicializar el árbol AVL
    app.run(debug=True)  # Ejecutar la aplicación Flask en modo debug
