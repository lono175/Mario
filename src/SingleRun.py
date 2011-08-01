
from rlglue.types import Observation
from rlglue.agent import AgentLoader as AgentLoader
from rlglue.agent.Agent import Agent
from rlglue.utils.TaskSpecVRLGLUE3 import TaskSpecParser
from LambdaSARSA import LambdaSARSA
import tool
import pickle
from ModelAgent import ModelAgent
if __name__=="__main__":        
    import atexit
    agent = tool.Load('mario_sarsa_981_0.04_0.db')
    #agent = LinearSarsaAgent()
    #atexit.register(lambda: saveObj(agent)) #workaround to the NoneType error in hte descructorn
    #agent = tool.Load("Speed.db")
    #AgentLoader.loadAgent(agent)

    #while True:
    
    AgentLoader.loadAgent(agent)
    #time.sleep(2)
