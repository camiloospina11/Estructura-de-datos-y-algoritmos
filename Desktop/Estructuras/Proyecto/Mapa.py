from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color

# Tamaño de la ventana
Window.size = (900, 600)

# Posiciones fijas (x, y) en porcentaje relativo para Kivy
POSICIONES = {
    "Bosque Sombrío": (0.05, 0.55),
    "Castillo del Eco": (0.25, 0.65),
    "Montaña de Cristal": (0.25, 0.80),
    "Cueva del Trueno": (0.05, 0.25),
    "Templo de Fuego": (0.4, 0.4),
    "Llanura Dorada": (0.6, 0.25),
    "Aldea del Viento": (0.6, 0.65),
    "Río de la Luna": (0.6, 0.1),
    "Ruinas del Olvido": (0.05, 0.05),
    "Isla Perdida": (0.85, 0.8)
}

ICONOS_BIOMA = {
    "bosque": "images/Arbol.png",
    "fuego": "images/Fuego.png",
    "hielo": "images/Hielo.png",
    "agua": "images/Agua.png",
    "montaña": "images/Montaña.png",
    "desierto": "images/Desierto.png"
}

import random

class MapaWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            self.bg = Rectangle(source='images/mapa_papiro.png', pos=self.pos, size=Window.size)
            self.bind(pos=self.update_bg, size=self.update_bg)

        boton = Button(text="Ver Mapa", size_hint=(None, None), size=(150, 50), pos_hint={"center_x": 0.5, "y": 0.9})
        boton.bind(on_press=self.ver_mapa)
        self.add_widget(boton)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def ver_mapa(self, instance):
        CONEXIONES = [
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
        jugador_posicion = "Bosque Sombrío"  # Nodo inicial del jugador
        self.clear_widgets()
        self.update_bg()

        with self.canvas:
            Color(0, 0, 0, 1)
            for origen, destino in CONEXIONES:
                x1, y1 = POSICIONES[origen]
                x2, y2 = POSICIONES[destino]
                x1_abs = x1 * Window.width
                y1_abs = y1 * Window.height
                x2_abs = x2 * Window.width
                y2_abs = y2 * Window.height
                from kivy.graphics import Line
                Line(points=[x1_abs + 32, y1_abs + 32, x2_abs + 32, y2_abs + 32], width=1.5)

        # Volver a colocar el botón
        boton = Button(text="Ver Mapa", size_hint=(None, None), size=(150, 50), pos_hint={"center_x": 0.5, "y": 0.9})
        boton.bind(on_press=self.ver_mapa)
        self.add_widget(boton)

        BIOMAS_FIJOS = {
    "Bosque Sombrío": "bosque",
    "Castillo del Eco": "desierto",
    "Montaña de Cristal": "montaña",
    "Cueva del Trueno": "fuego",
    "Templo de Fuego": "fuego",
    "Llanura Dorada": "hielo",
    "Aldea del Viento": "bosque",
    "Río de la Luna": "agua",
    "Ruinas del Olvido": "montaña",
    "Isla Perdida": "agua"
}

        for lugar, (x, y) in POSICIONES.items():
            bioma = BIOMAS_FIJOS.get(lugar, "bosque")
            ruta_icono = ICONOS_BIOMA.get(bioma, "images/Arbol.png")

            imagen = Image(source=ruta_icono, size_hint=(None, None), size=(64, 64), pos_hint={"x": x, "y": y})
            self.add_widget(imagen)

            etiqueta = Label(text=lugar, size_hint=(None, None), size=(120, 20), pos_hint={"x": x, "y": y - 0.05})
            self.add_widget(etiqueta)

            # Mostrar ícono del jugador si es la posición actual
            if lugar == jugador_posicion:
                icono_jugador = Image(source="images/Jugador.png", size_hint=(None, None), size=(32, 32), pos_hint={"x": x + 0.02, "y": y + 0.05})
                self.add_widget(icono_jugador)

class MundoApp(App):
    def build(self):
        return MapaWidget()

if __name__ == '__main__':
    MundoApp().run()
