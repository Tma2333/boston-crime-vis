import sys
from PyQt5 import QtCore, QtWidgets
import bos_crime_vis_tool as vis_tool

def main():
    app = QtWidgets.QApplication(['Boston Crime Report Map'])
    window = vis_tool.gui.MainWindow()
    window.show()
    sys.exit(app.exec_())
    

if __name__ == '__main__':
    main()