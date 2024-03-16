import os
from graphviz import Digraph

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return Node(key)
        else:
            if key < root.val:
                root.left = self.insert(root.left, key)
            else:
                root.right = self.insert(root.right, key)
        return root

    def search(self, root, key):
        if root is None or root.val == key:
            return root
        if root.val < key:
            return self.search(root.right, key)
        return self.search(root.left, key)

    def minValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def deleteNode(self, root, key):
        if root is None:
            return root
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.minValueNode(root.right)
            root.val = temp.val
            root.right = self.deleteNode(root.right, temp.val)
        return root

    def convert_to_binary(self, root):
        if root is None:
            return None
        dot = Digraph()
        stack = [root]
        while stack:
            current = stack.pop()
            if current:
                dot.node(str(current.val))
                if current.left:
                    dot.node(str(current.left.val))
                    dot.edge(str(current.val), str(current.left.val))
                    stack.append(current.left)
                if current.right:
                    dot.node(str(current.right.val))
                    dot.edge(str(current.val), str(current.right.val))
                    stack.append(current.right)
        dot.render('binary_tree', format='png', cleanup=True)
        return 'binary_tree.png'


def print_menu():
    print("1. Insertar nodo")
    print("2. Buscar nodo")
    print("3. Eliminar nodo")
    print("4. Cargar desde archivo")
    print("5. Convertir a binario")
    print("6. Salir")


def main():
    bst = BinarySearchTree()
    while True:
        print("\nÁrbol Binario de Búsqueda - Menú:")
        print_menu()
        choice = int(input("Seleccione una opción: "))
        if choice == 1:
            key = int(input("Ingrese el valor del nodo a insertar: "))
            bst.root = bst.insert(bst.root, key)
            print("Nodo insertado exitosamente.")
        elif choice == 2:
            key = int(input("Ingrese el valor del nodo a buscar: "))
            if bst.search(bst.root, key):
                print("El nodo está presente en el árbol.")
            else:
                print("El nodo no está presente en el árbol.")
        elif choice == 3:
            key = int(input("Ingrese el valor del nodo a eliminar: "))
            bst.root = bst.deleteNode(bst.root, key)
            print("Nodo eliminado exitosamente.")
        elif choice == 4:
            filepath = input("Ingrese la ruta completa del archivo (por ejemplo, C:\\Users\\WichoxXGT\\Documents\\datos.txt): ")
            with open(filepath, 'r') as file:
                for line in file:
                    key = int(line.strip())
                    bst.root = bst.insert(bst.root, key)
            print("Datos cargados desde el archivo exitosamente.")
        elif choice == 5:
            png_path = bst.convert_to_binary(bst.root)
            print(f"Árbol convertido a binario y la representación visual ha sido guardada en {png_path}.")
        elif choice == 6:
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    main()
