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
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from math import sqrt, sin, cos, atan, pi
import sys
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
#Window.size = (800, 400)
#Window.size = (100, 288)
Builder.load_string("""
<Menu>:
    ScreenManager:
        size: root.size
        id: sm
        Screen:
            id: title
            name: "title"
            size: root.size
            AnchorLayout:
                anchor_x: "center"
                anchor_y: "bottom"
                BoxLayout:
                    size_hint: (.75,.3)
                    orientation: "vertical"
                    Button:
                        size_hint: (1,.5)
                        text: "Play"
                        on_press: root.ids["sm"].current = "levels"
                    Button:
                        size_hint: (1,.5)
                        text: "Credits"
                        on_press: root.ids["sm"].current = "credits"
        Screen:
            id: levels
            name: "levels"
            AnchorLayout:
                anchor_x: "center"
                anchor_y: "bottom"
                ScrollView:
                    size_hint: (.75, 1)
                    BoxLayout:
                        size_hint_y: None
                        orientation: "vertical"
                        id:box
        Screen:
            id: credits
            name: "credits"
            AnchorLayout:
                size_hint: (1,1)
                anchor_x: "center"
                anchor_y: "center"
                BoxLayout:
                    orientation: "vertical"
                    Label:
                        text_size: self.size
                        halign: "center"
                        valign: "center"
                        size_hint: (1,.8)
                        text: "This game is for those that find joy in discovery.\\n\\nMany Thanks to:\\nBrenda Kosbab\\nDr. Yuanjie Li and Professor Songwu Lu\\nFriends and family that have supported me\\nYou for playing this game!\\n\\nI hope you enjoy this game as much as I enjoyed making it. \\nAaron Nhan\\n"
                    Button:
                        text: "Back"
                        size_hint: (1,.2)
                        on_press: root.ids["sm"].current = "title"
        Screen:
            id:game
            name: "game"
            AnchorLayout:
                id: back_butt
                anchor_x: "center"
                anchor_y: "bottom"
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
<GameScreen>:
    FloatLayout:
        id:gamescreen
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
        size:root.mySize
<Laser>:
    Image:
        id: laser
        source: "red.png"
        center: self.center
        allow_stretch: True
        keep_ratio: False
<Obstacle>:
    Image:
        id: obstacle
        source: "white.jpeg"
        pos: self.pos
        size: 10,10
<Wall>:
    Image:
        id: wall
#        source: "line.png"
        pos: self.pos
""")
#Window.size = (592, 288)
ratio_y = Window.height/144.
ratio_x = Window.width/296.
class levelBuilder():
    def __init__(self):
        self.nodeList = []
        self.wallList = []
        self.laserList = []
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
    def makeLaser(self, listy):
        w = int(listy[0])
        x = int(listy[1])
        y = int(listy[2])
        z = int(listy[3])
        return Laser(w,x,y,z)
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
            #for line in text.split("\n"):
            for x in range(2):
                smallList = []
                myList.append(text.split("\n")[x])
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
            laserlist = []
            lists = x.split("|")
            for node in lists[0].split(";"):
                if node is not "":
                    nodelist.append(self.makeNode(self.string_to_list(node)))
            for wall in lists[1].split(";"):
                if wall is not "":
                    walllist.append(self.makeWall(self.string_to_list(wall)))
            for laser in lists[2].split(";"):
                if laser is not "":
                    laserlist.append(self.makeLaser(self.string_to_list(laser)))
            returnList.append([nodelist, walllist, laserlist])
        return returnList
    
    def return_level(self,level):
        myBuilder = levelBuilder()
        levelList = myBuilder.find_levels() # list of levels
        filename = "levels/" + str(level) + ".txt" # makes file path
        fileText = myBuilder.returnText(filename) # gets file text
        return myBuilder.parseList(fileText)


