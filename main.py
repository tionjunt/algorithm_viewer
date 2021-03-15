from kivy.app import App
from kivy.uix.widget import Widget

import heap


class RootWidget(Widget):
    pass


class AlgoApp(App):
    def build(self):
        root = RootWidget()
        return root

if __name__ == "__main__":
    AlgoApp().run()