
import random
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
from kivy.uix.screenmanager import SlideTransition,SwapTransition,ScreenManager, Screen, FadeTransition
from kivy.utils import *
from main import check

class Arcs:

    def __init__(self,start,poid,end):
        self.start = start
        self.end = end
        self.poid = poid

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getPoid(self):
        return self.getPoid

class ResultScreen(Screen):

    def __init__(self,**kwargs):
        super(ResultScreen,self).__init__(**kwargs)
        #Window.clearcolor = (0,1,0)
        Window.size = (1000,500)
        self.backSetup = Button(
                            text="Back ",
                            size_hint=(.2,.1),
                            pos=(740,20)
                            )
        self.backSetup.bind(on_press=self.move)
        self.add_widget(self.backSetup)

    def move(self,btn):
        self.manager.current = 'setup'


class SetupScreen(Screen,FloatLayout):

    def __init__(self, **kwargs):
        super(SetupScreen, self).__init__(**kwargs)
        Window.clearcolor = (1, 1, 1, 1)
        Window.size = (1000, 500)

        #global value
        self.vertexCoord = {}
        self.arcsCoord = {}
        self.lienListe = []
        self.adjacency_matrix = []

        self.nbVertex = 0
        self.nbLigne = 0
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
        self.kLimit  = TextInput(
                            text="K-limit",
                            size_hint=(.2,.1),
                            pos=(740,340))
        self.undoAction.bind(on_press=self.undo)
        self.actionDrawArc.bind(on_press=self.pressedSetUpArc)
        self.actionDrawVertex.bind(on_press=self.pressedSetUpVertex)
        self.validation.bind(on_press=self.processData)
        self.add_widget(self.validation)
        self.add_widget(self.undoAction)
        self.add_widget(self.actionDrawArc)
        self.add_widget(self.actionDrawVertex)
        self.add_widget(self.kLimit)

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
            #print("Là")       
 
    def colorAssignement(self,colorSet):

        d = 30.
        r = d/2
    
        with self.canvas:
            for sommet, nombre in colorSet.items():
                    if nombre == 0:
                        Color(1,0,0)
                    elif nombre == 1:
                        Color(0,1,0)
                    elif nombre == 2:
                        Color(0,0,1)
                    elif nombre == 3:
                        Color(1,1,0)
                    elif nombre == 4:
                        Color(0,1,1)
                    elif nombre == 5:
                        Color(1,0,1)
                    elif nombre == 6:
                        Color(0,1,1)
                    elif nombre == 7:
                        Color(1,1,1)            
                    print("{} -> {}".format(sommet,nombre))
                    x = self.vertexCoord[sommet][0]
                    y = self.vertexCoord[sommet][1]
                    Ellipse(pos=(x-r,y-r),size=(d,d))

    def welsh_powell(self,mat,kLimit):

        dic = {}
        dejaColorier = []
        couleurVertex = {}
        couleur = 0
        kColoriable = True

        taille = len(mat)

        for i in range(0,taille):
                tmp = 0
                for j in range(0,taille):
                        if mat[i][j] == 1:
                                tmp+=1
                dic[i] = tmp
                dejaColorier.append(False)

        dic = dict(sorted(dic.items(), key=lambda item: item[1],reverse=True))
        x = list(dic.keys())

        while False in dejaColorier :

                if couleur >= kLimit:
                        kColoriable = False
                        break
                else:
                        selectedVertex = x[0]
                        dejaColorier[selectedVertex] = True
                        couleurVertex[selectedVertex] = couleur
                        x.remove(selectedVertex)

                        for sommet in x:

                                if mat[selectedVertex][sommet] == 0:
                                        dejaColorier[sommet] = True
                                        couleurVertex[sommet] = couleur
                                        x.remove(sommet)

                        couleur+=1

        return couleur,kColoriable,couleurVertex

    def check(self,mat,k):
        tuple = self.welsh_powell(mat,k)

        if(not tuple[1]):
                self.colorAssignement(tuple[2])
                popup = Popup(title="Résultat",
                            content=Label(text="Le graphe n'est pas k-{} coloriable\n seulement {} sommets on été coloriés".format(k,len(tuple[2]))),
                            size_hint=(None, None), size=(400, 400))
                popup.open()
        else:
                print()
                popup = Popup(title="Résultat",
                            content=Label(text="Le graphe est bien k-{} coloriable".format(k),
                            size_hint=(None, None), size=(400, 400)))
                popup.open()
                self.colorAssignement(tuple[2])

    def undo(self,btn):
        if self.drawVertexPressed:
            if self.nbVertex > 0:
                with self.canvas:
                    Color(0,0,0)
                    d = 30.
                    x = self.vertexCoord[self.nbVertex-1][0]
                    y = self.vertexCoord[self.nbVertex-1][1]
                    Ellipse(pos=(x,y),size=(d,d))
                    self.add_widget(Label(text=str(self.nbVertex),pos_hint={'center_x':(x-d)/1000,'center_y':(y-d)/500},
                                    color=(0, 0, 0)))
                    del self.vertexCoord[self.nbVertex-1]
                    self.nbVertex-=1
            else:
                print("Ooopsss...")
        elif self.drawArcPressed:
            if self.nbLigne > 0:
                with self.canvas:
                    Color(0,0,0)
                    x1 = self.arcsCoord[self.nbLigne-1][0]
                    y1 = self.arcsCoord[self.nbLigne-1][1]
                    x2 = self.arcsCoord[self.nbLigne-1][2]
                    y2 = self.arcsCoord[self.nbLigne-1][3]
                    self.line_replace = Line(points=[x1,y1,x2,y2], width=2)
                    del self.arcsCoord[self.nbLigne-1]
                    self.nbLigne-=1


    def checkInt(self,str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def on_touch_down(self,touch):

        x = touch.pos[0]
        y = touch.pos[1]
        d = 30.
        r = d/2

        if self.drawVertexPressed:

            if x < 700 and y < 500:
                with self.canvas:
                    Color(1, 1, 0)
                    Ellipse(pos=(x-r, y-r), size=(d, d))
                    self.vertexCoord[self.nbVertex] = (x,y)
                    self.add_widget(Label(text=str(self.nbVertex),pos_hint={'center_x':(x-d)/1000,'center_y':(y-d)/500},
                                    color=(0, 1, 0)))
                    self.nbVertex+=1

        if self.drawArcPressed:

            if x < 700 and y < 500:
                with self.canvas:
                    Color(0,1,0)
                    self.line = Line(points=[touch.pos[0], touch.pos[1]], width=2)


        if not self.drawArcPressed and not self.drawVertexPressed:
            for vertex, points in self.vertexCoord.items():
                xVertex = points[0]
                yVertex = points[1]

                if (x >= xVertex - r and x <= xVertex + r) and (y >= yVertex - r and y <= yVertex + r):
                        print("Tu as cliqué sur le sommet {}".format(vertex)) 

        return super(SetupScreen, self).on_touch_down(touch)

    '''def on_touch_move(self, touch):
        if self.drawArcPressed:
            self.line.points = self.line.points + [touch.pos[0], touch.pos[1]]'''

    def on_touch_up(self,touch):
        x = touch.pos[0]
        y = touch.pos[1]

        if self.drawArcPressed and x < 700 and y < 500:
            self.line.points = self.line.points + [x, y]
            self.arcsCoord[self.nbLigne] = self.line.points
            #print(self.arcsCoord)
            self.nbLigne +=1 

    def processData(self,btn2):

        d = 30.
        r = d/2
        for ligne,points in self.arcsCoord.items():
            x1 = points[0]
            y1 = points[1]
            x2 = points[2]
            y2 = points[3]
            idStart = -1
            idFinish = -1
            for vertex, points_prim in self.vertexCoord.items():
                xPoint = points_prim[0]
                yPoint = points_prim[1]

                if x1 >= xPoint - r and x1 <= xPoint + r and y1 >= yPoint - r and y1 <= yPoint + r:
                    idStart = vertex

                if x2 >= xPoint - r and x2 <= xPoint + r and y2 >= yPoint - r and y2 <= yPoint + r:
                    idFinish = vertex

            if idStart != -1 and idFinish != -1:
                print("Arc({},{})".format(idStart,idFinish))
                print("Arc({},{})".format(idFinish,idStart))
                arc = Arcs(idStart,-1,idFinish) #dans le cas d'un graphe non pondéré non poids = -1
                arcOppose = Arcs(idFinish,-1,idStart)
                self.lienListe.append(arc)
                self.lienListe.append(arcOppose)


        #maintenant construire la matrice d'adjacence 
        for i in range(0,self.nbVertex):
            tmp = [0 for x in range(self.nbVertex)]
            for arcs in self.lienListe:
                start = arcs.getStart()
                finish = arcs.getEnd()
                if i == start:
                    tmp[finish] = 1

            self.adjacency_matrix.append(tmp)

        self.check(self.adjacency_matrix,int(self.kLimit.text))

        #self.manager.current = 'result'
               

class MainApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(SetupScreen(name='setup'))
        sm.add_widget(ResultScreen(name='result'))
        return sm

    

MainApp().run()