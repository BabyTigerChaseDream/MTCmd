#!/usr/bin/python3

### Step-1 : multiprocess func run model
import os

from multiprocessing import *
import subprocess as sub

import re
import time 

#############################
#   child-process func      #
#############################

def MtFunc(msg):
    print('In MtFunc :: \n')
    for i in range(0,60):
        time.sleep(1)
        print(i,'[[ ',msg)
 
##############################
###### main-process func ###### 
##############################
if __name__ == '__main__':        

    #MtFunc('hello')
    p = Pool(cpu_count()) 
    
    arglists =['a','b','c','d','e','f','g']
    ### block mode 
    result = p.map(MtFunc,arglists)
    # none block mode 
    #result = p.map_async(MtFunc,arglists)

