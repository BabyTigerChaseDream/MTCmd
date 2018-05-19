#!/usr/bin/python3

### Step-1 : multiprocess func run model
from multiprocessing import *
import subprocess as sub

import time 

# child-process func 
def vulrun(tag):
    DResu = {'tag':tag,'resu':'pass','webID':None}

    cmdtemp="vulcan -v --eris --user jiag --dry-run --product=//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r90_r384.vlcp --build cudnn --target-revision=cl-tot --target-os=Ubuntu16_04 --target-arch=ppc64le --tags={tag}".format_map(vars())

    print('=====> Start running {tag}'.format_map(vars()))
    proc=sub.Popen(cmdtemp, bufsize=1, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    stdout,stderr = proc.communicate()

# parse stdout/stderr
    strout=stdout.decode("utf-8")
    strerr=stderr.decode("utf-8")
    #queue , 
    q.put(tag)

### func output/err collection
# search for ERROR
#### >>> stderr
# b'[ERROR cuda.py:_get_eris_arch_targets:1851] unknown target architecture "ppc"\n    

    if 'ERROR' in strerr:
        DResu['resu'] = 'failed'

    DResu['webID'] = strout[0]

    return (DResu.values())


##############################
###### main-process func ###### 
m = Manager()
q = m.Queue()
p = Pool(cpu_count()) 

taglists = ['Jia-11111','Jia-22222','Jia-33333','Jia-44444','Jia-55555','Jia-66666','Jia-77777','Jia-88888']

### block mode 
#result = p.map(vulrun,lists)

# none block mode 
#result = p.map_async(vulrun,taglists)
	
### collect ALL process result in a Queue ? and summarize  
# monitor loop
#while True:
#    if result.ready():
#        break
#    else:
#        size = q.qsize()
#        print(size)
#        time.sleep(3)
#
#outputs = result.get()
outputs = []
for t in taglists:
    outputs.append(vulrun(t))

for o in outputs:
    print(o)
## Try timeit for *.py (multiprocess/for loop)
