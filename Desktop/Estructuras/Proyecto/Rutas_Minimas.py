import sys
import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import random

# Posiciones fijas en el mapa
POSICIONES = {
    "Bosque Sombrío": (0, 3),
    "Castillo del Eco": (2, 4),
    "Montaña de Cristal": (2, 5),
    "Cueva del Trueno": (0, 1.2),
    "Templo de Fuego": (3, 2),
    "Llanura Dorada": (4, 1),
    "Aldea del Viento": (4, 4),
    "Río de la Luna": (4, 0),
    "Ruinas del Olvido": (0, -0.5),
    "Isla Perdida": (6, 5)
}

COLORES_BIOMA = {
    "bosque": "#228B22",
    "fuego": "#B22222",
    "hielo": "#ADD8E6",
    "agua": "#1E90FF",
    "montaña": "#A9A9A9",
    "desierto": "#EDC9AF"
}

ICONOS_BIOMA = {
    "bosque": "images/Arbol.png",
    "fuego": "images/Fuego.png",
    "hielo": "images/Hielo.png",
    "agua": "images/Agua.png",
    "montaña": "images/Montaña.png",
    "desierto": "images/Desierto.png"
}

CONEXIONES_FIJAS = [
    ("Bosque Sombrío", "Castillo del Eco"),
    ("Castillo del Eco", "Montaña de Cristal"),
    ("Montaña de Cristal", "Isla Perdida"),
    ("Isla Perdida", "Aldea del Viento"),
    ("Aldea del Viento", "Llanura Dorada"),
    ("Llanura Dorada", "Río de la Luna"),
    ("Río de la Luna", "Templo de Fuego"),
    ("Templo de Fuego", "Cueva del Trueno"),
    ("Cueva del Trueno", "Ruinas del Olvido"),
    ("Ruinas del Olvido", "Bosque Sombrío")
]

class MapaCanvas(FigureCanvas):
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        super().__init__(self.fig)

    def dibujar_mapa(self, G):
        self.ax.clear()
        self.fig.patch.set_facecolor('#f3e5ab')
        self.ax.set_facecolor('#f3e5ab')

        nx.draw_networkx_edges(G, POSICIONES, ax=self.ax)

        etiquetas = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, POSICIONES, edge_labels=etiquetas, font_color='brown', ax=self.ax)

        for nodo, (x, y) in POSICIONES.items():
            bioma = G.nodes[nodo].get('bioma', 'bosque').lower()
            path = ICONOS_BIOMA.get(bioma)
            print(f"Nodo: {nodo}, Bioma: {bioma}, Ruta: {path}")
            if path and os.path.exists(path):
                try:
                    img = mpimg.imread(path)
                    im = OffsetImage(img, zoom=0.45)
                    ab = AnnotationBbox(im, (x, y), frameon=False)
                    self.ax.add_artist(ab)
                except Exception as e:
                    print(f"Error cargando imagen para {nodo}: {e}")
            else:
                print(f"⚠️ Imagen no encontrada para bioma '{bioma}': {path}")

            self.ax.text(x, y - 0.4, nodo, ha='center', fontsize=9, fontweight='bold')

        self.ax.set_title("🌍 Mapa de Mundo Ficticio", fontsize=16, fontweight='bold')
        self.ax.axis('off')
        self.draw()

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generador de Mundo Ficticio con Grafos")

        self.canvas = MapaCanvas()
        self.boton_generar = QPushButton("Ver Mapa")
        self.boton_generar.clicked.connect(self.ver_mapa)

        self.G = None

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.boton_generar)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

    def ver_mapa(self):
        if self.G is None:
            self.G = nx.Graph()
            biomas = list(COLORES_BIOMA.keys())

            for lugar in POSICIONES:
                self.G.add_node(lugar)
                self.G.nodes[lugar]['bioma'] = random.choice(biomas)

            for a, b in CONEXIONES_FIJAS:
                if not self.G.has_edge(a, b):
                    self.G.add_edge(a, b, weight=random.randint(1, 10))

        self.canvas.dibujar_mapa(self.G)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
