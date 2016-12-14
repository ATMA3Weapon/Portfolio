#!/usr/bin/env python

from OpenSSL import SSL
import wx, sys, os, string, cStringIO, time, threading
from wx import EVT_MENU, EVT_CLOSE
#import gms_ssl
import defs

from twisted.internet import wxreactor
wxreactor.install()

# import t.i.reactor only after installing wxreactor:
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import ssl, reactor

#
# Specail Variables

MenuCreated = False # if the menu has been created in taskbar


ID_GHOSTFRAME = wx.NewId()
ID_SPLASHFRAME = wx.NewId()
ID_FRAME = wx.NewId()

ID_LOGIN = wx.NewId()
ID_CONNE = wx.NewId()
ID_CONAM = wx.NewId()
ID_EXIT = wx.NewId()
ID_CLOSE = wx.NewId()

#prob = ''
#SSL Stuff
class EchoClient(LineReceiver, Protocol):
    
    def __init__(self):
        self.prob = self
    
    def connectionMade(self):
        print "Connection made"
        app.ChangeIcon_Green(defs.bizname)                                      # Change icon to green indicating that were connected to the server via SSL
        
        print "Sending client password to server"                               #create log data
        file = open('passwords/_password2')                                     #open a password file and set the object to 'file'
        file_read = file.read()                                                 #read file object 'file'
        
        self.sendLine("PASS " + file_read)                                      #Send password to server

        app.Splash_SetGauge(50)                                                 #Set gauge ahead another step to indicate progress 


    def dataReceived(self, data):
        x = data.split(" ")
        
        #initialization password check against server
        if MyApp.SSLConnected == False:
            if x[0] == "PASS":
                if x[1] == "Success":
                    MyApp.SSLConnected = True                                   # set connection to true allow user to login at this point
                    MyApp.ConnHash = x[2]                                       # set connection hash
                    MyApp.ConnTime = x[3]                                       # set connection time
                    
                    app.Splash_SetGauge(100)                                    # set gauge to 100% complete
                    app.OpenLogin()                                             # Once connected open up the login box
                    app.CloseSplash()                                           # Close the splash window
                    
                    print "Password Accepted"                                   # print log info
        
                if x[1] == "Failed":
                    print "Error Password not accepted"                         # Loging
                    
                    splitdata = data.split(",")                                 # split the data so we can grab the error message
                    ssl_error = splitdata[1]                                    # set data from list
                    
                    defs.errorMsg("Error, "+ ssl_error)                         # notify user      

        #if MyApp.SSLConnected == True:
            #if x[0] == "":
        #self.transport.write("m00")
        #print "FINALLY FUCKer " + str(self)
        #print data # Loging

    #@staticmethod
    def SendLogin(self, username, password, hash, time):
        #print "FINALLY FUCK " + str(self)
        #self.transport
        print self.prob
        print self
        self.transport.write("LOGIN "+username+" "+password+" "+hash+" "+time)
        #LineReceiver.sendLine("LOGIN "+username+" "+password+" "+hash+" "+time)

class EchoClientFactory(ClientFactory):
    def __init__(self):
        self.protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        app.ChangeIcon_Red(defs.bizname)                                        # Change taskbar icon to Red
        print "Connection Failed: "+ reason.getErrorMessage()                   # Print log info and get reason
        reactor.callLater(3, app.SSLConnect.SSL_Thread)                           # Wait 3 seconds before attempting to reconnect

    def clientConnectionLost(self, connector, reason):
        app.ChangeIcon_Red(defs.bizname)                                        # Change taskbar icon to Red
        print "Connection Lost: "+ reason.getErrorMessage()                     # Print log info and get reason
        reactor.callLater(3, app.SSLConnect.SSL_Thread)                           # Wait 3 seconds before attempting to reconnect


# Create definition for Creating connection to server
class SSLConnector():
    def __init__(self):
        self.factory = EchoClientFactory()                                                  #create client handler
    
    def SSL_Thread(self):
        reactor.connectSSL('76.20.172.30', 54100, self.factory, ssl.ClientContextFactory())  #connect to server via SSL  192.168.0.4
    
    #def SendLogin(self, username, password, hash, time):
        #self.factory.SendLogin(username, password, hash, time)
        #print str(self.factory.protocol)
        #self.factory.protocol.SendLogin(username, password, hash, time)

