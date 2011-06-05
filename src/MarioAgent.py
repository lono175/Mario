# 
# Copyright (C) 2007, Mark Lee
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import random
import sys
from rlglue.agent.Agent import Agent
from rlglue.types import Action
from rlglue.types import Observation
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.utils.TaskSpecVRLGLUE3 import TaskSpecParser


from random import choice
import string
class MonType:
	Mario = 0
	RedKoopa = 1
	GreenKoopa = 2
	Goomba = 3
	Spikey = 4
	PiranhaPlant = 5
	Mushroom = 6
	FireFlower = 7
	Fireball = 8
	Shall = 9
	BigMario = 10
	FieryMario = 11
class Monster:
	def __init__(self):
		pass

def GenPasswd():
	chars = string.letters + string.digits
	for i in range(8):
		newpasswd = newpasswd + choice(chars)
	return newpasswd

def GenPasswd2(length=8, chars=string.letters + string.digits):
	return [choice(chars) for i in range(length)]


class RandomAgent(Agent):

	def agent_init(self,taskSpecString):
		print taskSpecString
		#TaskSpec = TaskSpecParser(taskSpecString);
		#if TaskSpec.valid:
			#print "Task spec was valid";
		#else:
			#print "Task Spec could not be parsed: "+taskSpecString;
			#exit()

		##parse action
		self.action = Action()
		#self.int_action_ranges    = TaskSpec.getIntActions()
		#self.double_action_ranges = TaskSpec.getDoubleActions()
		#self.action.numInts       = len(self.int_action_ranges)
		#self.action.numDoubles    = len(self.double_action_ranges)
		#self.action.numChars      = TaskSpec.getCharCountActions()

		#print "int",self.int_action_ranges,self.action.numInts 
		#print "doubles",self.double_action_ranges,self.action.numDoubles
		#print "chars",self.action.numChars 


		random.seed(0)

	def dummyAction(self):
		action = Action()
		action.numInts = 3
		action.numDoubles = 0
		action.numChars = 0
		action.intArry = []
		action.doubleArray = []
		action.charArray = []
		action.intArray.append(1)
		action.intArray.append(1)
		action.intArray.append(1)
		return action

	def getMario(self, obs):
		monList = self.getMonsters(obs)
		for m in monList:
			if m.type == MonType.Mario or m.type == MonType.BigMario or m.type == MonType.FieryMario:
				print "type: ", m.type
				return m
		assert(False)
					
	def getMonsters(self, obs):
		monList = []
		print obs.intArray
		print obs.doubleArray
		for i, type in enumerate(obs.intArray):
			m = Monster()
			if i == 0:
				continue
			if i % 2 == 0:
				m.winged = False
				if type != 0:
					m.winged = True	
			else:
				m.type = type
			if i % 2 == 0:
				continue
			id = i/2

			print "index ", i
			print "len ", len(obs.doubleArray)
			m.x = obs.doubleArray[4*id];
			m.y = obs.doubleArray[4*id+1];
			m.sx = obs.doubleArray[4*id+2];
			m.sy = obs.doubleArray[4*id+3];
			monList.append(m)
				

		return monList

	def agent_start(self,observation):
		return self.dummyAction()

	def agent_step(self,reward, observation):
		#print observation.intArray
		#print reward
		mario = self.getMario(observation)
		print "loc:", mario.x , " ", mario.y, " ", mario.sx, " ", mario.sy
		return self.dummyAction()

	def agent_end(self,reward):
		pass
	def agent_cleanup(self):
		pass

	def agent_freeze(self):
		pass

	def agent_message(self,inMessage):
		return None

	def randomify(self):
		self.action.intArray = []
		self.action.doubleArray = []


		for min_action,max_action in self.int_action_ranges:					
			act = random.randrange(min_action,max_action+1)
			self.action.intArray.append(act)

		for min_action,max_action in self.double_action_ranges:					
			act = random.uniform(min_action,max_action)
			self.action.doubleArray.append(act)

		self.action.charArray   = GenPasswd2(self.action.numChars)
		#print self.action.intArray
		#print self.action.doubleArray
		#print self.action.charArray





if __name__=="__main__":        
	AgentLoader.loadAgent(RandomAgent())
