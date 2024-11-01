import networkx as nx
import matplotlib.pyplot as plt

# Función para crear el grafo de un tablero de tamaño especificado
def crear_grafo_tablero(tamaño):
    G = nx.Graph()

    # Crear nodos para cada posición en el tablero
    for i in range(tamaño):
        for j in range(tamaño):
            G.add_node((i, j))  # Cada nodo es una casilla (i, j)

    # Crear aristas (conexiones) entre casillas adyacentes (incluyendo diagonales)
    for i in range(tamaño):
        for j in range(tamaño):
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue  # Ignorar la casilla actual
                    x, y = i + dx, j + dy
                    if 0 <= x < tamaño and 0 <= y < tamaño:
                        G.add_edge((i, j), (x, y))  # Crear arista entre nodos adyacentes
    return G

# Crear el grafo para un tablero de 10x10
tamaño_tablero = 10
grafo_tablero = crear_grafo_tablero(tamaño_tablero)

# Definir posiciones de nodos para visualización
pos = {(i, j): (j, -i) for i in range(tamaño_tablero) for j in range(tamaño_tablero)}

# Marcar las primeras 3 filas de la parte superior y las últimas 3 filas de la parte inferior
top_pieces = [(i, j) for i in range(3) for j in range(tamaño_tablero)]
bottom_pieces = [(i, j) for i in range(tamaño_tablero - 3, tamaño_tablero) for j in range(tamaño_tablero)]

# Definir colores de nodos: azul claro para casillas normales, rojo para "bolas" superiores, verde para "bolas" inferiores
node_colors = []
for node in grafo_tablero.nodes():
    if node in top_pieces:
        node_colors.append('red')
    elif node in bottom_pieces:
        node_colors.append('green')
    else:
        node_colors.append('lightblue')

# Dibujar el grafo con los colores especificados
nx.draw(grafo_tablero, pos, node_size=300, node_color=node_colors, with_labels=True, font_size=8)

# Mostrar el grafo
plt.show()
