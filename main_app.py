# программа с двумя экранами
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from instructions import *
from ruffier import test
from seconds import Seconds
from kivy.core.window import Window
from runner import Runner
from sits import Sits
from kivy.uix.image import Image
# Экран (объект класса Screen) - это виджет типа "макет" (Screen - наследник класса RelativeLayout).
# ScreenManager - это особый виджет, который делает видимым один из прописанных в нём экранов.

name = ''
age = 0
p_1 = 0
p_2 = 0
p_3 = 0
pink = (0.87, .54, .8, 1)
Window.clearcolor = pink
btn_color = (.98, 0.31, 0.8)
txt = '[color=#4B0082][b]Введите имя:[/b][/color]'

def check_int(str_num):
    try:
        x = int(str_num)
        return x
    except:
        return False

class Main_screen(Screen):
    def __init__(self, name = 'Main screen'):
        super().__init__(name = name)
        label_1 = Label(text = txt_instruction)
        button_1 = Button(text = 'Начать', size_hint = (0.3, 0.2), pos_hint = {'center_x': 0.5})
        button_1.background_color = btn_color
        button_1.on_press = self.next   
        layout_1 = BoxLayout(size_hint = (0.8, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, height = '30sp')
        layout_2 = BoxLayout(size_hint = (0.8, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, height = '30sp')
        layout_vertical = BoxLayout(orientation = 'vertical', padding = 8, spacing = 8)
        self.ti_1 = TextInput(multiline = False)
        l_1 = Label(text = txt, markup=True)
        self.ti_2 = TextInput(multiline = False)
        l_2 = Label(text = 'Введите возвраст:')
        img = Image(source = 'skebob.jpg')
        layout_1.add_widget(l_1)
        layout_1.add_widget(self.ti_1)
        layout_2.add_widget(l_2)
        layout_2.add_widget(self.ti_2)
        layout_vertical.add_widget(label_1)
        layout_vertical.add_widget(layout_1)
        layout_vertical.add_widget(layout_2)
        layout_vertical.add_widget(button_1)
        layout_vertical.add_widget(img)
        self.add_widget(layout_vertical)

    def next(self):
        global name, age
        name = self.ti_1.text
        age = check_int(self.ti_2.text)
        if age == False or age < 7:
            age = 0
            self.ti_2.text = str(age)
        else:
            self.manager.transition.direction = 'down'
            self.manager.current = 'first'

class FirstScr(Screen):
    def __init__(self, name='first'):
        super().__init__(name=name) # имя экрана должно передаваться конструктору класса Screen
        self.btn = Button(text="Начать")
        self.ti = TextInput(multiline = False)
        l_1 = Label(text = 'Введите результат:')
        self.l_2 = Label(text = txt_test1)
        self.lbl_sec = Seconds(15)
        self.lbl_sec.bind(done = self.sec_finished)
        self.flag = False
        box1 = BoxLayout(size_hint = (0.3, 0.2), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        box1.add_widget(self.btn)
        box2 = BoxLayout(size_hint = (0.9, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, height = '30sp')
        box3 = BoxLayout(orientation = 'vertical', padding = 8, spacing = 8)
        box2.add_widget(l_1)
        box2.add_widget(self.ti)
        box3.add_widget(self.l_2)
        box3.add_widget(self.lbl_sec)
        self.ti.set_disabled(True)
        box3.add_widget(box2)
        box3.add_widget(box1)
        self.btn.on_press = self.next
        self.add_widget(box3)
    def next(self):
        if not self.flag:
            self.btn.set_disabled(True)
            self.lbl_sec.start()
        else:
            p_1 = check_int(self.ti.text)
            if p_1 == False or p_1 <= 0:
                p_1 = 0
                self.ti.text = str(p_1)
            else:
                self.manager.transition.direction = 'left'
                self.manager.current = 'third'
    def sec_finished(self, *args):
        self.ti.set_disabled(False)
        self.btn.set_disabled(False)
        self.flag = True
        self.btn.text = 'Продолжить'
class ThirdScr(Screen):
    def __init__(self, name='third'):
        super().__init__(name=name) # имя экрана должно передаваться конструктору класса Screen
        self.btn = Button(text = 'Начать', size_hint = (0.3, 0.2), pos_hint = {'center_x': 0.5})
        self.btn.on_press = self.next
        self.next_screen = False
        label_1 = Label(text = 'Выполните 30 приседаний за 45 секунд')
        layout_vertical = BoxLayout(orientation = 'vertical', padding = 8, spacing = 8)
        self.lbl_sits = Sits(30)
        self.run = Runner(total = 30, steptime = 1.5, size_hint = (0.4,1))
        layout_vertical_2 = BoxLayout(padding = 8, spacing = 8)
        layout_vertical_2.add_widget(label_1)
        layout_vertical_2.add_widget(self.lbl_sits)
        layout_vertical_2.add_widget(self.run)
        layout_vertical.add_widget(layout_vertical_2)
        layout_vertical.add_widget(self.btn)
        self.add_widget(layout_vertical)
        self.run.bind(finished = self.finished)
    def finished(self, a, b):
        self.btn.set_disabled(False)
        self.btn.text = 'Продолжить'
        self.next_screen = True
    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.run.start()
            self.run.bind(value = self.lbl_sits.next)
        else:
            self.manager.transition.direction = 'up'
            self.manager.current = 'fourten'
class FourtenScr(Screen):
    def __init__(self, name='fourten'):
        super().__init__(name = name)
        self.tap_tap = 0
        label_1 = Label(text = txt_test3)
        self.button_1 = Button(text = 'Начать', size_hint = (0.3, 0.2), pos_hint = {'center_x': 0.5})
        self.button_1.on_press = self.next   
        layout_1 = BoxLayout(size_hint = (0.8, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, height = '30sp')
        layout_2 = BoxLayout(size_hint = (0.8, None), pos_hint={'center_x': 0.5, 'center_y': 0.5}, height = '30sp')
        layout_vertical = BoxLayout(orientation = 'vertical', padding = 8, spacing = 8)
        self.ti_1 = TextInput(multiline = False)
        l_1 = Label(text = 'Результат')
        self.ti_2 = TextInput(multiline = False)
        l_2 = Label(text = 'Результат после отдыха')
        self.lbl_sec = Seconds(15)
        self.lbl_sec.bind(done = self.sec_finished)
        self.flag = False
        self.ti_1.set_disabled(True)
        self.ti_2.set_disabled(True)
        layout_1.add_widget(l_1)
        layout_1.add_widget(self.ti_1)
        layout_2.add_widget(l_2)
        layout_2.add_widget(self.ti_2)
        layout_vertical.add_widget(label_1)
        layout_vertical.add_widget(self.lbl_sec)
        layout_vertical.add_widget(layout_1)
        layout_vertical.add_widget(layout_2)
        layout_vertical.add_widget(self.button_1)
        self.add_widget(layout_vertical)
    def next(self):
        if not self.flag:
            self.button_1.set_disabled(True)
            self.lbl_sec.start()
        else:  
            p_2 = check_int(self.ti_1.text)
            p_3 = check_int(self.ti_2.text)
            if p_2  == False or p_2 <= 0:
                p_2 = 0
                self.ti_1.text = str(p_2)
            elif p_3 == False or p_3 <= 0:
                p_3 = 0
                self.ti_2.text = str(p_3)
            else:
                self.manager.transition.direction = 'right'
                self.manager.current = 'result'
    def sec_finished(self, *args):
        if self.lbl_sec.done:
            if self.tap_tap == 0:
                self.tap_tap = 1
                self.lbl_sec.restart(30)
                self.ti_1.set_disabled(False)
            elif self.tap_tap == 1:
                self.tap_tap = 2
                self.lbl_sec.restart(15)
            elif self.tap_tap == 2:
                self.ti_2.set_disabled(False)
                self.button_1.set_disabled(False)
                self.button_1.text = 'Завершить'
                self.flag = True

class Result(Screen):
    def __init__(self, name = 'result'):
        super().__init__(name = name)
        self.label_1 = Label(text = '')
        layout_vertical = BoxLayout(orientation = 'vertical', padding = 8, spacing = 8)
        layout_vertical.add_widget(self.label_1)
        self.add_widget(layout_vertical)
        self.on_enter = self.before
    def before(self):
        self.label_1.text = name + '\n' + test(p_1, p_2, p_3, age)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Main_screen())
        sm.add_widget(FirstScr())
        sm.add_widget(ThirdScr())
        sm.add_widget(FourtenScr())
        sm.add_widget(Result())
        return sm

app = MyApp()
app.run()






























