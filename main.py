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
from kivy.uix.label import Label
import time
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from math import sqrt, sin, cos, atan, pi
import sys
from kivy.clock import Clock, partial
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
Builder.load_string("""
<Menu>:
    ScreenManager:
        size: root.size
        id: sm
        Screen:
            id: title
            name: "title"
            size: root.size
            size_hint: (1,1)
            Image: 
                keep_ratio: False
                allow_stretch: True
                source: "images/grey1.PNG"
            AnchorLayout:
                anchor_x: "center"
                anchor_y: "top"
                size_hint: (1,1)
                Image:
                    size_hint: (1,.6)
                    source: "images/supercube.png"
                    center: (root.width/2, root.height*2/3)
                    keep_ratio: False
            AnchorLayout:
                anchor_x: "center"
                anchor_y: "bottom"
                BoxLayout:
                    size_hint: (.75,.3)
                    orientation: "vertical"
                    Button:
                        size_hint: (1,.5)
                        text: "Play"
                        on_release: 
                            root.ids["sm"].current = "levels"
                            root.make_menu()
                    Button:
                        size_hint: (1,.5)
                        text: "Credits"
                        on_release: root.ids["sm"].current = "credits"
        Screen:
            id: levels
            name: "levels"
            GridLayout:
                id: grid
                cols: 4
                rows: 3
        Screen:
            id: credits
            name: "credits"
            Image:
                source: "images/grey1.PNG"
                allow_stretch: True
                keep_ratio: False
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
                        text: "\\n\\nMany Thanks to:\\nBrenda Kosbab\\nDr. Yuanjie Li and Professor Songwu Lu\\nFriends and family that have supported me\\nYou for playing this game!\\n\\nI hope you enjoy this game as much as I enjoyed making it. \\nAaron Nhan\\n"
                    Button:
                        text: "Back"
                        size_hint: (1,.2)
                        on_release: root.ids["sm"].current = "title"
        Screen:
            id:game
            name: "game"
            AnchorLayout:
                id: back_butt
                anchor_x: "center"
                anchor_y: "bottom"
        Screen:
            size: root.size
            name: "white"
            Image:
                size: root.size
                source: "images/grey2.PNG"
                allow_stretch: True
                keep_ratio: False
        Screen:
            name: "tutorial"
            Image:
                size: root.size
                source: "images/grey1.PNG"
                allow_stretch: True
                keep_ratio: False
            BoxLayout:
                id: tutorial_box
#<Tutorial>:
#    Image: 
#        source: "images/grey2.PNG"
#        size_hint: (1,1)
#        allow_stretch: True
#        keep_ratio: False
#    Label:
#        size_hint: (1,1)
#        markup: True
#        id: label
<Intro>:
    ScrollView:
        size_hint: (.75, 1)
        BoxLayout:
            size_hint_y: None
            orientation: "vertical"
            id: box
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
                canvas.before:
                    Color:
                        rgba: (1,1,1,.95)
                    Rectangle:
                        size: self.size
                        pos: self.pos
        Screen:
            id: screen_one
            name: "1"
            Game_layout:
                id: layout1
                canvas.before:
                    Color:
                        rgba: (1,1,1,.15)
                    Rectangle:
                        size: self.size
                        pos: self.pos
<GameScreen>:
    FloatLayout:
        id:gamescreen
<Player>:
    Image:
        id: player
        size_hint: (.1, .1)
        source: root.color_list[root.color]
        allow_stretch: True
        keep_ratio: False
        center: root.center
        size: root.mySize
        myRotation: 45
        canvas.before:
            PushMatrix
            Rotate:
                angle: self.myRotation
                origin: self.center
        canvas.after:
            PopMatrix
<Node>:
    Image: 
        id: node
#        source: "background.png"
        center: root.center
        size:root.mySize
        allow_stretch: True
        #keep_ratio: False
<Laser>:
    Image:
        id: laser
#        source: "images/red.png"
        center: root.center
        allow_stretch: True
        keep_ratio: False
<Wall>:
    Image:
        id: wall
        center: self.center
        keep_ratio: False
        allow_stretch: True
<Enter_Animation>:
    Image:
        size: root.size
        source: "images/grey1.PNG"
        allow_stretch: True
        keep_ratio: False
    BoxLayout:
        size: (10,10)
        size_hint: (1,1)
        id: animation
        Image:
            size: (100,100)
            size_hint: (1,1)
            id: boy
            keep_ratio: False
            allow_stretch: True
            myRotation: 45
            source: "images/grey2.PNG"
            canvas.before:
                PushMatrix
                Rotate:
                    angle: self.myRotation
                    origin: self.center
            canvas.after:
                PopMatrix
""")
Window.size = (592, 288)
ratio_y = Window.height/144.
ratio_x = Window.width/296.
class levelBuilder():
    def __init__(self):
        self.nodeList = []
        self.wallList = []
        self.laserList = []
    def makeNode(self, listy):
        x = int(listy[0][0])
        y = int(listy[0][1])
        radius = int(listy[0][2])
        return Node(x,y,radius, listy[1])
    def makeWall(self, listy):
        w = int(listy[0][0])
        x = int(listy[0][1])
        y = int(listy[0][2])
        z = int(listy[0][3])
        r = int(listy[0][4])
        return Wall(w,x,y,z,r, listy[1])
    def makeLaser(self, listy):
        w = int(listy[0][0])
        x = int(listy[0][1])
        y = int(listy[0][2])
        z = int(listy[0][3])
        return Laser(w,x,y,z, listy[1])
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
    def string_to_list_screen(self, string, z):
        myList = []
        for x in string.split(","):
            myList.append(x)
        return myList, z
    def parseList(self,listy):
        returnList = []#list of faces
        for x in range(len(listy)):
            nodelist = []
            walllist = []
            laserlist = []
            lists = listy[x].split("|")
            for node in lists[0].split(";"):
                if node is not "":
                    nodelist.append(self.makeNode(self.string_to_list_screen(node, x)))
            for wall in lists[1].split(";"):
                if wall is not "":
                    walllist.append(self.makeWall(self.string_to_list_screen(wall, x)))
            for laser in lists[2].split(";"):
                if laser is not "":
                    laserlist.append(self.makeLaser(self.string_to_list_screen(laser, x)))
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
        self.color_list = ["images/grey1.PNG", "images/grey2.PNG"]
        self.color = 0
        super(Player, self).__init__(**kwargs)
        self.spin_direction = 1
        self.start_center = [Window.width/2,Window.height/2]
        self.finish_node = None
        self.nodelist = nodelist
        self.laserlist = laserlist
        self.walllist = walllist
        self.restart()
        self.node = None
        self.inc = .07
        self.finished = False
        self.size = self.mySize
    def set_lists(self, listy):
        self.nodelist = listy[0]
        self.walllist = listy[1]
        self.laserlist = listy[2]
    def update(self, dt):
        self.spin()
        if not self.node:
            self.checkNode()
        self.updatePos()
    def spin(self):
        self.ids["player"].myRotation+=4*self.spin_direction
    def inBound(self):
        if self.center_x <= 0:
            self.parent.change_face(3)
        elif self.center_y <= 0:
            self.parent.change_face(2)
        elif self.center_x >= Window.width:
            self.parent.change_face(1)
        elif self.center_y >= Window.height: 
            self.parent.change_face(0)
    def updatePos(self):
        self.inBound()
        if self.node == None:
            self.x +=self.velocity[0]*ratio_x
            self.y +=self.velocity[1]*ratio_y
        else:
            self.angle += self.inc*self.direction
            self.center_x = self.node.center_x + self.node.radius*cos(self.angle)
            self.center_y = self.node.center_y + self.node.radius*sin(self.angle)
    def calcAngle(self):
        ydif = (float)(self.node.center_y - self.center_y)
        xdif = (float)(self.node.center_x - self.center_x)
        if xdif == 0:
            xdif = 1
        angle = atan(ydif/xdif)
        if self.node.center_x > self.center_x:
            angle += pi
        distanceX = self.center_x - self.node.center_x
        distanceY = self.center_y - self.node.center_y
        if distanceX*self.velocity[1]/self.velocity[0]>distanceY: # if projected to be below node 
            if self.velocity[0] > 0:
                self.direction = 1
                self.spin_direction = 1
            else:
                self.direction = -1
                self.spin_direction = -1
        else:
            if self.velocity[0] > 0:
                self.direction = 1
                self.spin_direction = 1
            else:
                self.direction = -1
                self.spin_direction = -1
            
        return angle
    def checkNode(self):
        for x in range(len(self.nodelist)):
            distance = sqrt(pow(self.center_y - self.nodelist[x].center_y, 2) + 
                    pow(self.center_x - self.nodelist[x].center_x, 2))
            if (distance <= self.nodelist[x].radius and self.nodelist[x] != self.last_node):
                self.node = self.nodelist[x]
                self.node.transform("current")
                if self.last_node:
                    self.last_node.transform("revert")
                self.last_node = self.nodelist[x]
                if self.node == self.finish_node:
                    self.finished = True
        for x in range(len(self.laserlist)):
            if x<len(self.laserlist) and self.laserlist[x].ids["laser"].collide_widget(self):
                self.parent.ids["sm"].current = "0"
                if self.last_node:
                    self.last_node.transform("revert")
                self.restart()
        for x in range(len(self.walllist)):
            if x<len(self.walllist) and self.walllist[x].ids["wall"].collide_widget(self) and (time.time()-self.lastWall[1]>.1): # COLLIDE
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
        self.inc = .07
        if self.node:
            lAngle = self.angle + (pi/2.)*self.direction
            x = self.node.radius*cos(lAngle)
            y = self.node.radius*sin(lAngle)
            ratio = sqrt(pow(x, 2) + pow(y,2))
            if self.center_x<self.node.center_x: # 2+3
                if self.center_y>self.node.center_y: #2
                    xDir = -1*self.direction
                    yDir = -1*self.direction
                else: #3
                    xDir = self.direction
                    yDir = -1*self.direction
            else: #1+4
                if self.center_y>self.node.center_y:#1
                    xDir = -1*self.direction
                    yDir = self.direction
                else: #4
                    yDir = self.direction
                    xDir = self.direction

            self.velocity = [abs(2*x/ratio)*xDir, abs(2*y/ratio)*yDir]
            self.node = None
    def restart(self, *args):
        self.last_node = None
        self.node = None
        self.angle = None
        self.speed = 12
        self.velocity = [3.,0]
        self.center = self.start_center
        self.direction = 1
        self.lastWall = [None, 0]
        self.color = 0
        self.ids["player"].source = "images/grey1.PNG"
        if self.parent:
            self.parent.start_time = time.time()
            self.set_lists(self.parent.faces[int(self.parent.ids["sm"].current)])
    def setCenter(self, x, y):
        self.center = (x,y)
