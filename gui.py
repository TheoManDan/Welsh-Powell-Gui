from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.graphics import Rectangle
from kivy.graphics import Ellipse
from kivy.graphics import Color
from kivy.graphics import Line 
from kivy.uix.popup import Popup
from main import check

class SetupScreen(FloatLayout):

    def __init__(self, **kwargs):
        super(SetupScreen, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1000, 500)

        #global value
        self.vertexCoord = {}

        self.nbVertex = 0
        self.drawVertexPressed = False
        self.drawArcPressed = False
        self.validation = Button(
                            text="Go !",
                            size_hint=(.2,.1),
                            pos=(740,20)
                            )
        self.undoAction = Button(
                            text="Annuler ",
                            size_hint=(.2,.1),
                            pos=(740,100)
                            )
        self.actionDrawVertex = Button(
                            text="Dessiner les sommets ",
                            size_hint=(.2,.1),
                            pos=(740,180)
                            )
        self.actionDrawArc = Button(
                            text="Dessiner les arcs ",
                            size_hint=(.2,.1),
                            pos=(740,260)
                            )
        self.undoAction.bind(on_press=self.undo)
        self.actionDrawArc.bind(on_press=self.pressedSetUpArc)
        self.actionDrawVertex.bind(on_press=self.pressedSetUpVertex)
        self.add_widget(self.validation)
        self.add_widget(self.undoAction)
        self.add_widget(self.actionDrawArc)
        self.add_widget(self.actionDrawVertex)

        with self.canvas:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(pos=(0,0), size=(700,500))

    def pressedSetUpVertex(self,btn):
        if(not self.drawVertexPressed):
            self.drawVertexPressed = True
            self.actionDrawVertex.background_color = (0, 1, 0)
        else:
            self.drawVertexPressed = False
            self.actionDrawVertex.background_color = (1, 1, 1, 1)

    def pressedSetUpArc(self,btn1):
        if(not self.drawArcPressed):
            self.drawArcPressed = True
            self.actionDrawArc.background_color = (0, 1, 0)
        else:
            self.drawArcPressed = False
            self.actionDrawArc.background_color = (1, 1, 1, 1)
            print("Là")        


    def undo(self,btn):
        if self.drawVertexPressed:
            if self.nbVertex > 0:
                with self.canvas:
                    Color(0,0,0)
                    d = 30.
                    x = self.vertexCoord[self.nbVertex-1][0]
                    y = self.vertexCoord[self.nbVertex-1][1]
                    Ellipse(pos=(x,y),size=(d,d))
                    del self.vertexCoord[self.nbVertex-1]
                    self.nbVertex-=1
            else:
                print("Ooopsss...")

    def checkInt(self,str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def on_touch_down(self,touch):

        x = touch.pos[0]
        y = touch.pos[1]

        if self.drawVertexPressed:

            if x < 700 and y < 500:
                with self.canvas:
                    Color(1, 1, 0)
                    d = 30.
                    Ellipse(pos=(x - d / 2, y - d / 2), size=(d, d))
                    
                    self.vertexCoord[self.nbVertex] = (x - d / 2,y - d / 2)
                    self.nbVertex+=1
                    print(self.vertexCoord)

        if self.drawArcPressed:
            x = touch.pos[0]
            y = touch.pos[1]

            if x < 700 and y < 500:
                with self.canvas:
                    Color(0,1,0)
                    self.line = Line(points=[touch.pos[0], touch.pos[1]], width=2)

       
        return super(SetupScreen, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        self.line.points = self.line.points + [touch.pos[0], touch.pos[1]]


class MainApp(App):
    def build(self):
        return SetupScreen()

MainApp().run()