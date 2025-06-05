from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

# Set background to dark grey (but lighter than pure black)
Window.clearcolor = (0.15, 0.15, 0.15, 1)



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


class MainLayout(BoxLayout):
    selected_item = StringProperty("Select an item")
    button_enabled = BooleanProperty(False)
    search_text = StringProperty("")
    filters = ListProperty([True, True])  # Two example filter flags

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = [f"Item {i}" for i in range(30)]

    def on_item_click(self, item_name, is_enabled):
        self.selected_item = f"You clicked on: {item_name}"
        self.button_enabled = is_enabled

    def get_filtered_items(self):
        return [
            item for i, item in enumerate(self.items)
            if self.search_text.lower() in item.lower()
            and (self.filters[0] if i % 2 == 0 else self.filters[1])
        ]


class MyApp(App):
    def build(self):
        root = MainLayout(orientation='vertical', padding=10, spacing=10)

        # Top bar
        top_bar = BoxLayout(size_hint_y=0.1, padding=5, spacing=10)
        top_bar.add_widget(Button(text="Config", size_hint_x=0.2))
        title = Label(text="[b][size=24]UniCooking[/size][/b]", markup=True, halign="center")
        title.bind(size=title.setter('text_size'))
        top_bar.add_widget(title)
        top_bar.add_widget(Button(text="Stock", size_hint_x=0.3))
        root.add_widget(top_bar)

        # Body
        body = BoxLayout(spacing=10)

        # Left Panel
        left_panel = RoundedBox(orientation='vertical', size_hint_x=0.4, padding=10, spacing=10)

        # Header
        left_panel.add_widget(Label(text="My Recipies", size_hint_y=None, height=30))

        # Search bar
        search_input = TextInput(hint_text="Search...", size_hint_y=None, height=35)
        left_panel.add_widget(search_input)

        def update_search_text(instance, value):
            root.search_text = value
            refresh_item_list()

        search_input.bind(text=update_search_text)

        # Filter checkboxes
        filter_box = BoxLayout(size_hint_y=None, height=40, spacing=0)
        filter_box.add_widget(Label(text="Can Make:", size_hint_x=0))
        can_make_filter = CheckBox(active=True)
        filter_box.add_widget(can_make_filter)

        left_panel.add_widget(filter_box)

        def on_filter_change(instance, value):
            root.filters = [can_make_filter.active]
            refresh_item_list()

        can_make_filter.bind(active=on_filter_change)

        # Scrollable item list
        scroll = ScrollView()
        item_list = GridLayout(cols=1, size_hint_y=None, spacing=5)
        item_list.bind(minimum_height=item_list.setter('height'))
        scroll.add_widget(item_list)
        left_panel.add_widget(scroll)

        # Populate and refresh
        def refresh_item_list():
            item_list.clear_widgets()
            for j, item in enumerate(root.get_filtered_items()):
                btn = Button(
                    text=item,
                    size_hint_y=None,
                    height=40,
                    background_normal='',
                    background_color=(0.3, 0.3, 0.3, 1),
                    border=(16, 16, 16, 16)
                )
                btn.bind(on_press=lambda btn, i=j: root.on_item_click(item, i % 2 == 0))
                item_list.add_widget(btn)

        refresh_item_list()
        body.add_widget(left_panel)

        # Right Panel
        right_panel = RoundedBox(orientation='vertical', padding=15, spacing=10)

        subtitle = Label(text="Sub Title Here", size_hint_y=None, height=25, halign='left', valign='bottom')
        subtitle.bind(size=subtitle.setter('text_size'))
        description = Label(text="Description", halign='left', valign='top', size_hint_y=None, height=30)
        description.bind(size=description.setter('text_size'))
        misc_info = Label(text="Misc Information", halign='left', valign='top', size_hint_y=None, height=30)
        misc_info.bind(size=misc_info.setter('text_size'))
        selected_label = Label(text="Select an item", halign='left', valign='top')
        selected_label.bind(size=selected_label.setter('text_size'))
        root.bind(selected_item=selected_label.setter('text'))

        make_btn = Button(text="Make", size_hint_y=None, height=50, border=(16, 16, 16, 16))
        make_btn.disabled = True
        root.bind(button_enabled=lambda inst, val: setattr(make_btn, 'disabled', not val))

        right_panel.add_widget(subtitle)
        right_panel.add_widget(description)
        right_panel.add_widget(misc_info)
        right_panel.add_widget(selected_label)
        right_panel.add_widget(Label(text="The make button should be active/inactive depending on a flag."))
        right_panel.add_widget(make_btn)

        body.add_widget(right_panel)
        root.add_widget(body)

        return root


if __name__ == '__main__':
    MyApp().run()