class Node(Widget):
    def __init__(self,x,y,radius, screen, **kwargs):
        self.color_list = ["images/grey1.PNG", "images/grey2.PNG"]
        self.current_list = ["images/current2.png", "images/current1.png"]
        self.end_list = ["images/end1.png", "images/end2.png"]
        self.mySize = [4*ratio_x, 4*ratio_y]
        super(Node, self).__init__(**kwargs)
        self.ids["node"].source = self.color_list[int(screen)]
        self.radius = radius*ratio_x
        self.center = (x*ratio_x, y*ratio_y)
        self.used = False
        self.screen = screen
    def transform(self, img):
        if img == "end":
            self.ids["node"].source = "images/end1.png"
        if img == "current":
            self.ids["node"].source = self.current_list[abs(int(self.screen)-1)]
        if img == "revert":
            self.ids["node"].source = self.color_list[int(self.screen)]
class Wall(Widget):
    def __init__(self,x, y, size_x, size_y, angle, screen, **kwargs):
        self.angle = angle
        self.color_list = ["images/grey1.PNG", "images/grey2.PNG"]
        super(Wall, self).__init__(**kwargs)
        self.ids["wall"].source = self.color_list[int(screen)]
        self.ids["wall"].width = size_x*ratio_x
        self.ids["wall"].height = ratio_y*size_y
        self.ids["wall"].center = (x*ratio_x, y*ratio_y)
        #self.ids["wall"].keep_ratio = False
        #self.ids["wall"].allow_stretch = True
        #self.canvas.add()
