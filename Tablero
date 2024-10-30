import networkx as nx
import matplotlib.pyplot as plt

# Función para crear el grafo de un tablero de 10x10
def crear_grafo_tablero(tamaño):
    G = nx.Graph()
    
    # Crear nodos para cada posición en el tablero
    for i in range(tamaño):
        for j in range(tamaño):
            G.add_node((i, j))  # Cada nodo es una casilla (i, j)
    
    # Crear aristas (conexiones) entre casillas adyacentes (incluyendo diagonales)
    for i in range(tamaño):
        for j in range(tamaño):
            # Conectar con las casillas adyacentes
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

# Dibujar el grafo
pos = {(i, j): (j, -i) for i in range(tamaño_tablero) for j in range(tamaño_tablero)}  # Posiciones de los nodos
nx.draw(grafo_tablero, pos, node_size=300, with_labels=True, node_color='lightblue', font_size=8)

# Mostrar el grafo
plt.show()