class Player(Widget):
    def __init__(self, nodelist, walllist, laserlist, **kwargs):
        if ratio_y > ratio_x:
            self.mySize = (7*ratio_x,7*ratio_x)
        else:
            self.mySize = (7*ratio_y,7*ratio_y)
        super(Player, self).__init__(**kwargs)
        self.start_center = [Window.width/2,Window.height/2]
        self.finish_node = None
        self.nodelist = nodelist
        self.laserlist = laserlist
        self.walllist = walllist
        self.restart()
        self.node = None
        #if type(self.nodelist[0]) is not str:
        #    self.start_center = [Window.width/10,self.nodelist[0].ids["node"].y]
        self.finished = False
    def set_lists(self, listy):
        self.nodelist = listy[0]
        self.walllist = listy[1]
        self.laserlist = listy[2]
    def update(self, dt):
        if not self.node:
            self.checkNode()
        self.updatePos()
    def inBound(self):
        if self.ids["player"].center_x <= 0:
            self.parent.change_face(3)
        elif self.ids["player"].center_y <= 0:
            self.parent.change_face(2)
        elif self.ids["player"].center_x >= Window.width:
            self.parent.change_face(1)
        elif self.ids["player"].center_y >= Window.height: 
            self.parent.change_face(0)
    def updatePos(self):
        self.inBound()
        if self.node == None:
            self.ids["player"].x +=self.velocity[0]*ratio_x
            self.ids["player"].y +=self.velocity[1]*ratio_y
        else:
            self.angle += .15*self.direction
            self.ids["player"].center_x = self.node.ids["node"].center_x + self.node.radius*cos(self.angle)
            self.ids["player"].center_y = self.node.ids["node"].center_y + self.node.radius*sin(self.angle)
    def calcAngle(self):
        ydif = (float)(self.node.ids["node"].center_y - self.ids["player"].center_y)
        xdif = (float)(self.node.ids["node"].center_x - self.ids["player"].center_x)
        if xdif == 0:
            xdif = 1
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
            if (distance <= self.nodelist[x].radius and self.nodelist[x] != self.last_node):
                self.node = self.nodelist[x]
                self.last_node = self.nodelist[x]
                if self.node == self.finish_node:
                    self.finished = True
                    print "Finished"
        for x in range(len(self.laserlist)):
            if self.laserlist[x].ids["laser"].collide_point(self.ids["player"].x, self.ids["player"].y):
                self.parent.ids["sm"].current = "0"
                
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
            self.velocity = [abs(3*x/ratio)*xDir, abs(3*y/ratio)*yDir]
            self.node = None
    def restart(self, *args):
        self.last_node = None
        self.node = None
        self.angle = None
        self.speed = 12
        self.velocity = [3.,0]
        self.ids["player"].center = self.start_center
        self.direction = 1
        self.lastWall = [None, 0]
        if self.parent:
            self.set_lists(self.parent.faces[int(self.parent.ids["sm"].current)])
    def setCenter(self, x, y):
        self.ids["player"].center = (x,y)
class Node(Widget):
    def __init__(self,x,y,radius, **kwargs):
        self.mySize = (4*ratio_x, 4*ratio_y)
        super(Node, self).__init__(**kwargs)
        self.radius = radius*ratio_x
        self.ids["node"].center = (x*ratio_x, y*ratio_y)
        self.used = False
#class Obstacle(Widget):
#    def __init__(self,x, y, **kwargs):
#        super(Obstacle, self).__init__(**kwargs)
#        self.ids["obstacle"].center = (x*window_ratio_x, y*window_ratio_y)
class Wall(Widget):
    def __init__(self,x, y, size_x, size_y, angle, **kwargs):
        self.angle = angle
        super(Wall, self).__init__(**kwargs)
        self.ids["wall"].width = size_x*ratio_x
        self.ids["wall"].height = ratio_y*size_y
        self.ids["wall"].center = (x*ratio_x, y*ratio_y)
class Laser(Widget):
    def __init__(self,x, y, size_x, size_y, **kwargs):
        super(Laser, self).__init__(**kwargs)
        self.ids["laser"].width = size_x*ratio_x
        self.ids["laser"].height = ratio_y*size_y
        self.ids["laser"].center = (x*ratio_x, y*ratio_y)

class Game_layout(Widget):
    def __init__(self, **kwargs):
        super(Game_layout, self).__init__(**kwargs)
        self.finished = False
        self.levelBuilder = levelBuilder()
        self.nodeList = []
        self.laserList = []
        self.wallList = []
        self.gameLayout = FloatLayout(size_hint = (None, None))
        self.add_widget(self.gameLayout)
    def get_lists(self):
        return [self.nodeList, self.wallList, self.laserList]
    def set_lists(self, nodelist, walllist, laserlist):
        self.nodeList = nodelist
        self.laserList = laserlist
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
        for x in range(len(self.laserList)):
            self.gameLayout.add_widget(self.laserList[x])
        for x in range(len(self.wallList)):
            self.gameLayout.add_widget(self.wallList[x])
    #def check_finished(self, dt):
    #    self.finished = self.myPlayer.finished