class Laser(Widget):
    def __init__(self,x, y, size_x, size_y, screen, **kwargs):
        super(Laser, self).__init__(**kwargs)
        self.color_list = ["images/grey2.PNG", "images/grey1.PNG"]
        self.texture_list = ["images/spike1.png", "images/spike2.png"]
        self.ids["laser"].source = self.color_list[int(screen)]
        self.ids["laser"].width = size_x*ratio_x
        self.ids["laser"].height = ratio_y*size_y
        self.center = (x*ratio_x, y*ratio_y)
        with self.canvas:
            #Color(.4, .4, .4, 1)
            texture = CoreImage(self.texture_list[screen]).texture
            texture.wrap = 'repeat'
            nx = size_x/5
            ny = size_y/5
            Rectangle(size=(size_x*ratio_x,size_y*ratio_y), pos=(x*ratio_x-size_x*ratio_x/2,y*ratio_y-size_y*ratio_y/2),texture=texture,
                      tex_coords=(0, 0, nx, 0, nx, ny, 0, ny))
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
    def __init__(self, level, **kwargs):
        self.color = 0
        self.color_list = ["images/grey1.PNG","images/grey2.PNG"]
        super(Cube, self).__init__(**kwargs)    
        self.builder = levelBuilder()
        self.level = level
        self.face_guide = [[3,2,1,4],[0,2,5,4],[0,3,5,1],[0,4,5,2],[0,1,5,3],[1,2,3,4]]
        self.faces = self.builder.return_level(level) # list of lists for gamelayout (nodelist, etc.)
        for x in range(2):
            self.ids["layout" + str(x)].set_lists(self.faces[x][0], self.faces[x][1],self.faces[x][2])
        self.ids["layout0"].loadLevel()
        self.myPlayer = Player(self.faces[0][0], self.faces[0][1],self.faces[0][2])
        self.myPlayer.start_center = self.myPlayer.nodelist[0].center
        self.myPlayer.finish_node = self.myPlayer.nodelist[-1]
        self.myPlayer.finish_node.transform("end")
        self.myPlayer.center = self.myPlayer.start_center
        self.add_widget(self.myPlayer)
        Clock.schedule_interval(self.update, 1/60.)
        self.dir_list = ["down","left","up","right"]
        self.finish_anim_count = 0
        self.max_level = 12
        self.start_time = time.time()
    def update(self, dt):
        self.myPlayer.update(dt)
        if self.myPlayer.finished:
            self.finished()
    def finished(self):
        Clock.unschedule(self.update)
        Clock.schedule_interval(self.finish_anim, 1/30.)
        Clock.schedule_once(self.unschedule_finish_anim, .25)
        self.write_times()
        self.popup_layout = BoxLayout(orientation = "horizontal", size_hint = (.5,1))
        self.star_screen = BoxLayout()
        self.star_screen.add_widget(Label(text = self.star_label(), valign = "center", halign = "center"))
        self.finish_layout = BoxLayout(orientation = "vertical")
        self.finish_layout.add_widget(Button(text = "Restart", on_release = self.restart_level, size_hint = (1, 1)))
        self.finish_layout.add_widget(Button(text = "Levels", on_release = self.select_level, size_hint = (1, 1)))
        self.finish_layout.add_widget(Button(text = "Next", on_release = self.next_level, size_hint = (1, 1)))
        self.popup_layout.add_widget(self.star_screen)
        self.popup_layout.add_widget(self.finish_layout)
        self.finish_popup = Popup(content = self.popup_layout, title = "Menu", size_hint= (.9,.9))
        with open("current.txt","r") as file: 
            self.level_holder = int(file.read())
            file.close()
        if  self.level_holder < self.level and self.level is not self.max_level:
            with open("current.txt", "w") as file:
                file.write(str(self.level))
                self.parent.parent.parent.unlocked_level = self.level
                self.parent.parent.parent.make_menu()
                file.close()
    def star_label(self):
        if float(self.stars) < float(self.goal):
            return "Your time of " + str(float(self.stars)) + " seconds\nhas beaten the challenge time of \n" + str(self.goal) + " seconds"
        else:
            return "Your time of " + str(float(self.stars)) + " seconds\nhas not beaten the challenge time of \n" + str(self.goal) + " seconds"
    def write_times(self):
        with open("stars.txt", "r") as file:
            self.text = file.read()
        with open("goals.txt","r") as file: 
            self.goal = file.read()[(self.level-1)*3+1:(self.level-1)*3+3]
        with open("stars.txt", "w") as file:
            self.last_stars = self.text[(self.level-1)*5+1:(self.level-1)*5+5]
            self.stars = str(round(time.time() - self.start_time, 1))
            if float(self.stars) < 10:
                self.stars = "0" + self.stars
            if float(self.stars) > 99:
                self.stars = "99.9"
            if float(self.stars) < self.last_stars:
                file.write(self.text[0:(self.level-1)*5+1] + self.stars + self.text[(self.level-1)*5+5::])
                if self.parent:
                    self.parent.parent.parent.challenges_beaten.append(self.level)
    def finish_anim(self, dt):
        self.myPlayer.center_x -= (self.myPlayer.center_x - self.myPlayer.finish_node.center_x)*.3
        self.myPlayer.center_y -= (self.myPlayer.center_y - self.myPlayer.finish_node.center_y)*.3
    def unschedule_finish_anim(self, dt):
        Clock.unschedule(self.finish_anim)
        self.finish_popup.open()
    def restart_level(self, obj):
        self.finish_popup.dismiss()
        self.parent.parent.parent.restart_level()
        self.start_time = time.time()
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
            self.myPlayer.setCenter(self.myPlayer.center_x, self.myPlayer.ids["player"].height/2)
        if direction == 1:
            self.myPlayer.setCenter(self.myPlayer.ids["player"].width/2, self.myPlayer.ids["player"].center_y)
        if direction == 2:
            self.myPlayer.setCenter(self.myPlayer.center_x, Window.height-self.myPlayer.ids["player"].height/2)
        if direction == 3:
            self.myPlayer.setCenter(Window.width-self.myPlayer.ids["player"].width/2, self.myPlayer.center_y) 
        self.myPlayer.color = abs(self.myPlayer.color-1)
        self.myPlayer.ids["player"].source = self.myPlayer.color_list[self.myPlayer.color]
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.parent.parent.parent.back()
            Clock.unschedule(self.update)
        else:
            self.myPlayer.on_touch_down(touch)
