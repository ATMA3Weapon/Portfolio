""" 

  Stackless nerual net designed by Eric Blackburn (ATMA - ATMA3Weapon@gmail.com)
  
  Required modules 
   - Stackless python
  
  Simple model: 
  [ ] Each nerve will run independently from each other in a parallel sense.
  [ ] Each nerve holds its threshold, charge level, and the index's of its output nerves.
  [ ] Each nerve is a loop that waits for data from other nerves and checks if it's charge has meet the threshold. 
  [ ] Once a nerve has reached its threshold, it calculates its ouput energy levels and sends that information to the other nerves indicated by their index. Resets it's self to default charge of 0
  
  
  Rules for the EBNN:
  [ ] Nerve cells can have 1 to infinate number of outputs.
  [ ] Nerve cells can not output to them selves.
  [-] The strength of the connection between two nerves is indicated by an activity counter. 
  [ ] Nerve cells have a threshold they must meet and only then does it fire.
  [ ] The signal returned by a fired cell is the charge divided by the number of output connections.
  
  
  Math for EBNN: (not really that complicated)
  charge = sum(n1, n2, n3, xN)
  output = charge / (output list size)
  threshold =

"""

import stackless, random, math, sets, threading, PIL, Image
	
class nerve():	#This class is designed to hold information on a nerve cell and run its inernal logic	
	def __init__(self, nT, index, channels, exportChan, exportChar): # 

		if nT == "n":   self.nType = "N" # nerve type default: N
		elif nT == "i": self.nType = "I"
		elif nT == "I": self.nType = "I"
		elif nT == "o": self.nType = "O"
		elif nT == "O": self.nType = "O"
		else: 			self.nType = "N"

		
		self.defaultTreshold =  1 # only thing to edit really 
		
		self.index     = index
		self.pool      = len(channels) - 1
		self.nType     = nT
		self.threshold = float(self.defaultTreshold)  # default 1
		self.charge    = float(0)  # default 0
		self.outputs   = [] # empty list
		self.age       = 1
		self.randhash  = []
		for rIh in range(self.pool+1):
			self.randhash.append(rIh)
			#self.outputs.append(rIh)
		
		
		self.maxOutputsize = 200
		
		self.exportChan = exportChan
		self.exportChar = exportChar
		
		self.chan = channels
		self.mySyn = channels[index]
		
		self.outputAdd()

		
	def run(self): # logic area run check loop and wait for incoming charges.
		
		#inturpt = False
		#while inturpt != True:
			
		signal = self.mySyn.receive()
			#print signal
			#print self.charge, self.threshold, self.thresholdUpdate()
			#self.age += 1
		while signal:
			#print "index: %i age: %i" % (self.index, self.age)
			#self.age += 1
			if signal == "s": 
				print "waiting for charge signal...";

			else:
				#print self.ntasklet.alive
				#print signal
				self.addCharge(signal)
				if self.charge >= self.threshold:
					self.age += 1	
					print str(self.index) + " Exceeded Treshold " + str(self.charge) + " " + self.nType
					out = self.outputCharge()
					
					self.outputSignal()
					
					if self.nType == "o": self.exportSignal(out); 
						
					self.thresholdUpdate()
					self.resetCharge()
					self.outputAdd()
						
			stackless.schedule()
		
	def outputCharge(self):
		output = self.charge / len(self.outputs)
		return output
		
	def outputSignal(self):
		for i in self.outputs:
			#print i, charge
			self.chan[i].send(self.outputCharge())	
		
	def outputAdd(self):  # create a new function later that generates new outputs based on the amount of other outputs
		intr = False
		
		if len(self.randhash) == 0: random.randint(0, self.pool)
		#if len(self.randhash) >= self.maxOutputsize: self.randhash.pop(random.randint(0, self.pool))
		
		while intr != True: 
			# The age of a connection between two nerves is represented by the number of times an index appears in the output list, thus the stronger the connection.
			# a random number should be selected every time the nerve is fired.
			# this random number should be selected based on the past rule. 
			# So the more of an index in the outputs, the higher the probablility of being selected.
			rand =  random.choice(self.randhash) #random.choice(self.randhash) random.sample(self.randhash, randomrandint(self.pool, self.pool))   #random.randint(0, self.pool)
			if rand != self.index: intr = True

		self.randhash.append(rand)
		self.outputs.append(rand)
		
	def outputSize(self):
		return len(sorted(set(self.outputs)))

	def addCharge(self, inputs): # add X charge to the current charge
		fin = float(inputs)
		self.charge += fin
		#print self.index, self.charge
		
	def resetCharge(self):
		self.charge = 0
		
	def thresholdUpdate(self): # change the Threshold level
		# (charge*age^chargeout)+(chargeout^2/threshold)*chargeout
		newT = (self.charge * self.age ** self.outputCharge()) + (self.outputCharge() ** 2 / self.threshold) * self.outputCharge()  #(self.age * self.threshold) + (self.outputSize() * self.threshold) + self.outputCharge()  # lets try a linear type of equation
		self.threshold = newT
	
	def resetTreshold(self):
		self.threshold = self.defaultTreshold
		
	def exportSignal(self, sig):
		#print self.export
		print "EXPORTING"
		self.exportChan.send([self.index, sig])
		#pass
		
	def nerveType(self):
		return self.nType

	def wakeUp(self):
		stackless.tasklet(self.mySyn.send)('s')
	
 
	
