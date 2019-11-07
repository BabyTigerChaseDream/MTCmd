#!/usr/bin/python3

import _thread as thread
import os

cmd = "vulcan --dry-run -v --eris --db --user jiag --product=//sw/gpgpu/MachineLearning/cudnn_v7.1/eris/cudnn_r80_r375.vlcp --target-gpu gv100sxm2 --target-arch x86_64 --target-os Ubuntu16_04 --testsuite cudnn_layer_tests --target-revision=cl-tot --tags "

def child(tag):
    print('Running : *** ', tag)
    cmdline = cmd + tag
    print('cmdline is : *** ', cmdline)
    os.system(cmdline)
    mutex.acquire()
    mutex.release()

def parent():
    taglist = ['1111111','2222222','3333333','4444444']
    while True:
        for t in taglist:
            print('tag is : *** ', t)
            thread.start_new_thread(child, (t,))
        if input() == 'q': break    

if __name__ == '__main__':
    mutex = thread.allocate_lock() 
    parent()
