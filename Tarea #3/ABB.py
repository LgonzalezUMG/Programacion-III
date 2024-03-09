import os
from graphviz import Digraph

# Obtener la ruta del archivo actual
current_path = os.path.dirname(os.path.abspath(__file__))

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.graph = Digraph()

    def insert(self, data):
        if not self.root:
            self.root = TreeNode(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = TreeNode(data)
            else:
                self._insert_recursive(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = TreeNode(data)
            else:
                self._insert_recursive(node.right, data)

    def search(self, data):
        return self._search_recursive(self.root, data)

    def _search_recursive(self, node, data):
        if node is None or node.data == data:
            return node
        if data < node.data:
            return self._search_recursive(node.left, data)
        return self._search_recursive(node.right, data)

    def delete(self, data):
        self.root = self._delete_recursive(self.root, data)

    def _delete_recursive(self, root, data):
        if root is None:
            return root
        if data < root.data:
            root.left = self._delete_recursive(root.left, data)
        elif data > root.data:
            root.right = self._delete_recursive(root.right, data)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self._min_value_node(root.right)
            root.data = temp.data
            root.right = self._delete_recursive(root.right, temp.data)
        return root

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def load_from_file(self, filename):
        file_path = os.path.join(current_path, filename)  # Construir la ruta del archivo
        if not os.path.exists(file_path):
            print("El archivo no existe.")
            return
        with open(file_path, 'r') as file:
            for line in file:
                data = int(line.strip())
                self.insert(data)

    def to_binary(self):
        if not self.root:
            return
        self._to_binary_recursive(self.root)

    def _to_binary_recursive(self, node):
        if node is None:
            return
        self._to_binary_recursive(node.left)
        self._to_binary_recursive(node.right)
        if node.left and node.right:
            node.right = TreeNode(node.left.data)
            node.left = None

    def generate_graphviz(self):
        self.graph = Digraph()
        self._add_nodes_to_graphviz(self.root)
        self.graph.render('binary_tree', format='png', cleanup=True)
        print("Se ha generado la representación en Graphviz del árbol.")
        input("Presiona Enter para continuar...")

    def _add_nodes_to_graphviz(self, node):
        if node is None:
            return
        self.graph.node(str(node.data))
        if node.left:
            self.graph.edge(str(node.data), str(node.left.data))
            self._add_nodes_to_graphviz(node.left)
        if node.right:
            self.graph.edge(str(node.data), str(node.right.data))
            self._add_nodes_to_graphviz(node.right)

def menu():
    print("1. Insertar")
    print("2. Buscar")
    print("3. Eliminar")
    print("4. Cargar desde Archivo")
    print("5. Convertir a binario el árbol")
    print("6. Generar representación en Graphviz")
    print("7. Salir")

if __name__ == "__main__":
    tree = BinarySearchTree()
    while True:
        print("\nÁrbol Binario de Búsqueda")
        menu()
        choice = input("Seleccione una opción: ")
        if choice == "1":
            data = int(input("Ingrese el número a insertar: "))
            tree.insert(data)
        elif choice == "2":
            data = int(input("Ingrese el número a buscar: "))
            if tree.search(data):
                print("El número está en el árbol.")
            else:
                print("El número no está en el árbol.")
        elif choice == "3":
            data = int(input("Ingrese el número a eliminar: "))
            tree.delete(data)
        elif choice == "4":
            filename = input("Ingrese el nombre del archivo: ")
            tree.load_from_file(filename)
        elif choice == "5":
            tree.to_binary()
            print("El árbol se ha convertido a binario.")
        elif choice == "6":
            tree.generate_graphviz()
        elif choice == "7":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")
