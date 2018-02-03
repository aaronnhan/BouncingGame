import kivy
kivy.require("1.8.0")
from os import listdir
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from math import sqrt, sin, cos, atan, pi
import sys
from kivy.metrics import dp
#Window.size = (500, 400)

Builder.load_string("""
<Player>:
    Image:
        id: player
        size_hint: (.1, .1)
#        source: "player.png"
        pos: self.pos
        size: root.mySize
<Node>:
    Image: 
        id: node
#        source: "background.png"
        pos: self.pos
        size:(10,10)
<Obstacle>:
    Image:
        id: obstacle
#        source: "object.png"
        pos: self.pos
        size: 10,10
<Wall>:
    Image:
        id: wall
#        source: "wall.png"
        pos: self.pos
        canvas.before:
            PushMatrix
            Rotate:
                angle: root.angle
                axis: 0, 0, 1
                origin: self.center
        canvas.after:
            PopMatrix
""")
window_ratio_y = Window.height/350.
window_ratio_x = Window.width/500.
class levelBuilder():
    def __init__(self):
        self.nodeList = []
        self.wallList = []
        self.obstacleList = []
    def makeNode(self, listy):
        x = int(listy[0])
        y = int(listy[1])
        radius = int(listy[2])
        return Node(x,y,radius)
    def makeWall(self, listy):
        w = int(listy[0])
        x = int(listy[1])
        y = int(listy[2])
        z = int(listy[3])
        r = int(listy[4])
        return Wall(w,x,y,z,r)
    def makeObstacle(self, listy):
        x = int(listy[0])
        y = int(listy[1])
        return Obstacle(x,y)
    def find_levels(self):
        levels = []
        for file in listdir("levels"):
            if file.endswith(".txt"):
                levels.append("levels/" + file)
        levels.sort()
        return levels

    def returnText(self, filepath):
        try:
            f = open(filepath)
            text = f.read()
            f.close()
            myList = []
            for line in text.split("\n"):
                smallList = []
                for key in line.split(": "):#[Node, None]
                    smallList.append(key)
                myList.append(smallList)
            return myList
        except IOError:
            return
    def parseList(self,listy):
        wallList = []
        nodeList = []
        obstacleList = []
        for x in listy:
            paramList = x[1].split(",")
            if x[0] == "wall":
                wallList.append(self.makeWall(paramList))
            if x[0] == "node":
                nodeList.append(self.makeNode(paramList))
            if x[0] == "object":
                obstacleList.append(self.makeObstacle(paramList))
        return [wallList, nodeList, obstacleList]
    
    def build_level(self,level):
        myBuilder = levelBuilder()
        levelList = myBuilder.find_levels() # list of levels
        filename = "levels/" + str(level) + ".txt" # makes file path
        fileText = myBuilder.returnText(filename) # gets file text
        return myBuilder.parseList(fileText)


