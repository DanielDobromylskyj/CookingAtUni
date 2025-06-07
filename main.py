from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

import loader

DataLoader = loader.Loader()
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
        layout = BoxLayout(orientation='vertical', padding=20)
        label = Label(text="Welcome to UniCooking!", font_size=32)
        btn = Button(text="Go Back to Loading", size_hint=(1, 0.2))
        btn.bind(on_press=lambda *a: setattr(self.manager, 'current', 'loading'))
        layout.add_widget(label)
        layout.add_widget(btn)
        self.add_widget(layout)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoadingScreen(name='loading'))
        sm.add_widget(RecipeSelector(name='recipie_selector'))
        sm.current = 'loading'  # start here
        return sm

if __name__ == '__main__':
    MyApp().run()
