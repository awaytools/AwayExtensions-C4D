# Custom Canvas-Class used to output the status of the plugin (Progess-Bar + Text-message)



import c4d
from c4d import gui
# this class is used in the "maindialog.py" 
class Canvas(gui.GeUserArea):

    # the object list supplied by the worker
    data = []

    # called on Redraw()
    def DrawMsg(self, x1, y1, x2, y2, msg):

        self.fontHeight = self.DrawGetFontHeight()
        self.OffScreenOn()

        self.DrawSetPen(c4d.COLOR_BG)
        self.DrawRectangle(0, 0, x2, y2)

        value = self.data[1]
        value2 = self.data[2]
        self.curWidth=int(value*x2)
        self.curWidth2=int(value2*self.curWidth)

        self.DrawSetTextCol(c4d.COLOR_TEXT, c4d.COLOR_TRANS)            
        self.SetClippingRegion(5, 5,x2-5,35)
        borderStyle=c4d.BORDER_BLACK
        if value>0:
            borderStyle=c4d.BORDER_ACTIVE_4
        self.DrawBorder(borderStyle, 5, 5,x2-5,35 - 1)

        self.DrawSetPen(c4d.Vector(0.5, 0, 0))
        
        if value>0:
            self.DrawRectangle(6, 6, 5 + self.curWidth - 11, 33)
            if value2>0:
                self.DrawSetPen(c4d.Vector(0.8,0, 0))
                self.DrawRectangle(6, 6, 5 + self.curWidth2 - 11, 33)

        self.DrawSetPen(c4d.COLOR_BG)
        self.DrawSetTextCol(c4d.COLOR_TEXT, c4d.COLOR_TRANS)
        self.DrawText(self.data[0], x2 / 2 - self.DrawGetTextWidth(self.data[0]) / 2, y2 / 2 - self.fontHeight / 2)

    # starts the redraw
    def draw(self, aData):

        self.data = aData
        self.Redraw()

