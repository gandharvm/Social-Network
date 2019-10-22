class menuItem:
    def __init__(self,title,index): 
        self.title = title
        self.index = index 
    def __str__(self):
        return(""+self.title)