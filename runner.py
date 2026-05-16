from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.animation import Animation

class Runner(BoxLayout):
    value = NumericProperty(0)
    finished = BooleanProperty(False)
    def __init__(self, total, steptime, **kwargs):
        super().__init__(**kwargs)
        self.total = total
        self.animation = (Animation(pos_hint = {'top': 0.1}, duration = steptime/2)) + Animation(pos_hint = {'top': 1.0}, duration = steptime/2)
        self.btn = Button(text = 'Приседание', pos_hint = {'top': 1.0}, size_hint = (1, 0.1))
        self.add_widget(self.btn)
        self.animation.on_progress = self.next
    def start(self):
        self.value = 0
        self.finished = False
        self.animation.repeat = True
        self.animation.start(self.btn)

    def next(self, widget, step):
        if step == 1.0:
            self.value += 1
            if self.value >= self.total:
                self.animation.repeat = False
                self.finished = True



