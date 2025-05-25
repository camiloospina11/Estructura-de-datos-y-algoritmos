from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color, Line, InstructionGroup
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.clock import Clock
from collections import deque

Window.size = (900, 600)

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

class MapaWidget(FloatLayout):
    def __init__(self, **kwargs):
        self.jugador_posicion = "Bosque Sombrío"
        self.destino_ruta = None
        self.animaciones_anteriores = []
        self.CONEXIONES = [
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
        self.clear_widgets()
        self.update_bg()

        # Borrar animaciones anteriores
        for animacion in self.animaciones_anteriores:
            self.canvas.remove(animacion)
        self.animaciones_anteriores.clear()

        with self.canvas:
            Color(0, 0, 0, 1)
            for origen, destino in self.CONEXIONES:
                x1, y1 = POSICIONES[origen]
                x2, y2 = POSICIONES[destino]
                x1_abs = x1 * Window.width
                y1_abs = y1 * Window.height
                x2_abs = x2 * Window.width
                y2_abs = y2 * Window.height
                Line(points=[x1_abs + 32, y1_abs + 32, x2_abs + 32, y2_abs + 32], width=1.5)

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
            self.add_widget(Image(source=ruta_icono, size_hint=(None, None), size=(64, 64), pos_hint={"x": x, "y": y}))
            self.add_widget(Label(text=lugar, size_hint=(None, None), size=(120, 20), pos_hint={"x": x, "y": y - 0.05}))
            if lugar == self.jugador_posicion:
                self.add_widget(Image(source="images/Jugador.png", size_hint=(None, None), size=(32, 32), pos_hint={"x": x + 0.02, "y": y + 0.05}))
            if lugar == self.destino_ruta:
                with self.canvas:
                    Color(1, 1, 0, 1)  # Amarillo
                    circulo = Line(circle=(x * Window.width + 32, y * Window.height + 32, 40), width=2)
                    self.animaciones_anteriores.append(circulo)

        self.spinner_destino = Spinner(
            text='Destino',
            values=sorted([lugar for lugar in POSICIONES.keys() if lugar != self.jugador_posicion]),
            size_hint=(None, None),
            size=(150, 44),
            pos_hint={'x': 0.82, 'y': 0.05}
        )
        self.add_widget(self.spinner_destino)

        btn_ruta_min = Button(
            text="Ruta más corta",
            size_hint=(None, None),
            size=(150, 44),
            pos_hint={"x": 0.82, "y": 0.13}
        )
        btn_ruta_min.bind(on_press=self.calcular_ruta_minima)
        self.add_widget(btn_ruta_min)

        spinner_adyacente = Spinner(
            text='Mover a...',
            values=sorted(
                [b for a, b in self.CONEXIONES if a == self.jugador_posicion] +
                [a for a, b in self.CONEXIONES if b == self.jugador_posicion]
            ),
            size_hint=(None, None),
            size=(150, 44),
            pos_hint={'x': 0.82, 'y': 0.21}
        )
        spinner_adyacente.bind(text=self.mover_jugador)
        self.add_widget(spinner_adyacente)

    def mover_jugador(self, spinner, destino):
        self.jugador_posicion = destino
        self.ver_mapa(None)

    def calcular_ruta_minima(self, instance):
        inicio = self.jugador_posicion
        destino = self.spinner_destino.text.strip()
        self.destino_ruta = destino

        def mostrar_popup_ruta(titulo, mensaje, camino):
            layout = FloatLayout()
            with layout.canvas.before:
                Color(1, 1, 1, 1)
                self.popup_bg = Rectangle(source='images/mapa_papiro.png', pos=layout.pos, size=(600, 300))
                layout.bind(pos=lambda *args: setattr(self.popup_bg, 'pos', layout.pos))
                layout.bind(size=lambda *args: setattr(self.popup_bg, 'size', layout.size))

            label = Label(
                text=mensaje,
                size_hint=(0.9, 0.5),
                pos_hint={"center_x": 0.5, "center_y": 0.6},
                halign='center',
                valign='middle',
                color=(0, 0, 0, 1),
                font_size=16
            )
            label.bind(size=label.setter('text_size'))
            layout.add_widget(label)

            btn_aceptar = Button(
                text="Aceptar",
                size_hint=(None, None),
                size=(100, 40),
                pos_hint={"x": 0.3, "y": 0.05}
            )

            btn_seguir = Button(
                text="Seguir ruta",
                size_hint=(None, None),
                size=(120, 40),
                pos_hint={"x": 0.55, "y": 0.05}
            )

            popup = Popup(
                title=titulo,
                content=layout,
                size_hint=(None, None),
                size=(600, 300),
                auto_dismiss=False
            )

            def seguir_ruta(inst):
                popup.dismiss()
                camino_iter = iter(camino[1:])

                def mover_paso_a_paso(dt):
                    try:
                        siguiente = next(camino_iter)
                        self.jugador_posicion = siguiente
                        self.ver_mapa(None)
                        Clock.schedule_once(mover_paso_a_paso, 0.7)
                    except StopIteration:
                        return

                Clock.schedule_once(mover_paso_a_paso, 0.7)

            btn_aceptar.bind(on_press=popup.dismiss)
            btn_seguir.bind(on_press=seguir_ruta)

            layout.add_widget(btn_aceptar)
            layout.add_widget(btn_seguir)

            popup.open()

        if inicio not in POSICIONES or destino not in POSICIONES or inicio == destino:
            mostrar_popup_ruta("Destino inválido", "Selecciona un destino distinto a tu posición actual.", [])
            return

        visitados = set()
        cola = deque([[inicio]])

        while cola:
            camino = cola.popleft()
            nodo = camino[-1]
            if nodo == destino:
                ruta_texto = " → ".join(camino)

                with self.canvas:
                    Color(1, 0, 0, 1)
                    for i in range(len(camino) - 1):
                        x1, y1 = POSICIONES[camino[i]]
                        x2, y2 = POSICIONES[camino[i + 1]]
                        x1_abs = x1 * Window.width
                        y1_abs = y1 * Window.height
                        x2_abs = x2 * Window.width
                        y2_abs = y2 * Window.height
                        Line(points=[x1_abs + 32, y1_abs + 32, x2_abs + 32, y2_abs + 32], width=2.5)

                mostrar_popup_ruta("Ruta más corta", f"Ruta más corta:\n{ruta_texto}", camino)
                return

            if nodo not in visitados:
                visitados.add(nodo)
                vecinos = [b for a, b in self.CONEXIONES if a == nodo] + [a for a, b in self.CONEXIONES if b == nodo]
                for vecino in vecinos:
                    if vecino not in camino:
                        cola.append(camino + [vecino])

        mostrar_popup_ruta("Sin ruta", "No hay ruta disponible.", [])

class MundoApp(App):
    def build(self):
        return MapaWidget()

if __name__ == '__main__':
    MundoApp().run()

