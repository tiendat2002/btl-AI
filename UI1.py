import pygame
import sys
import math
import queue
import tkinter as tk
from tkinter import filedialog
import datetime
u = True
bf = False
root = tk.Tk()
root.withdraw()

pygame.init()
objects = []
font = pygame.font.SysFont("Times New Roman", 15)


class point:
    def __init__(self, x, y, old=None):
        self.x = x
        self.y = y
        self.G = 0
        self.H = 0
        self.old = old
#

    def __gt__(self, other):
        if self.G+self.H > other.G+other.H:
            return True
        else:
            return False


class smallBox:
    baseColor = (255, 255, 255)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        pygame.draw.rect(window, self.baseColor, (self.x, self.y, 5, 5))

    def change(self, state):
        if state == 'base':
            self.baseColor = (255, 255, 255)
        elif state == 'obs':
            self.baseColor = (34, 59, 245)  # màu của chướng ngoại vật
        elif state == 'sta':
            self.baseColor = (162, 50, 168)  # màu của điểm xuất phát
        elif state == 'dis':
            self.baseColor = (255, 0, 0)  # màu của đích
        elif state == 'check':
            self.baseColor = (245, 245, 34)  # màu của các ô đang tìm
        elif state == 'road':
            self.baseColor = (224, 123, 57)  # màu của tuyến đường tốt nhất
        elif state == 'uncheck':
            self.baseColor = (0, 255, 0)  # màu của ô đang chờ xét duyệt
        elif state == 'begin':
            self.baseColor =(0,0,0)


