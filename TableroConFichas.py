import networkx as nx
import matplotlib.pyplot as plt

# Función para crear el grafo de un tablero de Damas Chinas
def crear_grafo_tablero(tamaño):
    G = nx.Graph()

    # Crear nodos para cada posición en el tablero
    for i in range(tamaño):
        for j in range(tamaño):
            G.add_node((i, j))

    # Crear aristas (solo en diagonal y adyacencias horizontales/verticales)
    for i in range(tamaño):
        for j in range(tamaño):
            if i > 0:
                G.add_edge((i, j), (i - 1, j))  # Arriba
            if i < tamaño - 1:
                G.add_edge((i, j), (i + 1, j))  # Abajo
            if j > 0:
                G.add_edge((i, j), (i, j - 1))  # Izquierda
            if j < tamaño - 1:
                G.add_edge((i, j), (i, j + 1))  # Derecha
            if i > 0 and j > 0:
                G.add_edge((i, j), (i - 1, j - 1))  # Diagonal superior izquierda
            if i > 0 and j < tamaño - 1:
                G.add_edge((i, j), (i - 1, j + 1))  # Diagonal superior derecha
            if i < tamaño - 1 and j > 0:
                G.add_edge((i, j), (i + 1, j - 1))  # Diagonal inferior izquierda
            if i < tamaño - 1 and j < tamaño - 1:
                G.add_edge((i, j), (i + 1, j + 1))  # Diagonal inferior derecha

    return G

# Crear el grafo para un tablero de 10x10
tamaño_tablero = 10
grafo_tablero = crear_grafo_tablero(tamaño_tablero)

# Definir posiciones de nodos para visualización
pos = {(i, j): (j, -i) for i in range(tamaño_tablero) for j in range(tamaño_tablero)}

# Definir las posiciones de las fichas de Damas Chinas
top_pieces = [(i, j) for i in range(3) for j in range(tamaño_tablero) if (i + j) % 2 == 1]
bottom_pieces = [(i, j) for i in range(tamaño_tablero - 3, tamaño_tablero) for j in range(tamaño_tablero) if (i + j) % 2 == 1]

# Definir colores de nodos
node_colors = []
for node in grafo_tablero.nodes():
    if node in top_pieces:
        node_colors.append('red')  # Fichas superiores (rojas)
    elif node in bottom_pieces:
        node_colors.append('green')  # Fichas inferiores (verdes)
    else:
        node_colors.append('lightgray')  # Casillas vacías

# Dibujar el grafo
nx.draw(grafo_tablero, pos, node_size=300, node_color=node_colors, with_labels=True, font_size=8, edge_color='black')

# Mostrar el grafo
plt.show()
