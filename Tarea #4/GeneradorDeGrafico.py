import os
import graphviz

def visualize_sparse_matrix(matrix):
    dot = graphviz.Digraph()
    dot.attr(rankdir='LR', size='150,130')  # Aumentar el tamaño de la imagen
    dot.node_attr.update(shape='plaintext')

    for i in range(matrix.rows):
        row_label = ""
        for j in range(matrix.cols):
            if matrix.data[i][j] != 0:
                row_label += f"<{i}_{j}> {matrix.data[i][j]} | "
        dot.node(f"row_{i}", label=f"{{ {row_label} }}")

    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if matrix.data[i][j] != 0:
                dot.edge(f"row_{i}", f"row_{i}", f"<{i}_{j}>")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(current_dir, 'Grafico')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, 'sparse_matrix.png')
    print(f"La ruta de salida es: {output_path}")  # Imprimir la ruta de salida
    dot.render(output_path, format='png', cleanup=True)
    print(f"Visualización de la matriz dispersa generada como '{output_path}'")