class Menu(Widget):
    def __init__(self,**kwargs):
        self.max_level = 12
        self.window_height = Window.height
        super(Menu, self).__init__(**kwargs)
        self.challenges_beaten = []
        with open("current.txt","r") as file:
            self.unlocked_level = int(file.read())
            file.close()
        self.make_menu()
        self.current_level = 0
    def make_menu(self):
        self.ids["grid"].clear_widgets() 
        myLayout = GridLayout(cols = 1, size_hint_y = None)
        myLayout.height = Window.height/4*(self.unlocked_level+1)
        background_colors = ["images/grey1.PNG", "images/grey2.PNG"]
        for x in range(self.max_level):
            if x <= self.unlocked_level:
                if self.level_button_color(x) and not (x+1) in self.challenges_beaten:
                    self.ids["grid"].add_widget(Button(bold = True, text = str(x+1), on_release = self.intro))#self.press
                else:
                    self.ids["grid"].add_widget(Button(bold = True, text = str(x+1), on_release = self.intro, color = [1,1,1,1], background_color = [1,1,1,.75]))
            if x > self.unlocked_level:
                self.ids["grid"].add_widget(Button(text = "Locked"))
    def level_button_color(self, level):
        with open("goals.txt","r") as file: 
            self.goal = file.read()[level*3+1:level*3+3]
            file.close()
        with open("stars.txt","r") as file: 
            self.star_current = file.read()[(level)*5+1:(level)*5+5]
            file.close()
        if self.goal<self.star_current:
            return True
        return False
    def intro(self, obj):
        self.ids["sm"].current = "game"
        self.ids["game"].clear_widgets()
        self.ids["game"].add_widget(Enter_Animation())
        Clock.schedule_once(self.fade, 1.95)
        Clock.schedule_once(self.fade, 2.95)
        Clock.schedule_once(partial(self.tutorial_check, obj), 3)
    def tutorial_check(self, obj, dt):
        if int(obj.text) == 1:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "Tap on the screen to release the square.\nAim for the x-shaped endpoint.\nAvoid the checkered lines.", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 2:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "Each Stage has two screens.\nYou can switch between them.", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 3:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "From here on out the levels get a lot harder.\nI'm sorry.\nTo beat the challenge times you will need optimal routes.", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 4:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "You can bounce off walls.\nWalls are solid.\nDouble tap to exit to the menu.", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 5:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "I'm honestly impressed you made it this far.\nYou're almost halfway there.", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 6:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "I'll be honest I couldn't complete this level.\nBut I have complete faith in you.", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 7:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "Good News: it's mostly downhill from here.\nBad News: Arguably the second hardest level in the game.", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 8:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "This should be an easy one.\nIf you get stuck, double tap to exit to the main menu", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 9:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "Two ways.\nUp or Left.", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 10:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "Look for the easiest route.", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 11:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "The hardest level in the game.\nInspired by my good friend Trenton Nguyen.", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        elif int(obj.text) == 12:
            self.ids["sm"].current = "tutorial"
            self.ids["tutorial_box"].clear_widgets()
            self.tutorial = Button(text = "You made it!\nCongrats!", background_color = (.5,1,1,.2), on_press = partial(self.tutorial_to_game, obj))
            self.ids["tutorial_box"].add_widget(self.tutorial)
        else:
            self.tutorial_to_game(obj, 1)
    def tutorial_to_game(self, obj, dt):
        self.press_setup(obj, 1)
        self.ids["sm"].current = "game"
    def press_setup(self, obj, dt):
        self.ids["game"].clear_widgets()
        self.ids["game"].add_widget(Cube(int(obj.text)))
        self.current_level = int(obj.text)
    def press_setup2(self, lvl, obj):
        self.ids["game"].clear_widgets()
        self.ids["game"].add_widget(Cube(lvl))
        self.current_level = lvl
        self.ids["sm"].transition = FadeTransition()
        self.ids["sm"].current = "white"
        Clock.schedule_once(self.fade, .9)
    def fade(self, dt):
        if self.ids["sm"].current == "game":
            self.ids["sm"].transition = FadeTransition()
            self.ids["sm"].duration = 4
            self.ids["sm"].current = "white"
        else:
            self.ids["sm"].current = "game"
            self.ids["sm"].transition = SlideTransition()
    def back(self):
        self.ids["sm"].current = "title"
        
    def restart_level(self):
        self.ids["game"].clear_widgets()
        self.ids["game"].add_widget(Cube(self.current_level))
    def select_level(self):
        self.ids["sm"].current = "levels"
        self.make_menu()
    def next_level(self):
        self.current_level +=1
        if self.current_level > self.max_level:
            self.current_level = 1
        #self.ids["game"].clear_widgets()
        #self.ids["game"].add_widget(Enter_Animation())
        #Clock.schedule_once(self.fade, 1.95)
        self.intro(Button(text = str(self.current_level)))
        #Clock.schedule_once(partial(self.press_setup, Button(text = str(self.current_level))), 2.1)
    def intro_release(self, obj):
        self.intro_popup.dismiss()
        self.ids["game"].clear_widgets()
        self.ids["game"].add_widget(Enter_Animation())
        Clock.schedule_once(self.fade, 1.95)
        Clock.schedule_once(partial(self.press_setup, Button(text = "1")), 2.1)
class Enter_Animation(Widget):
    def __init__(self, **kwargs):
        super(Enter_Animation, self).__init__(**kwargs)
        self.animate()
    def animate(self):
        Clock.schedule_interval(self.animation, 1/60.)
        Clock.schedule_once(self.unschedule, 2.5)
    def unschedule(self, dt):
        Clock.unschedule(self.animation)
    def animation(self, dt):
        self.ids["boy"].myRotation-=4
        self.ids["animation"].height=self.ids["boy"].myRotation/10. + 40
        self.ids["animation"].width=self.ids["boy"].myRotation/10. +40
        self.ids["animation"].center_x = Window.width/2 + (Window.width/2 + Window.width/1200.*self.ids["boy"].myRotation)*sin(self.ids["boy"].myRotation/90.)
        self.ids["animation"].center_y = Window.height/2 + (Window.height/2 + Window.height/1200.*self.ids["boy"].myRotation)*cos(self.ids["boy"].myRotation/90.)
class Tutorial(Widget):
    def __init__(self, str, **kwargs):
        super(Tutorial, self).__init__(**kwargs)
        self.ids["label"].text = str
class TestApp(App):
    def build(self):
        return Menu()
if __name__ == '__main__':
    TestApp().run()
