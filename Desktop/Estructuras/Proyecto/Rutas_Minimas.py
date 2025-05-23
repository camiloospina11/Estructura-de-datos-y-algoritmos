import networkx as nx
import matplotlib.pyplot as plt
import random

def generar_lugares():
    return [
        "Bosque Sombrío", "Castillo del Eco", "Aldea del Viento", "Cueva del Trueno",
        "Montaña de Cristal", "Llanura Dorada", "Río de la Luna", "Ruinas del Olvido",
        "Templo de Fuego", "Isla Perdida"
    ]

def generar_mapa():
    lugares = generar_lugares()
    biomas = ["bosque", "fuego", "hielo", "agua", "montaña", "desierto"]
    G = nx.Graph()

    for lugar in lugares:
        bioma = random.choice(biomas)
        G.add_node(lugar)
        G.nodes[lugar]['bioma'] = bioma

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

def mostrar_mapa(G):
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#f3e5ab')
    ax.set_facecolor('#f3e5ab')

    colores_bioma = {
        "bosque": "#228B22", "fuego": "#B22222", "hielo": "#ADD8E6",
        "agua": "#1E90FF", "montaña": "#A9A9A9", "desierto": "#EDC9AF"
    }

    nodos = list(G.nodes())
    colores_nodos = [colores_bioma.get(G.nodes[n].get("bioma", "bosque"), "#ffffff") for n in nodos]

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=colores_nodos,
            font_size=10, font_weight='bold', ax=ax)

    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, font_color='brown', ax=ax)

    plt.title("🌍 Mapa de Mundo Ficticio con Biomas 🌄", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.show()

def mostrar_mapa_con_ruta(G, camino):
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#f3e5ab')
    ax.set_facecolor('#f3e5ab')

    colores_bioma = {
        "bosque": "#228B22", "fuego": "#B22222", "hielo": "#ADD8E6",
        "agua": "#1E90FF", "montaña": "#A9A9A9", "desierto": "#EDC9AF"
    }

    nodos = list(G.nodes())
    colores_nodos = [colores_bioma.get(G.nodes[n].get("bioma", "bosque"), "#ffffff") for n in nodos]

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=colores_nodos,
            font_size=10, font_weight='bold', ax=ax)

    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, font_color='brown', ax=ax)

    edges = list(zip(camino[:-1], camino[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=4, edge_color='crimson', ax=ax)

    plt.title("🧭 Ruta más corta resaltada", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.show()

def narrar_aventura(G, camino):
    print("\n📖 Leyenda del viajero entre tierras antiguas:\n")

    inicio = camino[0]
    destino = camino[-1]
    print(f"Desde la ancestral {inicio}, un viajero parte en busca del mítico {destino}.\n")

    for i in range(len(camino)-1):
        actual = camino[i]
        siguiente = camino[i+1]
        peso = G[actual][siguiente]['weight']
        bioma = G.nodes[siguiente].get("bioma", "tierra desconocida")

        descripcion = {
            "bosque": "un denso bosque encantado 🌲",
            "fuego": "una tierra ardiente plagada de lava y cenizas 🔥",
            "hielo": "una tundra helada donde el tiempo parece congelado ❄️",
            "agua": "pantanos y lagunas de aguas misteriosas 💧",
            "montaña": "colinas escarpadas y niebla espesa ⛰️",
            "desierto": "una llanura seca y agrietada por el sol abrasador 🏜️"
        }.get(bioma, "un paraje inexplorado")

        print(f"Tras cruzar {peso} leguas, el viajero llega a {siguiente}, {descripcion}.")

    print(f"\nFinalmente, al anochecer, alcanza su destino: {destino}.")
    print("Allí lo espera un secreto milenario, guardado por siglos...\n✨ Fin de la travesía ✨\n")

def encontrar_mejor_ruta(G):
    print("\n--- Encontrar ruta más corta entre dos lugares ---")
    nodos = list(G.nodes())
    for i, n in enumerate(nodos):
        print(f"{i+1}. {n}")
    try:
        origen = int(input("Selecciona el número del nodo de origen: ")) - 1
        destino = int(input("Selecciona el número del nodo de destino: ")) - 1
        if origen == destino:
            print("¡El origen y el destino son iguales!")
            return

        camino = nx.dijkstra_path(G, nodos[origen], nodos[destino], weight='weight')
        print("Ruta más corta:", " → ".join(camino))
        mostrar_mapa_con_ruta(G, camino)
        narrar_aventura(G, camino)
    except Exception as e:
        print("Error:", e)

def menu():
    G = None
    while True:
        print("\n=== Generador de Mapas Ficticios con Grafos ===")
        print("1. Generar nuevo mapa")
        print("2. Mostrar mejor ruta (Dijkstra)")
        print("3. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            G = generar_mapa()
            mostrar_mapa(G)
        elif opcion == "2":
            if G is None:
                print("Primero genera un mapa (opción 1).")
            else:
                encontrar_mejor_ruta(G)
        elif opcion == "3":
            print("¡Hasta la próxima exploración!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()
