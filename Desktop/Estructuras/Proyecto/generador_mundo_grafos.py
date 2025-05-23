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

# Función para crear un grafo de mundo ficticio con biomas
def generar_mapa():
    lugares = generar_lugares()
    biomas = ["bosque", "fuego", "hielo", "agua", "montaña", "desierto"]
    G = nx.Graph()

    for lugar in lugares:
        bioma = random.choice(biomas)
        G.add_node(lugar, bioma=bioma)

    conectados = [lugares[0]]
    no_conectados = lugares[1:]

    while no_conectados:
        a = random.choice(conectados)
        b = random.choice(no_conectados)
        peso = random.randint(1, 10)
        G.add_edge(a, b, weight=peso)
        conectados.append(b)
        no_conectados.remove(b)

    for _ in range(5):
        a, b = random.sample(lugares, 2)
        if not G.has_edge(a, b):
            peso = random.randint(1, 10)
            G.add_edge(a, b, weight=peso)

    return G

# Función para mostrar el mapa gráficamente con fondo tipo papiro y colores por bioma
def mostrar_mapa(G):
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 8))

    # Fondo estilo papiro
    fig.patch.set_facecolor('#f3e5ab')
    ax.set_facecolor('#f3e5ab')

    # Colores por bioma
    colores_bioma = {
        "bosque": "#228B22",
        "fuego": "#B22222",
        "hielo": "#ADD8E6",
        "agua": "#1E90FF",
        "montaña": "#A9A9A9",
        "desierto": "#EDC9AF"
    }

    nodos = G.nodes()
    colores_nodos = [colores_bioma[G.nodes[n]["bioma"]] for n in nodos]

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=colores_nodos,
            font_size=10, font_weight='bold', ax=ax)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='brown', ax=ax)

    plt.title("🌍 Mapa de Mundo Ficticio con Biomas 🌄", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.show()

# Menú principal
def menu():
    while True:
        print("\n=== Generador de Mapas Ficticios con Grafos ===")
        print("1. Generar nuevo mapa con biomas")
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

# Ejecutar menú
if __name__ == "__main__":
    menu()