# a nerve sees all the channels and selects the ones it ones to communicate with. so we have to create all the channels first for our NN
# Then make all the nerves so we need two more systems, a synapse for communication, and a main system that controls the nerve and synapse classes
class synapse():
	def __init__(self, size):
		print "init"
		self.channels = []
		for i in range(size):
			self.channels.append(stackless.channel())
			
	def add(self, i):
		self.channels.append(i)
	
	def remove(self, i):
		self.channels.pop(i) # remove by index 
		
	def chans(self):
		return self.channels
	
	
# the input layer is used to pass patterns and charges into the neural net
# a pattern and the number of times to input it into the system
# inputs will be a list of lists eg: [[5, 104.19204], [4, 19], [6, 0.219]] <=- [[index, charge]
# all this class is supposed to do is inject 1 pulse of charge to any number of indexes
class inputCharge():
	def __init__(self, nDict, channels, inputMatrix):
		self.nDict  = nDict
		self.chans  = channels
		self.inMat  = inputMatrix

	def inject(self):
		for i in self.inMat:
			if self.nDict[i[0]].nerveType() == "i":
				self.chans[i[0]].send(i[1])
		
#before we can get an export charge we have to wait for each of the asked indexed nerves to fire.
class exportCharge():
	def __init__(self, chan):
		#self.nDict = nDict
		self.chan = chan
		#self.opNerves = outputNerves
		self.inputMatrix = []
		
	def run(self):
		#for i in self.opNerves:
		signal = self.chan.receive()
		while signal:
			print "signal receieved"
			self.inputMatrix.append(signal)
		#pass
		#print self.inputMatrix
		#print "Wtf"
		
	def matrix(self):
		print self.inputMatrix

class i2d():
	def __init__(self, iLocation):
		self.imgDmatrix = [] # this will be a container list that holds a dec value version for the NN, starts from 0,0 and move to 0,x and then move through y,x 
		
		self.im = Image.open(iLocation)

		self.size = self.im.size
		self.height = self.size[1]
		self.width = self.size[0]
		
		self.pixels = self.im.load()
		
		for h in xrange(self.height):
			for w in xrange(self.width):
				Cred   = self.pixels[w, h][0]
				Cblue  = self.pixels[w, h][1]
				Cgreen = self.pixels[w, h][2]
				
				newD = self.rgbtoDec(Cred, Cgreen, Cblue)
				
				self.imgDmatrix.append(newD)
				
	def __call__(self):
		return self.imgDmatrix
	
	def rgbtoDec(self, red, green, blue): # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
		maindec = (red*256.0**2 + green*256.0 + blue)
		dMax = (256.0*256.0**2 + 256*256.0 + 256.0)
		
		return maindec / dMax
		
		
	def sizeDmatrix(self):
		return len(self.imgDmatrix)
		
	def size(self):
		return self.imgDmatrix
		
	def readIn(self, i):
		return self.imgDmatrix[i]

class main():
	# for the main class, create the synapse, create the nerves (input/ouput/nerves).
	def __init__(self, inP, outP, nerves):
		self.inputNerves  = inP       # input nerves poolsize.
		self.outputNerves = outP      # output nerves poolsize.
		self.nerves       = nerves    # intial number of nerves.
		self.poolSize     = inP+outP+nerves
		
		self.nDict   = []
		self.tDict   = []
		self.i = 0
		
		self.run()
		
	def run(self):
		syn = synapse(self.poolSize)
		synChan = syn.chans()
		exportChan = stackless.channel() 
		exportChar = exportCharge(exportChan)

		
		for i in range(self.nerves):
			self.nDict.append(nerve("i", self.i, synChan, exportChan, exportChar))
			#self.nDict[str(self.i)] = nerve("n", self.i, synChan)
			self.i += 1

		for o in range(self.inputNerves):
			self.nDict.append(nerve("o", self.i, synChan, exportChan, exportChar))
			#self.nDict[str(self.i)] = nerve("i", self.i, synChan)
			self.i += 1
			
		for n in range(self.outputNerves):
			self.nDict.append(nerve("n", self.i, synChan, exportChan, exportChar))
			#self.nDict[str(self.i)] = nerve("o", self.i, synChan)
			self.i += 1
	
	
		#exportThread = threading.Thread(target=stackless.tasklet(exportChar.run)())
		#exportThread.start()
		
		Kimg = i2d("k.png")	
		sendMatrix = []
		for kI in range(Kimg.sizeDmatrix()):
			sendMatrix.append([kI, Kimg.readIn(kI)])
		
		for iN in range(self.poolSize):
			self.tDict.append(stackless.tasklet(self.nDict[iN].run)())
		

		
		#print sendMatrix
		#print self.nDict
		#stackless.tasklet(synChan[0].send)(0.01)
		
		#print self.tDict[0].blocked
		
		test = inputCharge(self.nDict, synChan, sendMatrix)
		test.inject()

		stackless.run(timeout=0, threadblock=False)
		

		print exportChar.matrix()
	
	def nerveDictionary(self):
		return self.nDict
		
mainT  = main(64, 50, 64)
#print mainT.nerveDictionary()


