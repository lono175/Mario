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

#TODO: add location to tile feature
#TODO: add speed to feature
import sys
from rlglue.types import Observation
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.utils.TaskSpecVRLGLUE3 import TaskSpecParser
from LambdaSARSA import LambdaSARSA
from FeatureMario import *
from ML import *
import tool


from random import choice
import string
episilon = 0.005

MaxY = 15
def saveObj(obj):
    print "descructing...."
    #actionList = getAllAction()
    #initialQ = 0
    #dumpCount = 100000
    #self.agent = LinearSARSA(0.05, 0.05, 0.95, actionList, initialQ, dumpCount)
    #obj.agent = LambdaSARSA(0.10, 0.05, 0.90, actionList, initialQ, dumpCount)
    tool.Save(obj, "mario.db")

def GenPasswd():
    chars = string.letters + string.digits
    for i in range(8):
        newpasswd = newpasswd + choice(chars)
    return newpasswd

def GenPasswd2(length=8, chars=string.letters + string.digits):
    return [choice(chars) for i in range(length)]

	





from ModelAgent import ModelAgent
if __name__=="__main__":        
    import atexit
    agent = tool.Load("mario.db")
    #agent = LinearSarsaAgent()
    #agent = ModelAgent()
    atexit.register(lambda: saveObj(agent)) #workaround to the NoneType error in hte descructorn
    #agent = tool.Load("Speed.db")
    #AgentLoader.loadAgent(agent)
    
    AgentLoader.loadAgent(agent)
