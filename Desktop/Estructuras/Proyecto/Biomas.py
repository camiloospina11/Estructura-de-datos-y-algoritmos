import networkx as nx
import matplotlib.pyplot as plt
import random

# Generar nombres de lugares ficticios
def generar_lugares():
    return [
        "Bosque Sombrío", "Castillo del Eco", "Aldea del Viento", "Cueva del Trueno",
        "Montaña de Cristal", "Llanura Dorada", "Río de la Luna", "Ruinas del Olvido",
        "Templo de Fuego", "Isla Perdida"
    ]

# Crear el grafo con nodos, biomas y conexiones
def generar_mapa():
    lugares = generar_lugares()
    biomas = ["bosque", "fuego", "hielo", "agua", "montaña", "desierto"]
    G = nx.Graph()

    for lugar in lugares:
        bioma = random.choice(biomas)
        G.add_node(lugar)
        G.nodes[lugar]['bioma'] = bioma  # Asignar bioma correctamente

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

# Mostrar el mapa con colores de bioma
def mostrar_mapa(G):
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#f3e5ab')
    ax.set_facecolor('#f3e5ab')

    colores_bioma = {
        "bosque": "#228B22",    # verde bosque
        "fuego": "#B22222",     # rojo fuego
        "hielo": "#ADD8E6",     # azul hielo
        "agua": "#1E90FF",      # azul agua
        "montaña": "#A9A9A9",   # gris
        "desierto": "#EDC9AF"   # arena
    }

    nodos = list(G.nodes())
    colores_nodos = []

    # Confirmamos y coloreamos según el bioma
    for n in nodos:
        bioma = G.nodes[n].get("bioma", "bosque")
        color = colores_bioma.get(bioma, "#fffffH")
        colores_nodos.append(color)
        print(f"{n} → {bioma} → {color}")  # Verificación en consola

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=colores_nodos,
            font_size=10, font_weight='bold', ax=ax)

    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, font_color='brown', ax=ax)

    plt.title("🌍 Mapa de Mundo Ficticio con Biomas 🌄", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.show()

# Menú interactivo
def menu():
    while True:
        print("\n=== Generador de Mapas Ficticios con Biomas ===")
        print("1. Generar nuevo mapa")
        print("2. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            G = generar_mapa()
            mostrar_mapa(G)
        elif opcion == "2":
            print("¡Hasta la próxima exploración!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()
