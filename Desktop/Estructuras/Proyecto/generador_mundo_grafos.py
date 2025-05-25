import networkx as nx
import matplotlib.pyplot as plt
import random

# Función para generar nombres ficticios
def generar_lugares():
    return [
        "Bosque Sombrío", "Castillo del Eco", "Aldea del Viento", "Cueva del Trueno",
        "Montaña de Cristal", "Llanura Dorada", "Río de la Luna", "Ruinas del Olvido",
        "Templo de Fuego", "Isla Perdida"
    ]

# Función para crear un grafo de mundo ficticio
def generar_mapa():
    lugares = generar_lugares()
    G = nx.Graph()

    for lugar in lugares:
        G.add_node(lugar)

    # Garantizar que el grafo sea conexo
    conectados = [lugares[0]]
    no_conectados = lugares[1:]

    while no_conectados:
        a = random.choice(conectados)
        b = random.choice(no_conectados)
        peso = random.randint(1, 10)
        G.add_edge(a, b, weight=peso)
        conectados.append(b)
        no_conectados.remove(b)

    # Agregar caminos adicionales
    for _ in range(5):
        a, b = random.sample(lugares, 2)
        if not G.has_edge(a, b):
            peso = random.randint(1, 10)
            G.add_edge(a, b, weight=peso)

    return G

# Función para mostrar el mapa con fondo de pergamino
def mostrar_mapa(G):
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 8))

    fig.patch.set_facecolor('#f3e5ab')  # fondo estilo papiro
    ax.set_facecolor('#f3e5ab')

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='#ffe4b5',
            font_size=10, font_weight='bold', ax=ax)
    
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='brown', ax=ax)

    plt.title("🌍 Mapa de Mundo Ficticio con Grafos 🌄", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.show()

# Menú de interacción
def menu():
    while True:
        print("\n=== Generador de Mapas Ficticios con Grafos ===")
        print("1. Generar nuevo mapa")
        print("2. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            G = generar_mapa()
            mostrar_mapa(G)
        elif opcion == "2":
            print("¡Hasta pronto, aventurero!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")

# Ejecutar el menú principal
if __name__ == "__main__":
    menu()
