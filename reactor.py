import event
import time

class Reactor(event.EventEmitter):

    def __init__(self):
        pass

    def run(self):
        """ Event reactor loop """
        while hasattr(self,'listeners') and self.listeners.has_key('tick') and self.listeners['tick']:
            # Tick event
            self.emit('tick', time.time())


reactor = Reactor()     # Reactor as a global object


if __name__ == "__main__":

    # Register a simple function for each tick
    def handleTick(emitter, event_type, event_data):
        print "%s %s" % (event_type, event_data)
        # Block for a while
        import time
        time.sleep(1) 

    # Interval, based on closure with problem (scope old_time)
    def setInterval(interval, doInterval):
        reactor.old_time = time.time()
        def handleTick(e, t, d):
            new_time = time.time()
            if new_time-reactor.old_time > interval:
                # NO puedo actualizar old_time en el scope superior!!!!
                # Fast hack --> put old_time in reactor
                reactor.old_time = new_time
                doInterval()
                 
        reactor.on('tick', handleTick)

    # Interval, based on object
    class Interval(event.EventEmitter):
        INTERVAL = 'interval'
        def __init__(self, seconds, callback):
            self.seconds = seconds
            self.old_time = 0
            self.on(self.INTERVAL, callback)
        
        def set(self):
            reactor.on('tick', self._handleTick)
            return self

        def unset(self):
            reactor.removeListener('tick', self._handleTick)
            print reactor.listeners

        def _handleTick(self, e, t, d):
            new_time = time.time()
            if new_time - self.old_time > self.seconds:
                self.old_time = new_time
                self.emit(self.INTERVAL, self.seconds)

        # Convenience class method
        @staticmethod
        def setInterval(seconds, callback):
            return Interval(seconds, callback).set()
     
            
              

    # Connect everyting
    #reactor.on('tick', handleTick) 
    def doit(e,t,d):
        print "timer..."
    #setInterval(2,doit)
    i = Interval.setInterval(1.5,doit)
    print i 
    i.unset()
    print i.listeners
    i.set()
    i.removeListener(i.INTERVAL ,doit)
    print i.listeners
    print reactor.listeners
    i.unset()

    # Main Loop
    reactor.run()