class Player(Widget):
    def __init__(self, nodelist, obstaclelist, walllist, **kwargs):
        self.mySize = (15*window_ratio_y,15*window_ratio_y)
        super(Player, self).__init__(**kwargs)
        self.nodelist = nodelist
        self.obstaclelist = obstaclelist
        self.walllist = walllist
        self.start_center = [50*window_ratio_x,130*window_ratio_y]
        self.restart()
    def update(self, dt):
        self.updatePos()
        if not self.node:
            self.checkNode()
    def inBound(self):
        if self.ids["player"].center_x <= 0 or self.ids["player"].y <= 0 or self.ids["player"].center_x >= Window.width or self.ids["player"].center_y >= Window.height: 
            self.restart()
    def updatePos(self):
        self.inBound()
        if self.node == None:
            self.ids["player"].x +=self.velocity[0]*window_ratio_x
            self.ids["player"].y +=self.velocity[1]*window_ratio_y
        else:
            self.angle += .15*self.direction
            self.ids["player"].center_x = self.node.ids["node"].center_x + self.node.radius*window_ratio_y*cos(self.angle)
            self.ids["player"].center_y = self.node.ids["node"].center_y + self.node.radius*window_ratio_y*sin(self.angle)
    def calcAngle(self):
        ydif = (float)(self.node.ids["node"].center_y - self.ids["player"].center_y)
        xdif = (float)(self.node.ids["node"].center_x - self.ids["player"].center_x)
        angle = atan(ydif/xdif)
        if self.node.ids["node"].center_x > self.ids["player"].center_x:
            angle += pi
        distanceX = self.ids["player"].center_x - self.node.ids["node"].center_x
        distanceY = self.ids["player"].center_y - self.node.ids["node"].center_y
        if distanceX*self.velocity[1]/self.velocity[0]>distanceY: # if projected to be below node 
            if self.velocity[0] > 0:
                self.direction = 1
            else:
                self.direction = -1
        else:
            if self.velocity[0] > 0:
                self.direction = 1
            else:
                self.direction = -1
            
        return angle
    def checkNode(self):
        for x in range(len(self.nodelist)):
            distance = sqrt(pow(self.ids["player"].center_y - self.nodelist[x].ids["node"].center_y, 2) + 
                    pow(self.ids["player"].center_x - self.nodelist[x].ids["node"].center_x, 2))
            if ( distance <= self.nodelist[x].radius):
                self.node = self.nodelist[x]
        for x in range(len(self.obstaclelist)):
            if self.ids["player"].collide_widget(self.obstaclelist[x].ids["obstacle"]):
                self.restart()
        for x in range(len(self.walllist)):
            if self.ids["player"].collide_widget(self.walllist[x].ids["wall"]): #and ((self.walllist[x] is not self.lastWall[0]) or time.time()-self.lastWall[1]>1.5): # COLLIDE
                print self.walllist[x].center
                angle = atan(self.velocity[1]/self.velocity[0])
                if self.walllist[x].ids["wall"].center_x > self.ids["player"].center_x:
                    angle += pi
                angle = -angle+2*self.walllist[x].angle
                self.lastWall = [self.walllist[x], time.time()]
                self.velocity = [self.speed*cos(angle), self.speed*sin(angle)]
        if self.node:
            self.angle = self.calcAngle()
    def on_touch_down(self, key):
        if self.parent.parent.children[2].collide_point(key.x, key.y) or self.parent.parent.children[1].collide_point(key.x, key.y):
            return None #CAN CHANGE TO IF
        if self.node:
            lAngle = self.angle+(pi/2)
            x = self.node.radius*cos(lAngle)
            y = self.node.radius*sin(lAngle)
            ratio = sqrt(pow(x, 2) + pow(y,2))
            if ((int)(lAngle/pi))%2 == 0: # no idea how this works
                yDir = 1
            else:
                yDir = -1
            if (int)((lAngle+pi/2)/pi)%2 == 0: # 1 + 3: no idea how this works
                xDir = 1
            else: 
                xDir = -1
            self.velocity = [abs(12*x/ratio)*xDir, abs(12*y/ratio)*yDir]
            self.node = None
    def restart(self, *args):
        self.node = None
        self.angle = None
        self.speed = 12
        self.velocity = [12.,0]
        self.ids["player"].center = self.start_center
        self.direction = 0
        self.lastWall = [None, None]
         
class Node(Widget):
    def __init__(self,x,y,radius, **kwargs):
        self.mySize = (10*window_ratio_x,10*window_ratio_y)
        super(Node, self).__init__(**kwargs)
        self.ids["node"].center = (x*window_ratio_x,y*window_ratio_y)
        self.radius = radius
        self.used = False
class Obstacle(Widget):
    def __init__(self,x, y, **kwargs):
        super(Obstacle, self).__init__(**kwargs)
        self.ids["obstacle"].center = (x*window_ratio_x, y*window_ratio_y)
