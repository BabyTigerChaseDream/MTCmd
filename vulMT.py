#!/usr/bin/python3

### Step-1 : multiprocess func run model
from multiprocessing import *
import subprocess as sub

import re
import time 

#############################
#   child-process func      #
#############################

def vulmtFunc(vulargs):
    # cl: change-list / tags: notes of submit / Qbar: Queue log progress
    cl, cmdtemp, tags, Qbar = vulargs
    DResu = {'tags':tags,'resu':'pass','uuidLink':None}

    print('=====> Start running cl-{cl}'.format_map(vars()))
    print('cmdline: ',cmdtemp.format_map(vars()))
    proc=sub.Popen(cmdtemp.format_map(vars()), bufsize=1, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    stdout,stderr = proc.communicate()

# parse stdout/stderr
    strout=stdout.decode("utf-8")
    strerr=stderr.decode("utf-8")
    #queue , 
    Qbar.put(tags)

    # Filter error 
    # b'[ERROR cuda.py:_get_eris_arch_targets:1851] unknown target architecture "ppc"\n    
    if 'ERROR' in strerr:
        DResu['resu'] = 'failed :' + strerr
        # if failed , no uuidLink at all... use "None" in default DResu
    else:
    #  TODO: can be an attri of vulcmd class 
        start='ACCEPTED... Go to '
        end=' to check its status.'
    
        DResu['uuidLink']=re.search('%s(.*)%s' % (start, end), strout).group(1)

    return (DResu.values())

##############################
###### main-process func ###### 
##############################
if __name__=="__main__":
    ### cmdline arguments 
    import argparse
    parser = argparse.ArgumentParser(description='MT-process run vul cmdline ')

    # show command group 
    parser.add_argument('-cl', action='store', dest='CLList', default=None, help='CL numbers to run, inform of 1,2,3 ')    
    # note: -cmd must quote by " 
    parser.add_argument('-cmd', action='store', dest='cmdline', default=None, help='full vul cmdline')    
    parser.add_argument('-t', action='store', dest='tags', default=None, help='tags in cmdline')    

    arglist=parser.parse_args()
    print(parser.parse_args())

    ### vulmtFunc paramter
    #CLList = ['24068678','24068670','24068575','24068452','24068331','24068142','24068074','24068074','tot']
    #CLList = ['hello','multi']
    #cmdline="vulcan --keep-going -v --eris --user *** --product=//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r92_r396.vlcp --build cudnn_doc --target-os=Linux --target-arch=aarch64 --tag={tags} --target-revision=cl-{cl}"
    #tags = 'MT'
   
    CLList = arglist.CLList.split(',')
    # use " as a special char , incase of mix other cmdline param with it
    cmdline = re.sub('\"','',arglist.cmdline)
    tags = arglist.tags

    ##### multi-process param #####
    m = Manager()
    p = Pool(cpu_count()) 
    q = m.Queue()

    arglists = [ (cl,cmdline,tags,q) for cl in CLList ]

    ### block mode 
    #result = p.map(vulmtFunc,lists)
    
    # none block mode 
    result = p.map_async(vulmtFunc,arglists)
    	
    ### collect ALL process result in a Queue ? and summarize  
    # monitor loop
    while True:
        if result.ready():
            break
        else:
            size = q.qsize()
            print(size)
            time.sleep(3)
    
    outputs = result.get()
    
    for o in outputs:
        print(o)
