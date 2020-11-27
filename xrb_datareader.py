# -*- coding: utf-8 -*-
"""

		  
@author: Jason Lee
"""

import csv
import math
import numpy as np
import os.path
import threading

NRB_HEIGHT = 1.4
ARB_HEIGHT = 1.2

# plot class
class DataReader():
    
    maxLen = 360
    
    #GUI
    hold = False
    filename = 'xrb.csv'                
    
    def __init__(self):

#        threading.Thread.__init__(self)           
               
        # data buffer to draw
        self.w15_buf = np.zeros(self.maxLen)
        self.w135_buf = np.zeros(self.maxLen)
        self.nrb_buf = np.zeros(self.maxLen)
        self.arb_buf = np.zeros(self.maxLen)
        self.time = np.arange(0, self.maxLen)
        self.update("15Hz", 0)
        self.update("135Hz", 0)
        self.update("NRB", 0)
        self.update("ARB", 0)
        
        # GUI
        self.w = None
        
        #offset
        self.nrb_offset = 0
        self.arb_offset = 0
        self.w15_offset = 0
        self.w135_offset = 0
        
        
        try:
            os.remove(self.filename)
        except OSError:
            pass

    def SetGUI(self, w):
        self.w = w
                
    #GUID interface    
    def gui_set_hold(self, value):
        self.hold = value

    def gui_save(self):
        holded = False
        if not self.hold:
            self.hold = True
            holded = True
        print("graph hold")
        
        if not os.path.isfile(self.filename):
            f = open(self.filename, 'ab') # without b extra carriage return saved
            wr = csv.writer(f, delimiter=',')
            wr.writerow(['fb', 'fb_old', 'attn', 'antenna', 'average'])
        else:
            f = open(self.filename, 'a')
            wr = csv.writer(f, delimiter=',')

        for i in range(self.maxLen):
            idx = self.maxLen-1-i
            wr.writerow([self.fb_buffer[idx],
                        self.fb_old_buffer[idx],
                        self.attn_buffer[idx],
                        self.antenna_buffer[idx],
                        self.ave_buffer[idx]])
        if holded == True:
            self.hold = False
        print("save done")
        
    # update data
    def update(self, name, offset): 
        if name == "15Hz":
            #15Hz
            self.w15_offset = offset
            for i, ti in enumerate(self.time):
                t = ti/float(self.maxLen)
                d = offset/float(self.maxLen)
                self.w15_buf[i] =  math.sin(2*math.pi*(t+d))   # 15Hz -> 1Hz                            

        if name == "135Hz":
            #135Hz
            self.w135_offset = offset
            for i, ti in enumerate(self.time):
                t = ti*9/float(self.maxLen)
                d = offset*9/float(self.maxLen)
                self.w135_buf[i] =  math.sin(2*math.pi*(t+d))
        
        if name == "NRB":
            self.nrb_offset = offset
            for i, ti in enumerate(self.time):
                if i == 0 + offset:
                    self.nrb = i
                    self.nrb_buf[i] =  NRB_HEIGHT
                else:    
                    self.nrb_buf[i] =  0
        
        if name == "ARB":
            self.arb_offset = offset

            for n in range(self.maxLen):
                self.arb_buf[n] = 0

            nn = list(range(0, self.nrb_offset - 20))
            for n in nn:
                if (n - offset) % 40 == 0:    # ARB
                    self.arb_buf[n] =  ARB_HEIGHT
                else:
                    tmp = 0

            start = self.nrb_offset + 20
            if start >= self.maxLen:
                start = self.maxLen
            nn = list(range(self.nrb_offset + 20, self.maxLen))
            for n in nn:
                if (n - offset) % 40 == 0:    # ARB
                    self.arb_buf[n] =  ARB_HEIGHT
                else:
                    tmp = 0

    def calBearing(self):
        # calculate 15Hz zero-crossing
        z15 = self.maxLen - self.w15_offset
        # 15Hz bearing
        b15 = z15 - self.nrb_offset
        if b15 < 0:
            b15 = self.maxLen - self.nrb
        # how many arb between nrb and 15hz zero-crossing
        count = 0
        #print "*"
        for i, m in enumerate(self.arb_buf):        
            if ((i > self.nrb_offset) and (i < z15)):
                if m == ARB_HEIGHT:
                    #print i
                    count += 1
                    last_arb = i
        # caculate 135Hz bearing        
        z135 = 40 - self.w135_offset
        b135 = (z135 - self.arb_offset%40)%40
        bearing_org = count * 40 + b135%40
        
        # Adjust bearing
        if (self.DegDiff(bearing_org, b15) > 20.0):
            bearing = bearing_org - 40
        elif (self.DegDiff(bearing_org, b15) < -20.0):  
            bearing = bearing_org + 40;
        else:
            bearing = bearing_org
            
        return (self.nrb, z15, b15, self.arb_offset%40, z135, b135, count, bearing_org, bearing)

    def DegDiff(deg1, deg2, modular=360):
        """
           deg1, deg2 : degree
           return: result = (deg1-deg2)
           modular = 360, -180 < result <= 180
           modular = 40,  -20 < result <= 20
        """

        if ((deg1 > 720.0) or (deg2 > 720.0)):
            return None
        m = 360 / modular
        if (m == 1):
            rot = 360.0;
        else:
            rot = 40.0;

        # -180 < deg 1 < 180
        while(deg1 > rot):
            deg1 -= rot
        if (deg1 > rot/2):
            deg1 -= rot
        if(deg1 < -rot/2):
            deg1 += rot

        # -180 < deg 2 < 180
        while(deg2 > rot):
            deg2 -= rot
        if (deg2 > rot/2):
            deg2 -= rot
        if(deg2 < -rot/2):
            deg2 += rot

        # -180 < diff < 180
        diff = deg1 - deg2
        if (diff > rot/2):
            diff -= rot
        if (diff < -rot/2):
            diff += rot
        return diff	

def main():
    pass
    
# call main
if __name__ == '__main__':
    main();