class Wall(Widget):
    def __init__(self,x, y, size_x, size_y, angle, **kwargs):
        self.angle = angle
        super(Wall, self).__init__(**kwargs)
        self.ids["wall"].center = (x*window_ratio_x, y*window_ratio_y)
        self.ids["wall"].width = size_x*window_ratio_x
        self.ids["wall"].height = size_y*window_ratio_y

class gameScreen(Widget):
    def __init__(self, **kwargs):
        super(gameScreen, self).__init__(**kwargs)
        self.levelBuilder = levelBuilder()
        self.level = 1
        #Menu
        self.myMenu = GridLayout(cols = 1,orientation = "vertical", size_hint_y = None)
        self.popupScroll = ScrollView(size_hint_y = None, size = (Window.width, Window.height*.9))
        self.popupScroll.add_widget(self.myMenu)
        self.popup = Popup(content = self.popupScroll, title = "Choose a plugin", size_hint= (.5,1))

        self.nodeList = [Node(200, 130, 50), Node(400, 130, 50), Node(400, 400, 50)]
        self.obstacleList = [Obstacle(300, 130)]
        self.wallList = [Wall(600,100,100,900, 0)]

        self.myPlayer = Player(self.nodeList, self.obstacleList, self.wallList)
        Clock.schedule_interval(self.myPlayer.update, 1/30.)
        self.gameLayout = FloatLayout(size_hint = (None, None))
        self.myLayout = FloatLayout(size_hint = (None, None))
        self.gameLayout.add_widget(self.myPlayer)
        for x in range(len(self.nodeList)):
            self.gameLayout.add_widget(self.nodeList[x])
        for x in range(len(self.obstacleList)):
            self.gameLayout.add_widget(self.obstacleList[x])
        for x in range(len(self.wallList)):
            self.gameLayout.add_widget(self.wallList[x])


        self.restartButton = Button(pos = (0,Window.height*9/10), size_hint = (None, None),size = (Window.width/5, Window.height/5), on_release = self.myPlayer.restart)
        self.levelSelectButton = Button(pos = (Window.width/5,Window.height*9/10), size = (Window.width/5, Window.height/5), size_hint = (None, None), on_release = self.loadMenu)
        self.myLayout.add_widget(self.restartButton)
        self.myLayout.add_widget(self.levelSelectButton)
        self.myLayout.add_widget(self.gameLayout)

        for x in self.levelBuilder.find_levels():
            self.myMenu.add_widget(Button(text = x, on_press = self.levelHelper))
    def levelHelper(self, parent):
        print parent.text
        self.level = parent.text[parent.text.find("/"):parent.text.find(".")]
        self.loadLevel()
    def loadMenu(self, *arg):
        self.popup.open()
    def closeMenu(self):
        self.popup.dismiss()
    def loadLevel(self):
        self.closeMenu()
        listy = self.levelBuilder.build_level(self.level) # wall, node, obstacle
        self.gameLayout.clear_widgets()
        self.wallList = listy[0]
        self.nodeList = listy[1]
        self.objectList = listy[2]
        Clock.unschedule(self.myPlayer.update)
        self.myPlayer = Player(self.nodeList, self.obstacleList, self.wallList)
        Clock.schedule_interval(self.myPlayer.update, 1/30.)
        self.gameLayout.add_widget(self.myPlayer)
        for x in range(len(self.nodeList)):
            self.gameLayout.add_widget(self.nodeList[x])
        for x in range(len(self.obstacleList)):
            self.gameLayout.add_widget(self.obstacleList[x])
        for x in range(len(self.wallList)):
            self.gameLayout.add_widget(self.wallList[x])
        self.myPlayer.restart()

    def returnGame(self):
        return self.myLayout
class TestApp(App):
    def build(self):
        myScreen = gameScreen()
        return myScreen.returnGame()
if __name__ == '__main__':
    TestApp().run()
