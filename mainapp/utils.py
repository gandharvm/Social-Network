class menuItem:
    def __init__(self,title,index): 
        self.title = title
        self.index = index 
    def __str__(self):
        return(""+self.title)

menuListCasual=[]
menuListPremium=[]
menuListCommercial=[]

menuListCasual.append(menuItem("Send Friend request",1))
menuListCasual.append(menuItem("Accept a Friend request",2))
menuListCasual.append(menuItem("Decline a Friend request",3))
menuListCasual.append(menuItem("Unfriend someone",4))
menuListCasual.append(menuItem("Deposit money in wallet",5))
menuListCasual.append(menuItem("Send money request",6))
menuListCasual.append(menuItem("Accept a money request",7))
menuListCasual.append(menuItem("Decline a money request",8))
menuListCasual.append(menuItem("Post on your timeline",9))
menuListCasual.append(menuItem("Post on a friend's timeline",10))
menuListCasual.append(menuItem("Join a group",11))
menuListCasual.append(menuItem("Manage privacy settings",12))
menuListCasual.append(menuItem("View profile",13))
menuListCasual.append(menuItem("Upgrade account",14))


menuListPremium+=(menuListCasual)
menuListPremium.append(menuItem("Send private message",15))
menuListPremium.append(menuItem("Create a group",16))

menuListCommercial+=(menuListPremium)
menuListPremium.append(menuItem("Create commercial page",17))
