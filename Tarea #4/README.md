Curso: Programación II
Sección: B
Tarea No.4

Integrantes:
Carné: 9490-22-14408 Nombre: Luis Eduardo Gonzalez Alvarado (100%)
Carné: 9490-22-4796  Nombre: Keily Andrea Tobar Morales     (100%)

--------- Descripción del Programa --------
Este programa está diseñado para trabajar con matrices especiales llamadas "dispersas", estás son más eficientes de manejar.
El programa permite al usuario cargar los datos de la matriz desde un archivo CSV o ingresarlos manualmente, luego crea la matriz dispersa utilizando la clase Matriz Dispersa y ofrece dos opciones de visualización: por consola o utilizando Graphviz.

-------- Pasos para Ejecutar el Programa ----------

1. Inicio del programa: Al ejecutar el programa, se llama a la función main().

2. Menú de selección: Se muestra un menú que permite al usuario seleccionar cómo desea ingresar los datos de la matriz dispersa:

- Si elige "1", el programa solicita la ruta del archivo CSV que contiene los datos de la matriz.
- Si elige "2", el usuario ingresa manualmente los datos de la matriz.

3. Carga de datos: Dependiendo de la opción seleccionada, se cargan los datos de la matriz desde un archivo CSV o se ingresan manualmente. La función load_from_csv() lee el archivo CSV y devuelve los datos como una lista de listas, mientras que la función manual_input() solicita al usuario que ingrese los valores uno por uno.

4. Creación de la matriz dispersa: Una vez que se obtienen los datos de la matriz, se crea un objeto Matriz Dispersa con estos datos.

5. Visualización de la matriz: Se ofrece al usuario la opción de cómo desea visualizar la matriz dispersa:

- Si elige "1", se imprime la matriz dispersa por consola.
- Si elige "2", se utiliza Graphviz para generar una representación visual de la matriz dispersa.
Finalización del programa: Después de visualizar la matriz, el programa termina su ejecución.

En resumen, el programa permite al usuario cargar o ingresar manualmente los datos de una matriz dispersa, la crea, la visualiza de acuerdo con la elección del usuario y luego finaliza.

--------- Representación Visual de la Matriz Dispersa ---------

1. Inicialización del objeto Dot: Se crea un objeto Digraph de Graphviz llamado dot. Esto proporciona un lienzo en el que se construirá el gráfico.

2. Ajustes de atributos: Se especifican ciertos atributos para el gráfico, como la dirección del diseño (rankdir) y el tamaño del lienzo (size). En este caso, el tamaño del lienzo se ha aumentado para que la imagen resultante sea más grande y más legible.

3. Creación de nodos para filas: Se recorre cada fila de la matriz. Para cada fila, se crea un nodo en el gráfico. El contenido de cada nodo representa los valores no cero en esa fila. Se utiliza el formato plaintext para que los nodos puedan contener texto formateado.

4. Creación de enlaces entre nodos: Se recorre cada elemento de la matriz. Si el valor en esa posición es distinto de cero, se crea un enlace desde el nodo de fila correspondiente al mismo nodo de fila. Esto se hace para resaltar la posición de los elementos no cero en la matriz.

5. Renderizado y guardado de la imagen: Se determina la ruta de salida donde se guardará la imagen del gráfico. En este caso, se crea un directorio llamado "Grafico" en la misma ubicación que el archivo de código si aún no existe. Luego, se guarda la imagen del gráfico en formato PNG en ese directorio. La función render() se encarga de generar el gráfico en el formato especificado y guardarlo en el archivo indicado.

6. Impresión de información: Se imprime la ruta de salida del archivo generado para que el usuario pueda ubicar la imagen. También se imprime un mensaje indicando que la visualización de la matriz dispersa ha sido generada con éxito.

la función recorre la matriz dispersa, construye un gráfico en Graphviz donde los nodos representan las filas y los enlaces entre nodos resaltan los elementos no cero en la matriz, y luego guarda la imagen del gráfico generado en un archivo PNG.

--------- Tipo de Matriz Dispersa ----------

Esquema CRS (Comprossed Row Storage)
- Cada fila de la matriz dispersa se representa como un nodo en el grafo.
- Los elementos no cero de cada fila se muestran como etiquetas dentro de los nodos correspondientes.
- Los enlaces entre los nodos representan las conexiones entre las filas de la matriz dispersa, pero en este caso, se utilizan para resaltar la posición de los elementos no cero en la misma fila. Por lo tanto, estos enlaces son bucles que van desde un nodo de fila a sí mismo.
- Es una representación visual de la matriz dispersa, donde las conexiones entre los nodos resaltan los elementos no cero en la misma fila de la matriz. 
Esto proporciona una manera intuitiva de visualizar la estructura y los elementos de la matriz dispersa.

--------- Link PDF Manual -----------

https://drive.google.com/file/d/1UGqXHYRuAFYTCNjGlVVZfIqZyaJavUyL/view?usp=sharing




