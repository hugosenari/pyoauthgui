n = 1  
if __name__ == '__main__':
    import threading
    import datetime
    import time
    class ThreadClass(threading.Thread):
        def run(self):
            now = datetime.datetime.now()

            print "%s says Hello World at time: %s\nn: %s\n" % \
                (self.getName(), now, n)
                

    for i in range(2):
        t = ThreadClass()
        t.name = "name:%s:i:%s" % (t.name,i)
        t.start()