class makeMatrix:
    def __init__(self, size, margin):
        self.matrix = []
        self.size = size
        self.margin = margin
        self.start = None
        self.end = None
        self.n = size[0]/5
        self.m = size[1]/5
        self.E = [[0 for i in range(0, size[1]//5)]
                  for i in range(0, size[0]//5)]
        self.sets = queue.PriorityQueue()
        self.queue = queue.Queue()
        self.stack = []
        self.isFind = True
        for i in range(margin[0], size[0]+margin[0]+5, 5):
            b = []
            for j in range(margin[0], size[1]+margin[1]+5, 5):
                b.append(smallBox(i, j))
            self.matrix.append(b)

    def drawEnd(self, mousePos):
        x = (mousePos[0]-self.margin[0])//5
        y = (mousePos[1]-self.margin[1])//5
        self.matrix[x][y].change('dis')
        self.matrix[x][y].draw(window)
        self.end = point(x, y)
        self.E[x][y] = 0
        t = [1, 0, -1]
        for i in range(0, 3):
            for j in range(0, 3):
                self.E[x+t[i]][y+t[j]] = 0
                self.matrix[x+t[i]][y+t[j]].change('dis')
                self.matrix[x+t[i]][y+t[j]].draw(window)

    def drawStart(self, mousePos):
        # print(not self.start);
        # if self.sets.empty():
        #     k=self.sets.get();
        #     xo=k.x;
        #     yo=k.y;
        #     self.matrix[xo][yo].change('base')
        #     self.matrix[xo][yo].draw(window)
        #     self.E[xo][yo] = 0
        #     t = [1, 0, -1]
        #     for i in range(0, 3):
        #         for j in range(0, 3):
        #             self.E[xo+t[i]][yo+t[j]] = 0
        #             self.matrix[xo+t[i]][yo+t[j]].change('base')
        #             self.matrix[xo+t[i]][yo+t[j]].draw(window)
        x = (mousePos[0]-self.margin[0])//5
        y = (mousePos[1]-self.margin[1])//5
        self.matrix[x][y].change('sta')
        self.matrix[x][y].draw(window)
        self.start = point(x, y)
        self.E[x][y] = 0
        t = [1, 0, -1]
        for i in range(0, 3):
            for j in range(0, 3):
                self.E[x+t[i]][y+t[j]] = 0
                self.matrix[x+t[i]][y+t[j]].change('sta')
                self.matrix[x+t[i]][y+t[j]].draw(window)
        self.sets.put(self.start)
        self.stack.append(self.start)
        self.queue.put(self.start)

    def drawSE(self):
        self.matrix[self.start.x][self.start.y].draw(window)
        self.matrix[self.end.x][self.end.y].draw(window)
        xs = self.start.x
        ys = self.start.y
        xe = self.end.x
        ye = self.end.y
        t = [1, 0, -1]
        for i in range(0, 3):
            for j in range(0, 3):
                self.matrix[xs+t[i]][ys+t[j]].change('sta')
                self.matrix[xs+t[i]][ys+t[j]].draw(window)
                self.matrix[xe+t[i]][ye+t[j]].change('dis')
                self.matrix[xe+t[i]][ye+t[j]].draw(window)

    def draw(self, window, mousePos):
        x = (mousePos[0]-self.margin[0])//5
        y = (mousePos[1]-self.margin[1])//5
        self.matrix[x][y].change('obs')
        self.matrix[x][y].draw(window)
        self.E[x][y] = -1
        t = [1, 0, -1]
        for i in range(0, 3):
            for j in range(0, 3):
                self.E[x+t[i]][y+t[j]] = -1
                self.matrix[x+t[i]][y+t[j]].change('obs')
                self.matrix[x+t[i]][y+t[j]].draw(window)

    def drawReset(self, window):
        for i in range(0, self.size[0]//5):
            for j in range(0, self.size[1]//5):
                self.matrix[i][j].change('base')
                self.matrix[i][j].draw(window)
        self.start = None
        self.end = None
        self.E = [[0 for i in range(0, size[1]//5)]
                  for i in range(0, size[0]//5)]
        self.sets = queue.PriorityQueue()
        self.queue = queue.Queue()
        self.stack = list()
        self.isFind = True
        for i in range(margin[0], size[0]+margin[0]+5, 5):
            b = []
            for j in range(margin[0], size[1]+margin[1]+5, 5):
                b.append(smallBox(i, j))
            self.matrix.append(b)

    def drawF(self, window, borderWid):
        for i in range(0, self.size[0]+2*borderWid):
            pygame.draw.rect(window, (244, 164, 96),
                             (i+self.margin[0]-borderWid, self.margin[1]-borderWid, 1, borderWid))
            pygame.draw.rect(window, (244, 164, 96),
                             (i+self.margin[0]-borderWid, self.margin[1]+self.size[1], 1, borderWid))
            for j in range(0, self.size[1]+2*borderWid):
                pygame.draw.rect(window, (244, 164, 96),
                                 (self.margin[0]-borderWid, j+self.margin[1]-borderWid, borderWid, 1))
                pygame.draw.rect(window, (244, 164, 96),
                                 (self.margin[0]+self.size[0], j+self.margin[1]-borderWid, borderWid, 1))
        for i in range(0, self.size[0]//5):
            for j in range(0, self.size[1]//5):
                self.matrix[i][j].draw(window)
    def drawNew(self,window,borderWid):
        for i in range(0, self.size[0]+2*borderWid):
            pygame.draw.rect(window, (0,0,0),
                             (i+self.margin[0]-borderWid, self.margin[1]-borderWid, 1, borderWid))
            pygame.draw.rect(window, (0,0,0),
                             (i+self.margin[0]-borderWid, self.margin[1]+self.size[1], 1, borderWid))
            for j in range(0, self.size[1]+2*borderWid):
                pygame.draw.rect(window, (0,0,0),
                                 (self.margin[0]-borderWid, j+self.margin[1]-borderWid, borderWid, 1))
                pygame.draw.rect(window, (0,0,0),
                                 (self.margin[0]+self.size[0], j+self.margin[1]-borderWid, borderWid, 1))
        for i in range(0, self.size[0]//5):
            for j in range(0, self.size[1]//5):
                self.matrix[i][j].change('begin');
                self.matrix[i][j].draw(window)

    def solve(self, window):  # phần giải quyết vấn đề bfs
        if not self.start or not self.end:
            return
        self.drawSE()
        global u, bf
        if self.isFind == False:
            return
        p1 = [0, 0, 1, -1]
        p2 = [1, -1, 0, 0]
        if (self.queue.empty()):
            bf = False
            u = True
            return
        k = self.queue.get()
        self.matrix[k.x][k.y].change('check')
        self.matrix[k.x][k.y].draw(window)
        for i in range(4):
            x = k.x+p1[i]
            y = k.y+p2[i]
            if x < 0 or x >= self.n:
                continue
            if y < 0 or y >= self.m:
                continue
            if self.E[x][y] == -1:
                continue
            temp = point(x, y, k)
            temp.G = k.G + 1
            temp.H = math.sqrt(pow(x-self.end.x, 2)+pow(y-self.end.y, 2))
            self.E[x][y] = -1
            self.queue.put(temp)
            self.matrix[x][y].change('uncheck')
            self.matrix[x][y].draw(window)
            if temp.H == 0:
                self.isFind = False
                while temp is not None:
                    self.matrix[temp.x][temp.y].change('road')
                    self.matrix[temp.x][temp.y].draw(window)
                    temp = temp.old
                bf = False
                u = True
                self.matrix[self.start.x][self.start.y].draw(window)
                self.matrix[x][y].change('dis')
                self.matrix[x][y].draw(window)

    def solve1(self, window):  # phần giải quyết vấn đề dfs
        if not self.start or not self.end:
            return
        self.drawSE()
        global u, bf
        if self.isFind == False:
            return
        if (self.sets.empty()):
            bf = False
            u = True
            return

    def solve2(self, window):  # phần giải quyết vấn đề a*
        if not self.start or not self.end:
            return
        self.drawSE()
        global u, bf
        if self.isFind == False:
            return
        p1 = [0, 0, 1, -1]
        p2 = [1, -1, 0, 0]
        if (self.sets.empty()):
            bf = False
            u = True
            return
        k = self.sets.get()
        self.matrix[k.x][k.y].change('check')
        self.matrix[k.x][k.y].draw(window)
        t = point(-10, -10)
        for i in range(4):
            x = k.x+p1[i]
            y = k.y+p2[i]
            if x < 0 or x >= self.n:
                continue
            if y < 0 or y >= self.m:
                continue
            if self.E[x][y] == -1:
                continue
            temp = point(x, y, k)
            temp.G = k.G + 1
            temp.H = math.sqrt(pow(x-self.end.x, 2)+pow(y-self.end.y, 2))
            self.E[x][y] = -1
            self.sets.put(temp)
            self.matrix[x][y].change('uncheck')
            self.matrix[x][y].draw(window)
            if temp.H == 0:
                self.isFind = False
                while temp is not None:
                    self.matrix[temp.x][temp.y].change('road')
                    self.matrix[temp.x][temp.y].draw(window)
                    temp = temp.old
                bf = False
                u = True
                self.matrix[self.start.x][self.start.y].draw(window)
                self.matrix[x][y].change('dis')
                self.matrix[x][y].draw(window)

    def solve3(self, window):  # phần giải quyết vấn đề dijkstra
        if not self.start or not self.end:
            return
        self.drawSE()
        global u, bf
        if self.isFind == False:
            return
        if (self.sets.empty()):
            bf = False
            u = True
            return


class RadioButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, font, text):
        super().__init__()
        self.text = text
        text_surf = font.render(text, True, (0, 0, 0))
        self.button_image = pygame.Surface((w, h))
        self.button_image.fill((255, 255, 255))
        self.button_image.blit(
            text_surf, text_surf.get_rect(center=(w // 2, h // 2)))
        self.hover_image = pygame.Surface((w, h))
        self.hover_image.fill((96, 96, 96))
        self.hover_image.blit(
            text_surf, text_surf.get_rect(center=(w // 2, h // 2)))
        pygame.draw.rect(self.hover_image, (96, 196, 96),
                         self.hover_image.get_rect(), 3)
        self.clicked_image = pygame.Surface((w, h))
        self.clicked_image.fill((96, 196, 96))
        self.clicked_image.blit(
            text_surf, text_surf.get_rect(center=(w // 2, h // 2)))
        self.image = self.button_image
        self.rect = pygame.Rect(x, y, w, h)
        self.clicked = False
        self.buttons = None

    def setRadioButtons(self, buttons):
        self.buttons = buttons

    def update(self, event_list):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hover and event.button == 1:
                    for rb in self.buttons:
                        rb.clicked = False
                    self.clicked = True
        self.image = self.button_image
        if self.clicked:
            self.image = self.clicked_image
        elif hover:
            self.image = self.hover_image


class button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

        objects.append(self)

    def process(self, window, mousePos):
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        window.blit(self.buttonSurface, self.buttonRect)


class label():
    def __init__(self, x, y, width, height, buttonText='Button'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.buttonText = buttonText
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

    def process(self, window):
        self.buttonSurf = font.render(self.buttonText, True, (20, 20, 20))
        self.buttonSurface.fill(self.fillColors['normal'])
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        window.blit(self.buttonSurface, self.buttonRect)

#init 
pygame.init()
size = (1000, 700)
window = pygame.display.set_mode(size)
isRunning = True
algorithm = "bfs"
margin = (20, 20)
sizeMatrix = (size[0]-200, size[1]-50)
M = makeMatrix(sizeMatrix, margin)
# function:


def Play():
    global bf, M
    M.isFind = True
    bf = True


def Pause():
    global bf
    bf = False


def Reset():
    global bf, M, window
    M.isFind = False
    bf = False
    M.drawReset(window)

def ChooseFile():
    global M,window,sizeMatrix,size,buttonPlay,buttonPause,buttonReset,buttonChooseFile,labelTime,radioButtons,group;
    matrix=[];
    filePath = filedialog.askopenfile(
        mode='r', filetypes=(('text files', 'txt'),))
    while True:
        data = filePath.readline()
        if data == '':
            break
        matrix.append(data.strip());
    if matrix != []:
        h=len(matrix)*15;
        w=len(matrix[0])*15;
        size = (w+200,700);
        window = pygame.display.set_mode(size);
        buttonPlay = button(size[0]-150, 30, 100, 50, 'Bắt đầu', Play)
        buttonPause = button(size[0]-150, 100, 100, 50, 'Dừng lại', Pause)
        buttonReset = button(size[0]-150, 170, 100, 50, 'Đặt lại toàn bộ', Reset)
        buttonChooseFile = button(size[0]-150, 240, 100, 50, 'Chọn file', ChooseFile)
        labelTime = label(size[0]-150, 600, 150, 50, '00:00s')
        radioButtons = [
        RadioButton(size[0]-150, 310, 100, 50, font, "BFS"),
        RadioButton(size[0]-150, 380, 100, 50, font, "DFS"),
        RadioButton(size[0]-150, 450, 100, 50, font, "A*"),
        RadioButton(size[0]-150, 520, 100, 50, font, "Dijkstra")
        ]
        for rb in radioButtons:
            rb.setRadioButtons(radioButtons)
        radioButtons[0].clicked = True
        group = pygame.sprite.Group(radioButtons)
        M.drawNew(window,7);
        sizeMatrix=(w,h)
        M = makeMatrix(sizeMatrix,margin);
        M.drawF(window,7);
        print(matrix);
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j]=='1':
                    print((i,j));
                    y=i+(1+2*i);
                    x=j+(2*j+1);
                    M.E[x][y] = -1
                    t = [1, 0, -1]
                    for u in range(0, 3):
                        for v in range(0, 3):
                            M.E[x+t[u]][y+t[v]] = -1
                            M.matrix[x+t[u]][y+t[v]].change('obs')
                            M.matrix[x+t[u]][y+t[v]].draw(window)


    filePath.close()

# init values:


    # for i in range(1,w):
    #     for j in range(1,h):
    #         M.E[]
buttonPlay = button(size[0]-150, 30, 100, 50, 'Bắt đầu', Play)
buttonPause = button(size[0]-150, 100, 100, 50, 'Dừng lại', Pause)
buttonReset = button(size[0]-150, 170, 100, 50, 'Đặt lại toàn bộ', Reset)
buttonChooseFile = button(size[0]-150, 240, 100, 50, 'Chọn file', ChooseFile)
labelTime = label(size[0]-150, 600, 150, 50, '00:00s')
radioButtons = [
    RadioButton(size[0]-150, 310, 100, 50, font, "BFS"),
    RadioButton(size[0]-150, 380, 100, 50, font, "DFS"),
    RadioButton(size[0]-150, 450, 100, 50, font, "A*"),
    RadioButton(size[0]-150, 520, 100, 50, font, "Dijkstra")
]
for rb in radioButtons:
    rb.setRadioButtons(radioButtons)
radioButtons[0].clicked = True
group = pygame.sprite.Group(radioButtons)
# edit caption
pygame.display.set_caption(
    "Thuật toán tìm đường trong mê cung theo áp dụng A*")
logo = pygame.image.load('logo.png')
pygame.display.set_icon(logo)

# running:


def check(mouse):
    if mouse[0] > sizeMatrix[0]+margin[0]-10 or mouse[0] < margin[0] + 5:
        return False
    if mouse[1] > sizeMatrix[1]+margin[1]-10 or mouse[1] < margin[1] + 5:
        return False
    return True


M.drawF(window, 7)
while isRunning:
    # window.fill((255, 255, 255));
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            isRunning = False
    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    group.update(event_list)
    if keys[pygame.K_s] & check(mousePos):
        M.drawStart(mousePos)
    if keys[pygame.K_d] & check(mousePos):
        M.drawEnd(mousePos)
    if mouse[0] & check(mousePos):
        M.draw(window, mousePos)
    if (radioButtons[0].clicked):
        algorithm = radioButtons[0].text
    elif radioButtons[1].clicked:
        algorithm = radioButtons[1].text
    elif radioButtons[2].clicked:
        algorithm = radioButtons[2].text
    if bf:
        if (u):
            global t
            t = datetime.datetime.now()
            u = False
        if algorithm == "BFS":
            M.solve(window)
            if not u:
                tg = datetime.datetime.now()
            labelTime.buttonText = str(tg-t)
        elif (algorithm == "DFS"):
            M.solve1(window)
            if not u:
                tg = datetime.datetime.now()
            labelTime.buttonText = str(tg-t)
        elif algorithm == "A*":
            M.solve2(window)
            if not u:
                tg = datetime.datetime.now()
            labelTime.buttonText = str(tg-t)
        elif algorithm == "Dijkstra":
            M.solve3(window)
            if not u:
                tg = datetime.datetime.now()
            labelTime.buttonText = str(tg-t)

    for object in objects:
        object.process(window, mousePos)
    labelTime.process(window)
    group.draw(window)
    pygame.display.flip()
pygame.quit()
exit()
