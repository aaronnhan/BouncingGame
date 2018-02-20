import kivy
kivy.require("1.8.0")
from os import listdir
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
import time
from kivy.app import App
#from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from math import sqrt, sin, cos, atan, pi
import sys
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
Window.size = (500, 400)

Builder.load_string("""
<Game_layout>:
    size_hint: (1,1)
    FloatLayout:
        size_hint: (1,1)
        id: myLayout
<Cube>:
    ScreenManager:
        id: sm
        size: root.width, root.height
        Screen:
            size_hint: (1,1)
            id: screen_zero
            name: "0"
            Game_layout:
                id: layout0
        Screen:
            id: screen_one
            name: "1"
            Game_layout:
                id: layout1
        Screen:
            id: screen_two
            name: "2"
            Game_layout:
                id: layout2
        Screen:
            id: screen_three
            name: "3"
            Game_layout:
                id: layout3
        Screen:
            id: screen_four
            name: "4"
            Game_layout:
                id: layout4
        Screen:
            id: screen_five
            name: "5"
            Game_layout:
                id: layout5
<GameScreen>:
    FloatLayout:
        id:gamescreen
<LevelScreen>:
    AnchorLayout:
        anchor_x: "center"
        anchor_y: "top"
        BoxLayout:
            id: levelMenu
            orientation: "vertical"
            size_hint: (.5, .2)
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
#        source: "line.png"
        pos: self.pos
<FinishLayout>:
    size_hint: (1,1)
    pos: root.pos
    AnchorLayout:
        id: restart
        anchor_x: "left"
        anchor_y: "bottom"
    AnchorLayout:
        id: level
        anchor_x: "center" 
        anchor_y: "bottom"
    AnchorLayout:
        id: next
        anchor_x: "right"
        anchor_y: "bottom"
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

    def returnText(self, filepath): # makes list of [object, parameters]
        try:
            f = open(filepath)
            text = f.read()
            f.close()
            myList = []
            for line in text.split("\n"):
                smallList = []
                myList.append(line)
            return myList
        except IOError:
            return
    def string_to_list(self, string):
        myList = []
        for x in string.split(","):
            myList.append(x)
        return myList
    def parseList(self,listy):
        returnList = []#list of faces
        for x in listy: #Each face; always 6
            nodelist = []
            walllist = []
            obstaclelist = []
            lists = x.split("|")
            for node in lists[0].split(";"):
                nodelist.append(self.makeNode(self.string_to_list(node)))
            for wall in lists[1].split(";"):
                walllist.append(self.makeWall(self.string_to_list(wall)))
            for obstacle in lists[2].split(";"):
                obstaclelist.append(self.makeObstacle(self.string_to_list(obstacle)))
            returnList.append([nodelist, walllist, obstaclelist])
        return returnList
    
    def return_level(self,level):
        myBuilder = levelBuilder()
        levelList = myBuilder.find_levels() # list of levels
        filename = "levels/" + str(level) + ".txt" # makes file path
        fileText = myBuilder.returnText(filename) # gets file text
        return myBuilder.parseList(fileText)


class Player(Widget):
    def __init__(self, nodelist, walllist, obstaclelist, **kwargs):
        self.mySize = (15*window_ratio_y,15*window_ratio_y)
        super(Player, self).__init__(**kwargs)
        self.start_center = [40,40]
        self.finishNode = None
        self.nodelist = nodelist
        #self.finishNode = self.nodelist[-1]
        self.obstaclelist = obstaclelist
        self.walllist = walllist
        self.restart()
        if type(self.nodelist[0]) is not str:
            self.start_center = [Window.width/10,self.nodelist[0].ids["node"].y]
        self.finished = False
    def update(self, dt):
        self.updatePos()
        if not self.node:
            self.checkNode()
    def inBound(self):
        if self.ids["player"].center_x <= 0:
            self.parent.change_face(3)
        elif self.ids["player"].y <= 0:
            self.parent.change_face(2)
        elif self.ids["player"].center_x >= Window.width:
            self.parent.change_face(1)
        elif self.ids["player"].center_y >= Window.height: 
            self.parent.change_face(0)
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
        if self.node == self.finishNode:
            self.finished = True
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
            if (distance <= self.nodelist[x].radius):
                self.node = self.nodelist[x]
        for x in range(len(self.obstaclelist)):
            if self.obstaclelist[x].ids["obstacle"].collide_point(self.ids["player"].x, self.ids["player"].y):
                self.restart()
        for x in range(len(self.walllist)):
            if self.walllist[x].ids["wall"].collide_point(self.ids["player"].x, self.ids["player"].y) and (time.time()-self.lastWall[1]>.1): # COLLIDE
                if self.walllist[x].angle == 90:
                    self.velocity[0]*=-1
                    self.lastWall[0] = self.walllist[x]
                    self.lastWall[1] = time.time()
                elif self.walllist[x].angle == 0:
                    self.velocity[1]*=-1
                    self.lastWall[0] = self.walllist[x]
                    self.lastWall[1] = time.time()
        if self.node:
            self.angle = self.calcAngle()
    def on_touch_down(self, key):
        print self.parent
        #if  self.parent.parent.children[0].collide_point(key.x, key.y): #BUTTON DETECTION
            #return None #CAN CHANGE TO IF
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
        self.lastWall = [None, 0]
    def setPos(self, x, y):
        self.ids["player"].center = (x,y)
class Node(Widget):
    def __init__(self,x,y,radius, **kwargs):
        self.mySize = (10*window_ratio_x,10*window_ratio_y)
        super(Node, self).__init__(**kwargs)
        self.ids["node"].center = (x*window_ratio_x,y*window_ratio_y)
        self.radius = radius*window_ratio_y
        self.used = False
class Obstacle(Widget):
    def __init__(self,x, y, **kwargs):
        super(Obstacle, self).__init__(**kwargs)
        self.ids["obstacle"].center = (x*window_ratio_x, y*window_ratio_y)
class Wall(Widget):
    def __init__(self,x, y, size_x, size_y, angle, **kwargs):
        self.angle = angle
        super(Wall, self).__init__(**kwargs)
        self.center = (x*window_ratio_x, y*window_ratio_y)
        self.ids["wall"].width = size_x*window_ratio_x
        self.ids["wall"].height = size_y*window_ratio_y

class Game_layout(Widget):
    def __init__(self, **kwargs):
        super(Game_layout, self).__init__(**kwargs)
        self.finished = False
        self.levelBuilder = levelBuilder()
        self.nodeList = []
        self.obstacleList = []
        self.wallList = []
        self.gameLayout = FloatLayout(size_hint = (None, None))
        self.add_widget(self.gameLayout)
    def get_lists(self):
        return [self.nodeList, self.wallList, self.obstacleList]
    def set_lists(self, nodelist, walllist, obstaclelist):
        self.nodeList = nodelist
        self.obstacleList = obstaclelist
        self.wallList = walllist
        self.gameLayout.clear_widgets()
        self.loadLevel()
    def select_levels(self, parent):
        self.popup.dismiss()
    def select_main(self, parent):
        self.popup.dismiss()
    def levelHelper(self, parent):
        self.level = parent.text[parent.text.find("/"):parent.text.find(".")]
        self.loadLevel()
    def loadMenu(self, *arg):
        self.popup.open()
    def loadLevel(self):
        self.gameLayout.clear_widgets()
        for x in range(len(self.nodeList)):
            self.gameLayout.add_widget(self.nodeList[x])
        for x in range(len(self.obstacleList)):
            self.gameLayout.add_widget(self.obstacleList[x])
        for x in range(len(self.wallList)):
            self.gameLayout.add_widget(self.wallList[x])
    def check_finished(self, dt):
        self.finished = self.myPlayer.finished
class GameScreen(Screen):
    pass
class Cube(Widget):
    def __init__(self, level,**kwargs):
        super(Cube, self).__init__(**kwargs)
        self.builder = levelBuilder()
        self.face_guide = [[3,2,1,4],[0,2,5,4],[0,3,5,1],[0,4,5,2],[0,1,5,3],[1,2,3,4]]
        self.faces = self.builder.return_level(level) # list of lists for gamelayout (nodelist, etc.)
        for x in range(len(self.faces)):
            self.ids["layout" + str(x)].set_lists(self.faces[x][0], self.faces[x][1],self.faces[x][2])
            #self.ids["layout" + str(x+1)].loadLevel()
        self.ids["layout1"].loadLevel()
        self.myPlayer = Player(self.faces[0][0], self.faces[0][1],self.faces[0][2])
        self.add_widget(self.myPlayer)
        Clock.schedule_interval(self.myPlayer.update, .05)
        self.ids["sm"].current = "1"
    def change_face(self, direction):
        print self.face_guide[int(self.ids["sm"].current)][direction]
        self.ids["sm"].current = str(self.face_guide[int(self.ids["sm"].current)][direction])
        self.myPlayer.setPos(40,40)
    def on_touch_down(self, key):
        self.myPlayer.on_touch_down(key)
    #    self.change_face(self.current_face)
    #    self.current_face+=1
class TestApp(App):
    def build(self):
        return Cube(1)
if __name__ == '__main__':
    TestApp().run()