# Create taskbar icon and menus
class TaskBarMenu(wx.TaskBarIcon):
    def __init__(self, parent):
        wx.TaskBarIcon.__init__(self)  

        #setup icon object 
        self.taskbarIcon = wx.Icon("images/gms_icon.ico", wx.BITMAP_TYPE_ICO)     # Black icon, Connected + loged in
        self.taskbarIcon_r = wx.Icon("images/gms_icon_r.ico", wx.BITMAP_TYPE_ICO) # Red icon, Not connected to anything attempting to connect or idle
        self.taskbarIcon_g = wx.Icon("images/gms_icon_g.ico", wx.BITMAP_TYPE_ICO) # Green icon,  Connected but not logged in

        self.SetIcon_Red(defs.bizname)                                          # Set icon in taskbar to Red indicating not connected to the server or logged in
        self.CreateMenu_LoggedOut()                                             # Init menu for icon

    def CreateMenu_LoggedOut(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.ShowTaskbarMenu) 
        self.TaskbarMenu = wx.Menu()                                            # Create new menu 
        self.TaskbarMenu.Append(ID_LOGIN, "Login")                              # Create item "Login"
        self.TaskbarMenu.Append(ID_CONNE, "Connect to Server")                  # Create item "Connect to server"
        self.TaskbarMenu.Append(ID_CONAM, "Contact Admin")                      # Create item "Contact admin"
        self.TaskbarMenu.AppendSeparator()                                      # Create verticle bar
        self.TaskbarMenu.Append(ID_EXIT, "Quit")                                # Create Quit item
        
        EVT_MENU(self, ID_EXIT, self.ExitReactor)                               # Bind "Quit" to "ExitRecactor" 
        EVT_MENU(self, ID_LOGIN, self.ShowLogin)                                # Bind "Login" menu item to "ShowLogin"
        EVT_MENU(self, ID_CONNE, self.ConnectSSL)                               # Bind "Connect to Server" menu item to "ConnectLogin"
        
        # make sure reactor.stop() is used to stop event loop:
        EVT_CLOSE(self, lambda evt: reactor.stop())                             # Stops reactor properly before closing out program

    def CreateMenu_LoggedIn(self):                                              # Show this menu if your logged in
        return True

    # When someone right clicks the window popup the menu 
    def ShowTaskbarMenu(self, event):  
        self.PopupMenu(self.TaskbarMenu)                                        # Popup the menu  

    # Change the icon in taskbar to Black indicating user is connected and logged in
    def SetIcon_Normal(self, msg):
        self.SetIcon(self.taskbarIcon, msg)                                     # Change icon and set hover message

    # Change the icon in the taskbar to Green indicating user is connected but not logged in
    def SetIcon_Green(self, msg):
        self.SetIcon(self.taskbarIcon_g, msg)                                   # Change icon and set hover message
    
    def SetIcon_Red(self, msg):
        self.SetIcon(self.taskbarIcon_r, msg)                                   # Change icon and set hover message

    def ShowLogin(self, event):
        app.CreateLogin()
        app.OpenLogin()
    
    def ConnectSSL(self):
        if app.SSLConnected != True:
            SSLConnector.SSL_Thread()

    # Exit application 
    def ExitReactor(self, event):
        app.CloseApp()                                                          # Close the application properly

# GhostFrame: Hidden frame used to mediate commands between the taskbar icon and the rest of the program
class GhostFrame(wx.Frame):  
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title, size=(1, 1), style=wx.FRAME_NO_TASKBAR|wx.NO_FULL_REPAINT_ON_RESIZE)  
        self.tbicon = TaskBarMenu(self)
        self.Show(False)

    # Act as a mediator to change icon to "Normal" in "TaskBarMenu" class in the task bar
    def changeIcon_Normal(self, msg):
        self.tbicon.SetIcon_Normal(msg)                                         # Set icon and message

    # Act as a mediator to change icon to "Green" in "TaskBarMenu" class in the task bar
    def changeIcon_Green(self, msg):
        self.tbicon.SetIcon_Green(msg)                                          # Set icon and message

    # Act as a mediator to change icon to "Red" in "TaskBarMenu" class in the task bar
    def changeIcon_Red(self, msg):
        self.tbicon.SetIcon_Red(msg)                                            # Set icon and message
    
    # Change the menu style to "Loggedout" acting as a mediator to "TaskBarMenu" class
    def changeMenu_LoggedOut(self):
        self.tbicon.CreateMenu_LoggedOut()                                      # Create the logged out menu 

    # Destroy the icon on close 
    def DestroyIcon(self):
        self.tbicon.Destroy()                                                   # Destroy icon

 
# SplashFrame: The frame that pops up when program starts and initializes the connection
class SplashFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, (-1, -1), (500, 250), style=wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        
        # Background image
        imageFile = "images/splash.jpg"                                         # Location of the splash background
        data = open(imageFile, "rb").read()                                     # Create file object and open splash background image

        stream = cStringIO.StringIO(data)                                       # Turn file object and turn the data into a readable image form
        bmp = wx.BitmapFromImage(wx.ImageFromStream(stream))                    # Set stream as bitmap
        self.Loginheader = wx.StaticBitmap(self, -1, bmp, (0, 0), (500, 250))   # Create Bitmap place holder and bind BMP to it

        self.gauge = wx.Gauge(self, -1, 100, (100, 180), (300, 20))             # Create gauge bar for showing progress (even if its nothing lol)
        
        self.CentreOnScreen()                                                   # Center SplashFrame on users screen

    # Def to set Gauge position
    def setGauge(self, pos):
        self.gauge.SetValue(pos)                                                # Set position of guage 

class loginFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, (-1, -1), (350, 200), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)

        font1 = wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL)

        self.icon = wx.Icon("images/gms_icon.ico", wx.BITMAP_TYPE_ICO) 
        self.SetIcon(self.icon)

        imageFile = "images/login_banner.jpg"
        data = open(imageFile, "rb").read()

        stream = cStringIO.StringIO(data)
        bmp = wx.BitmapFromImage(wx.ImageFromStream(stream))
        self.Loginheader = wx.StaticBitmap(self, -1, bmp, (0, 0), (350, 50))


        UsernameFont = wx.StaticText(self, -1, "Username: ", (40, 76), (-1, -1))
        UsernameFont.SetFont(font1)
        self.UsernameCtrl = wx.TextCtrl(self, -1, '', (100, 73), (200, -1), style=wx.TE_LEFT)

        PasswordFont = wx.StaticText(self, -1, "Password: ", (40, 103), (10, 25))
        PasswordFont.SetFont(font1)
        self.PasswordCtrl = wx.TextCtrl(self, -1, '', (100, 98), (200, -1), style=wx.TE_LEFT|wx.PASSWORD) 


        self.loginButton  = wx.Button(self, 1, "Login", (80, 130), (80, 25))
        self.cancelButton = wx.Button(self, 2, "Cancel", (180, 130), (80, 25))


        self.Bind(wx.EVT_BUTTON, self.onLogin, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnCloseWindow, id=2)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)


        self.SetBackgroundColour("wx.LIGHT_GREY")
        self.CentreOnScreen()


    def OnCloseWindow(self, event):
        self.Destroy()

    def onLogin(self, event):
        if app.SSLConnected == True:
            username = self.UsernameCtrl.GetValue()
            password = self.PasswordCtrl.GetValue()
            
            if username != "":
                if password != "":
                    echocli = EchoClient()
                    echocli.SendLogin(username, password, app.ConnHash, app.ConnTime)
                    #app.SSLConnect.SendLogin(username, password, app.ConnHash, app.ConnTime)
 


class MyApp(wx.App):
    
    #set variables for global access
    SSLConnected = False   # if you are connected to the server or not
    ConnHash = ""          # hash key for saving info
    ConnTime = ""          # the epoch time when client connected to server
    
    def OnInit(self):

        self.CreateGhost()
        self.CreateSplash()
        self.CreateLogin()

        self.splashFrame.Show(True)
        
        self.CreateSSLConn()
        self.SSLConnect.SSL_Thread()   # Connect to server

        return True
    
    def CreateSSLConn(self):
        self.SSLConnect = SSLConnector()

    def CreateGhost(self):
        self.ghostFrame = GhostFrame(None, ID_GHOSTFRAME, "") # Create Ghostframe object
        self.ghostFrame.Show(False)                           # Show Ghostframe object
    
    def CreateSplash(self):
        self.splashFrame = SplashFrame(None, ID_SPLASHFRAME, defs.bizname) # Create Splashframe object
        self.splashFrame.Show(False)                                       # Show Splashframe object
    
    def CreateLogin(self):
        self.loginFrame = loginFrame(None, ID_FRAME, defs.bizname+" Login")
        self.loginFrame.Show(False)
        return True
    
    def ChangeIcon_Green(self, msg):
        self.ghostFrame.changeIcon_Green(msg)

    def ChangeIcon_Red(self, msg):
        self.ghostFrame.changeIcon_Red(msg)
    
    def Splash_SetGauge(self, pos):
        self.splashFrame.setGauge(pos)
    
    def CloseApp(self):
        reactor.stop()
        self.ghostFrame.DestroyIcon()
        sys.exit()
        
        return False

    def OpenLogin(self):
        self.loginFrame.Show(True)
    
    def CloseLogin(self):
        self.loginFrame.Show(False)
    
    def OpenSplash(self):
        self.splashFrame.Show(True)
    
    def CloseSplash(self):
        timer = threading.Timer(1.5, self.splashFrame.Show(False))

    

app = MyApp(0)

reactor.registerWxApp(app)

# start the event loop:
reactor.run()

app.MainLoop()






#wxreactor.registerWxApp(taskbarApp)
#wxreactor.run()




#tbicon = TaskBarMenu()