class GameScreen(Screen):
    pass
class Cube(Widget):
    def __init__(self, level,**kwargs):
        super(Cube, self).__init__(**kwargs)
        self.builder = levelBuilder()
        self.face_guide = [[3,2,1,4],[0,2,5,4],[0,3,5,1],[0,4,5,2],[0,1,5,3],[1,2,3,4]]
        self.faces = self.builder.return_level(level) # list of lists for gamelayout (nodelist, etc.)
        for x in range(2):
            self.ids["layout" + str(x)].set_lists(self.faces[x][0], self.faces[x][1],self.faces[x][2])
       # for x in self.faces:
            #self.ids["layout" + str(x+1)].loadLevel()
        self.ids["layout0"].loadLevel()
        self.myPlayer = Player(self.faces[0][0], self.faces[0][1],self.faces[0][2])
        self.myPlayer.start_center = self.myPlayer.nodelist[0].ids["node"].center
        self.myPlayer.finish_node = self.myPlayer.nodelist[-1]
        self.myPlayer.ids["player"].center = self.myPlayer.start_center
        self.add_widget(self.myPlayer)
        Clock.schedule_interval(self.update, 1/40.)
        self.dir_list = ["down","left","up","right"]
    def update(self, dt):
        self.myPlayer.update(dt)
        if self.myPlayer.finished:
            Clock.unschedule(self.update)
            self.finish_layout = BoxLayout()
            self.finish_layout.add_widget(Button(text = "Restart", on_press = self.restart_level, size_hint = (1, 1)))
            self.finish_layout.add_widget(Button(text = "Levels", on_press = self.select_level, size_hint = (1, 1)))
            self.finish_layout.add_widget(Button(text = "Next", on_press = self.next_level, size_hint = (1, 1)))
            self.finish_popup = Popup(content = self.finish_layout, title = "Menu", size_hint= (.9,.9))
            self.finish_popup.open()
    def restart_level(self, obj):
        self.finish_popup.dismiss()
        self.parent.parent.parent.restart_level()
    def select_level(self, obj):
        self.finish_popup.dismiss()
        self.parent.parent.parent.select_level()
    def next_level(self, obj):
        self.finish_popup.dismiss()
        self.parent.parent.parent.next_level()

    def change_face(self, direction):
        self.ids["sm"].transition.direction = self.dir_list[direction]
        self.ids["sm"].current = str(1- int(self.ids["sm"].current))
        self.myPlayer.set_lists(self.faces[int(self.ids["sm"].current)])
        if direction == 0:
            self.myPlayer.setCenter(self.myPlayer.ids["player"].center_x, self.myPlayer.ids["player"].height/2)
        if direction == 1:
            self.myPlayer.setCenter(self.myPlayer.ids["player"].width/2, self.myPlayer.ids["player"].center_y)
        if direction == 2:
            self.myPlayer.setCenter(self.myPlayer.ids["player"].center_x, Window.height-self.myPlayer.ids["player"].height/2)
        if direction == 3:
            self.myPlayer.setCenter(Window.width-self.myPlayer.ids["player"].width/2, self.myPlayer.ids["player"].center_y)
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.parent.parent.parent.back()
        else:
            self.myPlayer.on_touch_down(touch)

class Menu(Widget):
    def __init__(self,**kwargs):
        super(Menu, self).__init__(**kwargs)
        for x in range(len(levelBuilder().find_levels())):
            self.ids["box"].add_widget(Button(text = str(x+1), on_press = self.press))
        self.ids["box"].height = len(self.ids["box"].children)*self.ids["box"].children[0].height
        self.current_level = 0
    def press(self, obj):
        self.ids["game"].clear_widgets()
        self.ids["game"].add_widget(Cube(int(obj.text)))
        self.current_level = int(obj.text)
        self.ids["sm"].current = "game"
    def back(self):
        self.ids["sm"].current = "title"
    def restart_level(self):
        self.ids["game"].clear_widgets()
        self.ids["game"].add_widget(Cube(self.current_level))
    def select_level(self):
        self.ids["sm"].current = "levels"
    def next_level(self):
        self.current_level +=1
        if self.current_level > len(levelBuilder().find_levels()):
            self.current_level = 1
        self.ids["game"].clear_widgets()
        self.ids["game"].add_widget(Cube(self.current_level))
class TestApp(App):
    def build(self):
        return Menu()
if __name__ == '__main__':
    TestApp().run()
