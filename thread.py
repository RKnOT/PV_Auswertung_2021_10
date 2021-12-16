
import threading

numThreads = 0
threadStarted = False
lock = threading.Lock()

def heron(a, b):
    with lock:
        global numThreads, threadStarted 
        numThreads += 1
        threadStarted = True
        # Heron Code wie vorher
    with lock:
        numThreads -= 1
        
    return(new)
    
    
    
threading.thread(heron,(99,))
threading.thread(heron,(999,))
threading.thread(heron,(1733,))
threading.thread(heron,(17334,))

while (not threadStarted) or (numThreads > 0):
        pass