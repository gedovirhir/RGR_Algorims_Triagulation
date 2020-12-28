import clr
import random
import time
from math import ceil

clr.AddReference('System')
clr.AddReference('System.IO')
clr.AddReference('System.Drawing')
clr.AddReference('System.Reflection')
clr.AddReference('System.Threading')
clr.AddReference('System.Windows.Forms')

import System.IO
import System.Drawing as Dr
import System.Reflection
import System.Windows.Forms as WinForm
from System.Threading import ApartmentState, Thread, ThreadStart

#Cross checking
def area(a,b,c):
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)
def intersect_1(a,b,c,d):
    if a > b:
        a,b = b,a
    if c > d:
        c,d = d,c
    return max(a,c) <= min(b,d)
def intersect(a,b,c,d):
    if ((a.x == c.x and a.y == c.y) or (a.x == d.x and a.y == d.y)) != ((b.x == c.x and b.y == c.y) or (b.x == d.x and b.y == d.y)):
        return False
    return intersect_1(a.x, b.x, c.x, d.x) and intersect_1(a.y, b.y, c.y, d.y) and area(a,b,c) * area(a,b,d) <= 0 and area(c,d,a) * area(c,d,b) <= 0
class point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.prev = []
        self.next = []
class shape(object):
    def __init__(self, Point1, Point2):
        self.p1 = Point1
        self.p2 = Point2
class Graph(object):
    def __init__(self):
        self.points = []
        self.shapes = []
        self.observer = System.EventHandler
    def addPoint(self, point):
        self.points.append(point)

        self.observer.Invoke(self,None)
    def addShape(self, shape):
        self.shapes.append(shape)

        self.observer.Invoke(self, None)
    def drawAllPoints(self, flag, pen, Font):
        for i in self.points:
            flag.FillEllipse(Dr.Brushes.DeepSkyBlue,i.x-5,i.y-5,10,10)
            flag.DrawString(str(i.x)+","+str(i.y),Font,Dr.Brushes.Black, Dr.PointF(i.x-5,i.y-10))
        for i in self.shapes:
            flag.DrawLine(pen, i.p1.x,i.p1.y, i.p2.x, i.p2.y)
    def len(self):
        return len(self.points)
    def clear(self):
        self.points.clear()
        self.shapes.clear()
    def setPrev(self, p1, p2):
        p1.prev.append(p2)
        self.addShape(shape(p2,p1))
    def setNext(self, p1, p2):
        p1.next.append(p2)
        self.addShape(shape(p2,p1))
    def checkAv(self, p1, p2):
        for i in self.shapes:
            if intersect(p1,p2,i.p1,i.p2):
                return False
        return True
    def iterationOfNext(self, mas, el):
        for j in mas:
            if self.checkAv(j, el):
                self.setNext(el,j)
            self.iterationOfNext(j.next, el)
    def iterationOfPrev(self, mas, el):
        for j in mas:
            if self.checkAv(j, el):
                if len(el.next) == 0:
                    self.setNext(el,j)
                else:
                    self.setPrev(el,j)
            self.iterationOfPrev(j.prev, el)
    def createTriang(self):
        self.points.sort(key = lambda point: point.x)
        po = self.points
        lastAdd = self.points[0]
        if len(self.points) == 2:
            self.shapes.append(self.points[0], self.points[1])
        elif len(self.points) > 2:
            self.setPrev(po[2],po[1])
            self.setNext(po[2],po[0])
            self.setNext(po[1],po[0])
            lastAdd = po[2]

            for i in range(3, len(po)):
                self.setPrev(po[i], lastAdd)
                self.iterationOfNext(lastAdd.next, po[i])
                self.iterationOfPrev(lastAdd.prev, po[i])
                lastAdd = po[i]
                    


