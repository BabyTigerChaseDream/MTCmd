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

def wgetMtFunc(wgetArgs):
    serverDir, localDir, Qbar = wgetArgs
    DResu = {'resu':'pass'}

    # wget cmdline template:
    #cmdwget = "wget -q -nc -r -nH -np --cut-dirs=10 -R \"index.html*\" {serverDir} -P {localDir}".format_map(vars())
    # delete "-q" , because it will hide error to be collect to stderr in "proc.communicate()"
    cmdwget = "wget -nc -r -nH -np --cut-dirs=10 -R \"index.html*\" {serverDir} -P {localDir}".format_map(vars())

    print('=====> Start download : ', cmdwget)
    proc=sub.Popen(cmdwget.format_map(vars()), bufsize=1, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    stdout,stderr = proc.communicate()

# parse stdout/stderr
    strout=stdout.decode("utf-8")
    strerr=stderr.decode("utf-8")
    #queue , 
    Qbar.put(serverDir)

    ## TODO - check wget exception 
    #if strerr.find('ERROR') or strerr.find('failed'):
    #    DResu['resu'] = 'failed :'
    #    #DResu['resu'] = 'failed :' + strerr
    
    return (DResu.values())

##############################
###### main-process func ###### 
##############################
if __name__=="__main__":
    ### cmdline arguments 
    import argparse
    parser = argparse.ArgumentParser(description='multi-process wget download ')

    # note: -f/-loc should both be absolute path " 
    parser.add_argument('-f', action='store', dest='fdnld', default=None, help='init file includes all download links')    
    parser.add_argument('-loc', action='store', dest='locdir', default=None, help='local dir to put file')    

    arglist=parser.parse_args()
    print(parser.parse_args())
   
    fdnld = arglist.fdnld
    locdir = arglist.locdir

    wgetList = []
    with open(fdnld,'r') as fd:
        print('>>>>> Reading fdnld init file: ',fdnld)
        for links in fd:
            wgetList.append(links.strip('\n'))
        
    ##### multi-process param #####
    m = Manager()
    p = Pool(cpu_count()) 
    q = m.Queue()

    arglists = [ (link,locdir,q) for link in wgetList]

    ### block mode 
    #result = p.map(wgetMtFunc,lists)
    
    # none block mode 
    result = p.map_async(wgetMtFunc,arglists)
    	
    ### collect ALL process result in a Queue ? and summarize  
    # monitor loop
    while True:
        if result.ready():
            break
        else:
            size = q.qsize()
            print(size)
            time.sleep(0.5)
    
    outputs = result.get()
    
    for o in outputs:
        print(o)

    os.system('ls -al '+locdir)
