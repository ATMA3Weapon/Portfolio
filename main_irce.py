from twisted.application import internet, service
from twisted.internet import protocol, reactor, defer
from twisted.internet import threads
from twisted.enterprise import adbapi
from twisted.words.protocols import irc
import thread, sys, os, string, hashlib, time, datetime, MySQLdb

class IrceServer(protocol.Protocol):

    def connectionMade(self):
        global CurrentNickname, Users, ServerName
        ip, port = self.transport.client
        uPort = ip + ":" + str(port)
        
        #ip, port = self.transport.client
        print "Connection from: ", self.transport.client
        
        Users[uPort] = {}
        
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        global CurrentNickname, Users
        ip, port = self.transport.client
        uPort = ip + ":" + str(port)
        
        print "%s was removed from dictionary\n" % CurrentNickname
        del(Users[uPort])
        
        print "Disconnected from: ", self.transport.client
        self.factory.clients.remove(self)

    def addthread(self, act, prams):
        d = threads.deferToThread(act, prams)
        d.addCallback(self.result)

    def send(self, data):
        self.transport.write(data + "\n")

    def irc_ServerMessage(self, server, nick, message):
        return ":%s NOTICE %s :%s" % (server, nick, message)


    def NICK(self, nick):
        global CurrentNickname, Users
        
        ip, port = self.transport.client
        uPort = ip + ":" + str(port)
        
        nick = nick.strip(":,.\/ \n")
        oldnick = CurrentNickname
        
        if Users.has_key(nick):
            self.irc_NICK()
            #nickMessage = irc.IRCClient.  ":localhost 433 NOTICE %s :Nickname %s already in use." % (oldnick, nick)

        else:
            Users[uPort]['Nickname'] = nick
            CurrentNickname = nick
                
            print "%s was added to dictionary." % nick  
                
            if oldnick == "":
                nickMessage = ":localhost 433 NOTICE %s :Your nickname is now %s." % (nick, nick)
            else:                
                nickMessage = ":%s NICK %s" % (oldnick, nick)

        self.send(nickMessage)
        return True

    #def USER(self, username, hostname, servername, realname):
    #    test
    
    def dataReceived(self, data):
        data = data.strip("\n\r");
        x = data.split(" ")
        z = data.split(":")
        
        try:
            print data + "\n"
                
            if x[0] == "NICK":
                self.NICK(x[1])
                
            #if x[0] == "USER":
             #   self.USER(x[1], x[2], x[3], x[4])
            #if x[1] == "NICK": self.NICK(x[2], x[0])
            #if x[0] == "PONG": self.PONG()


        except IndexError:
            pass



class IrceServerFactory(protocol.ServerFactory):
    protocol = IrceServer
    clients = []
    
#        Username
CurrentNickname = ""
ServerName = ""

#        Ip address;  {Nickname: atma, modes: oaR, email: test@test.com, username: test, hostname: blah, servername: localhost, realname: test}
Users = {}
Channels = {"#chan1": {}}



#ircecommands = IrceCommands()
  
reactor.suggestThreadPoolSize(30)
application = service.Application("IrceServer")
appservice = internet.TCPServer(6667, IrceServerFactory())
appservice.setServiceParent(application)
    
