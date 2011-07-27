#!/bin/bash
#basePath=../../..
#systemPath=$basePath/system
#Source a script that sets all important functions and variables
#source $systemPath/rl-competition-includes.sh


#Utility functions from rl-competition-includes.sh
#startRLGlueInBackGround
#startEnvShellInBackGround

PYTHONPATH=../../../system/codecs/Python/src/:../../../system/includes:. python ./consoleTrainer.py 
#./RL_experiment

#Utility functions from rl-competition-includes.sh
#waitForEnvShellToDie
#waitForRLGlueToDie
