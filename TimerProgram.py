from tkinter import *
import time
from os import path
import os
class StopWatch(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self.shot_times = [0]
        self.shots_made = 1
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        #self.lapstr = StringVar()
        self.e = 0
        self.m = 0
        self.makeWidgets()
        self.laps = []
        self.lapmod2 = 0
        self.today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())
        
    def makeWidgets(self):                         
        """ Make the time label. """
        l1 = Label(self, text='----File Name----')
        l1.pack(fill=BOTH, expand=YES, pady=1, padx=2)

        self.e = Entry(self)
        self.e.pack(pady=2, padx=2)
        
        l = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=3, padx=2)

        l2 = Label(self,text='----Laps----')
        l2.pack(fill=BOTH, expand=YES, pady=10, padx=10)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        self.m = Listbox(self,selectmode=EXTENDED, height = 5,
                         yscrollcommand=scrollbar.set)
        self.m.pack(side=LEFT, fill=BOTH, expand=1, pady=5, padx=2)
        scrollbar.config(command=self.m.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
   
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)            
        return '%02d:%02d:%02d' % (minutes, seconds, hseconds)
        
    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def Reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0
        self.laps = []   
        self._setTime(self._elapsedtime)

    def Lap(self):
        '''Makes a lap, only if started'''
        tempo = self._elapsedtime - self.lapmod2
        if self._running:
            self.shots_made +=1
            print(self.shots_made)
            self.shot_times.append(self._elapsedtime)
            self.laps.append(self._setLapTime(tempo))
            self.m.insert(END, self.laps[-1])
            self.m.yview_moveto(1)
            self.lapmod2 = self._elapsedtime
       
    def GravaCSV(self):
        path = os.path.abspath(r"C:\Users\tkgam\Downloads\timer\shots.csv")
        with open(path, 'w') as csvfile:
            print("making file")
            for time in self.shot_times:
                csvfile.write(str(time) + '\n')
        print("file made")
            
def main():
    root = Tk()
    root.wm_attributes("-topmost", 1)      #always on top - might do a button for it
    root.geometry("1000x1000")
    sw = StopWatch(root)
    sw.pack(side=TOP)

    Button(root, text='Lap', height=200, width= 150,command=sw.Lap).pack(side=LEFT)
    Button(root, text='Start', command=sw.Start).pack(side=LEFT)
    Button(root, text='Stop', command=sw.Stop).pack(side=LEFT)
    #Button(root, text='Reset', command=sw.Reset).pack(side=LEFT)
    Button(root, text='Save', command=sw.GravaCSV).pack(side=LEFT)
    Button(root, text='Quit', command=root.quit).pack(side=LEFT)    
    
    root.mainloop()

if __name__ == '__main__':
    main()
