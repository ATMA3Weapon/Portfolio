from OpenSSL import SSL
import sys

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import ssl, wxreactor, reactor


class EchoClient(LineReceiver):
    end="Bye-bye!"
    def connectionMade(self):
        self.sendLine("Hello, world!")
        self.sendLine("What a fine day it is.")
        self.sendLine(self.end)

    def connectionLost(self, reason):
        print 'SSL Connection lost'

    def dataReceived(self, data):
        print data

    def lineReceived(self, line):
        print "receive:", line
        if line==self.end:
            self.transport.loseConnection()

class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print "Connection Failed: "+ reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection Lost: "+ reason.getErrorMessage()
        reactor.stop()


def main():
    factory = EchoClientFactory()
    reactor.connectSSL('localhost', 54100, factory, ssl.ClientContextFactory())
    reactor.run()

if __name__ == '__main__':
    main()



 