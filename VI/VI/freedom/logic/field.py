class Field:
    WHITE_COLOR = 'white'
    BLACK_COLOR = 'black'
    def __init__(self,code):
        self.empty = True
        self.isWhiteColor = False
        self.code = code
    def isBlackColor(self):
        return not self.isWhiteColor
    def checkForCollor(self,color):
        if color == self.WHITE_COLOR:
            return self.isWhiteColor
        return not self.isWhiteColor
    def getColor(self):
        if(self.isWhiteColor):
            return self.WHITE_COLOR
        return self.BLACK_COLOR
    def is_empty(self):
        return self.empty == True