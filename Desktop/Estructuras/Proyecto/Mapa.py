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
from kivy.core.audio import SoundLoader
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

HERMANO_POSICION = "Templo de Fuego"

class MapaWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.jugador_posicion = "Bosque Sombrío"
        self.destino_ruta = None
        self.ruta_encontrada = []
        self.animaciones_anteriores = []
        self.lineas_ruta = []
        self.hermano_opacidad = 1
        self.hermano_parpadeo_event = None
        Clock.schedule_once(self.mostrar_pantalla_inicio, 0.5)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def mostrar_pantalla_inicio(self, dt):
        layout = FloatLayout()

        with layout.canvas.before:
            Color(1, 1, 1, 1)
            bg = Rectangle(source='images/titulo_inicio.png', pos=layout.pos, size=Window.size)
            layout.bind(pos=lambda *a: setattr(bg, 'pos', layout.pos))
            layout.bind(size=lambda *a: setattr(bg, 'size', layout.size))

        boton = Button(
            text="Continuar",
            size_hint=(None, None),
            size=(160, 50),
            pos_hint={"center_x": 0.5, "y": 0.1}
        )

        layout.add_widget(boton)

        popup = Popup(
            title="",
            content=layout,
            size_hint=(1, 1),
            auto_dismiss=False
        )

        boton.bind(on_press=lambda *a: (popup.dismiss(), self.mostrar_historia(0)))
        popup.open()

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

        self.hermano_sound = SoundLoader.load('sonido/encontrado.mp3')
        if self.hermano_sound:
            self.hermano_sound.volume = 1

        self.bg_music = SoundLoader.load('sonido/sound.wav')
        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.play()

        with self.canvas.before:
            self.bg = Rectangle(source='images/mapa_papiro.png', pos=self.pos, size=Window.size)
            self.bind(pos=self.update_bg, size=self.update_bg)

    def mostrar_popup_hermano_encontrado(self):
        layout = FloatLayout()

        with layout.canvas.before:
            Color(1, 1, 1, 1)
            bg = Rectangle(source='images/mapa_papiro.png', pos=layout.pos, size=(600, 400))
            layout.bind(pos=lambda *a: setattr(bg, 'pos', layout.pos))
            layout.bind(size=lambda *a: setattr(bg, 'size', layout.size))

        hermano_img = Image(source="images/Hermano.png", size_hint=(None, None), size=(100, 100), pos_hint={"center_x": 0.5, "center_y": 0.65})
        layout.add_widget(hermano_img)

        label = Label(
            text="¡Has encontrado a tu hermano perdido en el Templo de Fuego!",
            size_hint=(0.9, 0.3),
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1),
            font_size=16,
            font_name="fonts/MedievalSharp.ttf"
        )
        label.bind(size=label.setter('text_size'))
        layout.add_widget(label)

        btn_cerrar = Button(
            text="Aceptar",
            size_hint=(None, None),
            size=(100, 40),
            pos_hint={"center_x": 0.5, "y": 0.05}
        )

        popup = Popup(
            title="¡Hermano encontrado!",
            content=layout,
            size_hint=(None, None),
            size=(600, 400),
            auto_dismiss=False
        )

        def cerrar_popup(instancia):
            popup.dismiss()
            if self.bg_music:
                self.bg_music.play()



        btn_cerrar.bind(on_press=popup.dismiss)
        layout.add_widget(btn_cerrar)

        if self.bg_music:
            self.bg_music.stop()


        popup.open()



    def mostrar_historia(self, dt):
        layout = FloatLayout()

        with layout.canvas.before:
            Color(1, 1, 1, 1)
            self.historia_bg = Rectangle(source='images/mapa_papiro.png', pos=layout.pos, size=(700, 400))
            layout.bind(pos=lambda *args: setattr(self.historia_bg, 'pos', layout.pos))
            layout.bind(size=lambda *args: setattr(self.historia_bg, 'size', layout.size))

        texto = """Hace años, en la vasta región de Eldoria, vivían dos hermanos inseparables. Una noche,
                una tormenta mágica separó sus destinos. Tú, el hermano mayor, despiertas solo
                en el Bosque Sombrío. Tu misión: recorrer el reino y encontrar a tu hermano perdido,
                a quien se vio por última vez en el Templo de Fuego."""

        label = Label(
            text=texto,
            size_hint=(0.9, 0.7),
            pos_hint={"center_x": 0.5, "center_y": 0.55},
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1),
            font_size=22,
            font_name="fonts/MedievalSharp.ttf"
        )
        label.bind(size=label.setter('text_size'))
        layout.add_widget(label)

        btn_iniciar = Button(
            text="Iniciar Aventura",
            size_hint=(None, None),
            size=(160, 50),
            pos_hint={"center_x": 0.5, "y": 0.05}
        )
        layout.add_widget(btn_iniciar)

        popup = Popup(
            title="El Comienzo",
            content=layout,
            size_hint=(1, 1),
            auto_dismiss=False
        )
        btn_iniciar.bind(on_press=lambda *args: (popup.dismiss(), self.ver_mapa(None)))
        popup.open()

    # Las funciones faltantes como ver_mapa, mover_jugador, calcular_ruta_minima, mostrar_popup se integrarán aquí.

    def ver_mapa(self, instance):
        self.clear_widgets()
        self.update_bg()

        for animacion in getattr(self, 'animaciones_anteriores', []):
            self.canvas.remove(animacion)
        self.animaciones_anteriores.clear()

        for linea in getattr(self, 'lineas_ruta', []):
            self.canvas.remove(linea)
        self.lineas_ruta.clear()

        boton = Button(text="Ver Mapa", size_hint=(None, None), size=(150, 50), pos_hint={"center_x": 0.5, "y": 0.9})
        boton.bind(on_press=self.ver_mapa)
        self.add_widget(boton)

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
                with self.canvas:
                    Color(1, 1, 0, 1)
                    circulo = Line(circle=(x * Window.width + 32, y * Window.height + 32, 40), width=2)
                    self.animaciones_anteriores.append(circulo)
            if lugar == HERMANO_POSICION:
                self.hermano_img = Image(source="images/Hermano.png", size_hint=(None, None), size=(32, 32), pos_hint={"x": x + 0.03, "y": y + 0.03}, opacity=self.hermano_opacidad)
                self.add_widget(self.hermano_img)
                if self.hermano_parpadeo_event:
                    self.hermano_parpadeo_event.cancel()
                self.hermano_parpadeo_event = Clock.schedule_interval(self.animar_hermano, 0.6)

        spinner = Spinner(
            text='Mover a...',
            values=sorted(
                [b for a, b in self.CONEXIONES if a == self.jugador_posicion] +
                [a for a, b in self.CONEXIONES if b == self.jugador_posicion]
            ),
            size_hint=(None, None),
            size=(150, 44),
            pos_hint={'x': 0.82, 'y': 0.05}
        )
        spinner.bind(text=self.mover_jugador)
        self.add_widget(spinner)

        self.spinner_destino = Spinner(
            text='Destino',
            values=sorted([lugar for lugar in POSICIONES.keys() if lugar != self.jugador_posicion]),
            size_hint=(None, None),
            size=(150, 44),
            pos_hint={'x': 0.82, 'y': 0.13}
        )
        self.add_widget(self.spinner_destino)

        btn_ruta_min = Button(
            text="Ruta más corta",
            size_hint=(None, None),
            size=(150, 44),
            pos_hint={"x": 0.82, "y": 0.21}
        )
        btn_ruta_min.bind(on_press=self.calcular_ruta_minima)
        self.add_widget(btn_ruta_min)

    def animar_hermano(self, dt):
        if self.hermano_img:
            self.hermano_opacidad = 1 if self.hermano_opacidad == 0 else 0
            self.hermano_img.opacity = self.hermano_opacidad

    def mover_jugador(self, spinner, destino):
        self.jugador_posicion = destino
        if destino == HERMANO_POSICION:
            if self.hermano_sound:
                self.hermano_sound.play()
            self.mostrar_popup_hermano_encontrado()

        else:
            self.mostrar_popup("Sin pistas", f"Tu hermano no está aquí. Tal vez deberías seguir buscando...", cerrar=True)
        self.ver_mapa(None)

    def calcular_ruta_minima(self, instance):
        origen = self.jugador_posicion
        destino = self.spinner_destino.text

        if origen == destino:
            self.mostrar_popup("Destino inválido", "Selecciona un destino distinto a tu posición actual.", botones=True)
            return

        visitados = set()
        cola = deque([(origen, [origen])])

        while cola:
            actual, camino = cola.popleft()
            if actual == destino:
                break
            for a, b in self.CONEXIONES:
                vecino = None
                if a == actual:
                    vecino = b
                elif b == actual:
                    vecino = a
                if vecino and vecino not in visitados:
                    visitados.add(vecino)
                    cola.append((vecino, camino + [vecino]))
        else:
            self.mostrar_popup("Ruta no encontrada", "No se encontró una ruta disponible.", botones=True)
            return

        self.destino_ruta = destino
        self.ruta_encontrada = camino

        for linea in self.lineas_ruta:
            self.canvas.remove(linea)
        self.lineas_ruta.clear()

        with self.canvas:
            Color(1, 0, 0, 1)
            for i in range(len(camino) - 1):
                x1, y1 = POSICIONES[camino[i]]
                x2, y2 = POSICIONES[camino[i + 1]]
                linea = Line(points=[
                    x1 * Window.width + 32, y1 * Window.height + 32,
                    x2 * Window.width + 32, y2 * Window.height + 32
                ], width=2)
                self.lineas_ruta.append(linea)

        ruta_str = " ➜ ".join(camino)
        self.mostrar_popup("Ruta más corta", f"Ruta más corta:\n{ruta_str}", botones=True)

    def mostrar_popup(self, titulo, mensaje, botones=False, cerrar=False):
        layout = FloatLayout()

        with layout.canvas.before:
            Color(1, 1, 1, 1)
            bg = Rectangle(source='images/mapa_papiro.png', pos=layout.pos, size=(600, 300))
            layout.bind(pos=lambda *a: setattr(bg, 'pos', layout.pos))
            layout.bind(size=lambda *a: setattr(bg, 'size', layout.size))

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

        popup = Popup(
            title=titulo,
            content=layout,
            size_hint=(None, None),
            size=(600, 300),
            auto_dismiss=False
        )

        if botones or cerrar:
            btn_aceptar = Button(
                text="Aceptar",
                size_hint=(None, None),
                size=(100, 40),
                pos_hint={"x": 0.25, "y": 0.05}
            )
            btn_aceptar.bind(on_press=popup.dismiss)
            layout.add_widget(btn_aceptar)

        if botones and hasattr(self, 'ruta_encontrada') and self.ruta_encontrada:
            btn_seguir = Button(
                text="Seguir ruta",
                size_hint=(None, None),
                size=(120, 40),
                pos_hint={"x": 0.55, "y": 0.05}
            )

            def seguir_ruta(inst):
                popup.dismiss()
                camino_iter = iter(self.ruta_encontrada[1:])

                def mover_paso_a_paso(dt):
                    try:
                        siguiente = next(camino_iter)
                        self.jugador_posicion = siguiente
                        self.ver_mapa(None)
                        if siguiente == HERMANO_POSICION:
                            if self.hermano_sound:
                                self.hermano_sound.play()
                            self.mostrar_popup_hermano_encontrado()
                            return  # Detiene el avance automático

                        Clock.schedule_once(mover_paso_a_paso, 0.7)
                    except StopIteration:
                        return

                Clock.schedule_once(mover_paso_a_paso, 0.7)

            btn_seguir.bind(on_press=seguir_ruta)
            layout.add_widget(btn_seguir)

        popup.open()

class MundoApp(App):
    def build(self):
        return MapaWidget()

if __name__ == '__main__':
    MundoApp().run()
