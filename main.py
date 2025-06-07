from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '802')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty

Window.clearcolor = (0.15, 0.15, 0.15, 1)
Window.title = "UniCooking"

import loader

class ColoredBox(BoxLayout):
    background_color = ListProperty([0.2, 0.2, 0.2, 1])

    def __init__(self, background_color=None, **kwargs):
        if background_color:
            self.background_color = background_color
        super().__init__(**kwargs)

        with self.canvas.before:
            self.bg_color = Color(*self.background_color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)
        self.bind(background_color=self._update_color)

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _update_color(self, *args):
        self.bg_color.rgba = self.background_color

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = (20, 10)  # (horizontal, vertical) padding

        with self.canvas.before:
            Color(0.3, 0.3, 0.3, 1)  # Button background color (dark gray)
            self.rect = RoundedRectangle(radius=[15], pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class RoundedBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.25, 0.25, 0.25, 1)  # Lighter dark gray
            self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

DataLoader = loader.Loader({"stock": "ingredients.db", "recipes": "recipes.json"})

class LoadingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.status_label = Label(text='Loading...', font_size=24)
        layout.add_widget(self.status_label)
        self.add_widget(layout)

        DataLoader.load()
        Clock.schedule_interval(self.update_status, 0.1)

    def update_status(self, dt):
        if DataLoader.has_loaded is False:
            self.status_label.text = DataLoader.update_text()
        else:
            self.manager.current = 'recipie_selector'
            return False  # stop the Clock


class RecipeSelector(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = BoxLayout(orientation='vertical')

        # Title / Top Bar
        top_bar = ColoredBox(height=40, size_hint_y=None, padding=5, spacing=10)
        title = Label(
            text="[b][size=24]UniCooking[/size][/b]",
            markup=True,
            halign="center",
            valign="middle"
        )
        title.bind(size=title.setter('text_size'))
        top_bar.add_widget(title)

        top_bar.add_widget(Button(text="Stock", size_hint_x=0.3, size_hint_y=None, height=30))
        top_bar.add_widget(Button(text="Config", size_hint_x=0.3, size_hint_y=None, height=30))
        self.main_layout.add_widget(top_bar)

        # Spacer
        self.main_layout.add_widget(ColoredBox(background_color=[0.05, 0.05, 0.05, 1], size_hint_y=0.001))

        # Search Area
        search_bar = ColoredBox(height=40, size_hint_y=None, padding=5, spacing=10)
        search_input = TextInput(
            hint_text="Search...",
            size_hint_y=1,
            multiline=False,
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1)
        )
        search_bar.add_widget(search_input)
        self.main_layout.add_widget(search_bar)

        filter_bar = ColoredBox(height=30, orientation='horizontal', size_hint_y=None, padding=(0, 5), spacing=10)

        checkbox = CheckBox(size_hint_x=None, width=30, active=True)
        label = Label(
            text="Gluten Free",
            halign='left',
            valign='middle',
            size_hint_x=None,
            width=150  # You can adjust this to fit your text
        )
        label.bind(size=label.setter('text_size'))

        filter_bar.add_widget(checkbox)
        filter_bar.add_widget(label)

        self.main_layout.add_widget(filter_bar)

        self.results_container = BoxLayout(size_hint_y=0.3, orientation='vertical')

        self.scroll = ScrollView()
        self.results_grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.results_grid.bind(minimum_height=self.results_grid.setter('height'))

        self.scroll.add_widget(self.results_grid)
        self.results_container.add_widget(self.scroll)
        self.main_layout.add_widget(self.results_container)

        # Example: populate with dummy data
        self.populate_results(["Apple Pie", "Banana Bread", "Chocolate Cake"])

    def populate_results(self, items):
        self.results_grid.clear_widgets()
        for item in items:
            btn = RoundedButton(text=item, size_hint_y=None, height=40)
            # You can bind on_press here to handle clicks
            self.results_grid.add_widget(btn)

        # Add the full layout to the screen
        self.add_widget(self.main_layout)


class MyApp(App):
    name = "UniCooking"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "UniCooking"

        DataLoader.set_local_path(self)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(RecipeSelector(name='recipie_selector'))
        sm.current = 'loading'  # start here
        return sm

if __name__ == '__main__':
    MyApp().run()
