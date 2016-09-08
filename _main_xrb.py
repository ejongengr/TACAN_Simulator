from PyQt4 import QtGui
import sys
import threading

#my class
import exmod
import xrb_datareader
import xrb_sliders
import xrb_scope_matplot

def main():
    app = QtGui.QApplication(sys.argv)

    # Data Reader
    dr = xrb_datareader.DataReader()

    window = xrb_sliders.Window(dr)
    window.show()
    
    # Oscilloscope doesn't return
    oc = xrb_scope_matplot.Oscilloscope(dr)
    oc.start_animation()

    sys.exit(app.exec_())
    
# call main
if __name__ == '__main__':

    main()
