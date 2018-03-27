from PyQt5.QtWidgets import (
#from PyQt4.QtGui import (
    QApplication
    )
import sys
import threading

#my class
import xrb_datareader
import xrb_sliders
import xrb_scope_matplot

def main():
    app = QApplication(sys.argv)

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