class form1(System.Windows.Forms.Form):
    def __init__(self):        
        self.Text = "form"
        self.BackColor = Dr.Color.FromArgb(238,238,238)
        self.ClientSize = Dr.Size(1800,900)
        caption_height = WinForm.SystemInformation.CaptionHeight
        self.MinimumSize =Dr.Size(392,(117 + caption_height))
        
        self.canvas = Dr.Bitmap(1, 1)
        self.flagGraphics = Dr.Graphics.FromImage(self.canvas)
        self.graph = Graph()
        self.graph.observer = System.EventHandler(self.drawObjects)

        self.drawPen = Dr.Pen(Dr.Brushes.DeepSkyBlue)
        self.drawPen.Color = Dr.Color.FromName("DeepSkyBlue")
        self.drawPen.Width = 1


        self.InitiliazeComponent()
        
    
    def run(self):
        WinForm.Application.Run(self)
    
    def InitiliazeComponent(self):
        self.components = System.ComponentModel.Container()
        self.ImagePB = WinForm.PictureBox()
        self.butt = WinForm.Button()
        self.TriangB = WinForm.Button()
        self.randomizePointsB = WinForm.Button()
        self.PointsCountTB = WinForm.TextBox()
        self.addPB = WinForm.Button()
        self.addPXTB = WinForm.TextBox()
        self.addPYTB = WinForm.TextBox()
        self.baton = WinForm.Button()

        self.ImagePB.Location = Dr.Point(10, 10)
        self.ImagePB.Size = Dr.Size(1300, 700)
        self.ImagePB.TabStop = False
        self.ImagePB.MouseDown += self.ImagePB_MouseDown

        self.butt.Location = Dr.Point(10, 720)
        self.butt.Size = Dr.Size(200, 50)
        self.butt.BackColor = Dr.Color.FromArgb(238,238,240)
        self.butt.Text = "Очистить"
        self.butt.UseVisualStyleBackColor = 0
        self.butt.FlatStyle = WinForm.FlatStyle.Flat
        self.butt.FlatAppearance.BorderSize = 0    
        self.butt.Click += self.butt_Click 

        self.addPB.Location = Dr.Point(10, 770)
        self.addPB.Size = Dr.Size(200, 50)
        self.addPB.BackColor = Dr.Color.FromArgb(238,238,240)
        self.addPB.Text = "Добавить: X Y"
        self.addPB.UseVisualStyleBackColor = 0
        self.addPB.FlatStyle = WinForm.FlatStyle.Flat
        self.addPB.FlatAppearance.BorderSize = 0  
        self.addPB.Click += self.addPB_Click 

        self.addPXTB.Location = Dr.Point(220, 770)
        self.addPXTB.Size = Dr.Size(50, 20)

        self.addPYTB.Location = Dr.Point(220, 800)
        self.addPYTB.Size = Dr.Size(50, 20)
        
        self.TriangB.Location = Dr.Point(220, 720)
        self.TriangB.Size = Dr.Size(200, 50)
        self.TriangB.BackColor = Dr.Color.FromArgb(238,238,240)
        self.TriangB.Text = "Произвести триангуляцию"
        self.TriangB.UseVisualStyleBackColor = 0
        self.TriangB.FlatStyle = WinForm.FlatStyle.Flat
        self.TriangB.FlatAppearance.BorderSize = 0
        self.TriangB.Click += self.TriangB_Click

        self.randomizePointsB.Location = Dr.Point(420, 720)
        self.randomizePointsB.Size = Dr.Size(200, 50)
        self.randomizePointsB.BackColor = Dr.Color.FromArgb(238,238,240)
        self.randomizePointsB.Text = "Создать точки случайно"
        self.randomizePointsB.UseVisualStyleBackColor = 0
        self.randomizePointsB.FlatStyle = WinForm.FlatStyle.Flat
        self.randomizePointsB.FlatAppearance.BorderSize = 0
        self.randomizePointsB.Click += self.randomizePointsB_Click   

        self.baton.Location = Dr.Point(420, 780)
        self.baton.Size = Dr.Size(200, 50)
        self.baton.BackColor = Dr.Color.FromArgb(238,238,240)
        self.baton.Text = "baton"
        self.baton.UseVisualStyleBackColor = 0
        self.baton.FlatStyle = WinForm.FlatStyle.Flat
        self.baton.FlatAppearance.BorderSize = 0
        self.baton.Click += self.baton_Click   

        self.PointsCountTB.Location = Dr.Point(645, 720)
        self.PointsCountTB.Size = Dr.Size(200, 50)
        self.PointsCountTB.Text = "20"
        
        self.Controls.Add(self.ImagePB)
        self.Controls.Add(self.butt)
        self.Controls.Add(self.TriangB)
        self.Controls.Add(self.randomizePointsB)
        self.Controls.Add(self.PointsCountTB)
        self.Controls.Add(self.addPB)
        self.Controls.Add(self.addPXTB)
        self.Controls.Add(self.addPYTB)
        self.Controls.Add(self.baton)
    def dispose(self):
        self.components.Dispose()
        WinForm.Form.Dispose(self)

    def ImagePB_MouseDown(self, sender, args):
        if args.Button == WinForm.MouseButtons.Right:
            self.graph.addPoint(point(args.X,args.Y))
        """
        elif args.Button == WinForm.MouseButtons.Left:
            if self.versh == -1:
                for i in range(self.n):
                    if (args.X<self.koortoch[i].X+10 and args.X>self.koortoch[i].X-10 and args.Y<self.koortoch[i].Y+10 and args.Y>self.koortoch[i].Y-10):
                        self.versh = i 
                        break
            else:
                toversh = -1
                for i in range(self.n):
                     if (args.X<self.koortoch[i].X+10 and args.X>self.koortoch[i].X-10 and args.Y<self.koortoch[i].Y+10 and args.Y>self.koortoch[i].Y-10):
                         toversh = i
                         break
                if (toversh != -1) and (self.versh != toversh):
                    drawPen.Width = 2
                    
                    flagGraphics.DrawLine(drawPen, self.koortoch[self.versh], self.koortoch[toversh])
                    self.DataGrid.Rows[self.versh].Cells[toversh].Value = 1
                    self.DataGrid.Rows[toversh].Cells[self.versh].Value = 1
                    self.versh = -1 

                    self.ImagePB.Image = self.canvas
            """
    def drawObjects(self, sender, args):
        self.ImagePB.Image = None
        self.canvas = Dr.Bitmap(self.ImagePB.Width, self.ImagePB.Height)
        self.flagGraphics = Dr.Graphics.FromImage(self.canvas)
        self.Font = Dr.Font(self.Font, Dr.FontStyle.Regular)
        self.graph.drawAllPoints(self.flagGraphics, self.drawPen, self.Font)

        self.ImagePB.Image = self.canvas
    def randomizePointsB_Click(self, sender, args):
        self.butt_Click(sender,args)
        for i in range(int(self.PointsCountTB.Text)):
            self.graph.addPoint(point(random.randint(30,self.ImagePB.Width-30), random.randint(30,self.ImagePB.Height-30)))
    def TriangB_Click(self, sender, args):
        self.graph.createTriang()
    def addPB_Click(self, sender, args):
        self.graph.addPoint(point(int(self.addPXTB.Text),int(self.addPYTB.Text)))

    def butt_Click(self, sender, args):
        self.ImagePB.Image = None
        self.graph.clear()
    def baton_Click(self, sender, args):
        a = [point(81,610),point(155,586),point(468,190),point(534,438),point(568,490),point(617,244),point(690,568), point(703,466), point(775, 68)]
        for i in a:
             self.graph.addPoint(i)

def form_thr():
    form = form1()

    WinForm.Application.Run(form)
    form.dispose()


if __name__ == '__main__':
    form_thr()
