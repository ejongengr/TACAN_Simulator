# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 11:24:10 2016

@author: Jason Lee
"""

import numpy as np
import math
import matplotlib.pyplot as plt 
from matplotlib.widgets import MultiCursor
import matplotlib.animation as animation
import sys
import threading
       
INTERVAL = 250 # How open update windows, in miliseconds

class Oscilloscope():

    def  __init__(self, dr):
        self.dr = dr

        self.fig = plt.figure()
        
        self.maxLen = self.dr.maxLen
        self.xdata = np.arange(0, self.maxLen, float(360)/self.maxLen)
        
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.set_xlim(0, self.maxLen)
        self.ax1.set_ylim(-1.5, 1.5)
        self.line_15, = self.ax1.plot([], [], label="15Hz", marker='.')         
        self.line_135, = self.ax1.plot([], [], label="135Hz", marker='.')         
        self.line_nrb, = self.ax1.plot([], [], label="NRB", marker='.')         
        self.line_arb, = self.ax1.plot([], [], label="ARB", marker='.')         
        self.ax1.set_title("xRB Simulation")
        #self.ax1.legend()
        self.ax1.grid(True)
                
        #multi = MultiCursor(self.fig.canvas, (self.ax1, self.ax2), color='r', lw=1)
        
        #close event
        self.fig.canvas.mpl_connect('close_event', self.handle_close)

        #plt.subplots_adjust(hspace=0.5)
        
    def init(self):
        pass

    def handle_close(self, event):
        print('Closed Figure!')
        sys.exit()
        
    def start_animation(self):
        # CAUSTION:inf no ani below, graph hold
        ani = animation.FuncAnimation(self.fig, self.update, 
                                init_func=self.init,
                                interval=INTERVAL
                                )        
        # show plot
        plt.show()

    def update(self, frameNum):
        self.line_15.set_data(self.xdata, self.dr.w15_buf)
        self.line_135.set_data(self.xdata, self.dr.w135_buf)
        self.line_nrb.set_data(self.xdata, self.dr.nrb_buf)
        self.line_arb.set_data(self.xdata, self.dr.arb_buf)

# call main
if __name__ == '__main__':
    
    class DataReader(threading.Thread):        

        def __init__(self):
            threading.Thread.__init__(self)
            self.maxLen = 100
            self.a0_buffer = []
            self.a = 10  # amplitudude of sine graph will change for animation
            
        def run(self):
            while True:            
                if self.a > 100:
                    self.a = 10
                self.a += 1    
                self.a0_buffer = [self.a*math.sin(2*math.pi*10*t/100.0) for t in range(100)]
            #    print self.a0_buffer[2]            
        
    drmutex = threading.Lock()
    dr = DataReader()
    dr.start()

    osc = Oscilloscope(dr, drmutex)
    osc.start_animation()
    
    sys.exit()
    print('exiting.')
