import pathlib
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
import logging

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QGridLayout

from . import utils

class MplCanvas(FigureCanvasQTAgg):
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class bosCrimeMapUI(QMainWindow):

    def __init__(self, df, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Boston Crime Report Map')
        self.setGeometry(100, 100, 950, 700)
        self.df = df
    
        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # initialize all components
        self._createCanvas()
        self._createFilterPanel()
        self._createMenu()
        self._createStatusBar()


    def _createCanvas(self):
        # variable
        width = 10
        height = 6
        dpi = 100

        canvasLayout = QVBoxLayout()
        self.canvas = MplCanvas(self, width=width, height=height, dpi=dpi)
        # set map background
        self.background = plt.imread(utils.get_map_png())
        self.canvas.axes.imshow(self.background, extent=utils.get_map_spec())
        # expand plot to whole figure
        self.canvas.axes.set_position([0,0,1,1])
        # remove axis label
        self.canvas.axes.get_yaxis().set_visible(False)
        self.canvas.axes.get_xaxis().set_visible(False)
        # create navigation tool bar and layout
        navToolbar = NavigationToolbar(self.canvas, self)
        canvasLayout.addWidget(navToolbar)
        canvasLayout.addWidget(self.canvas)
        self.generalLayout.addLayout(canvasLayout)

    
    def update_location(self, lat, lon, color, size=None):
        logging.debug('update plot')
        if size is None:
            num = lat.shape[0]
            size = 1/(num/300)
        self.canvas.axes.scatter(lon, lat, s=size, c=color)
        self.canvas.draw()
    

    def clear_location(self):
        logging.debug('clear plot')
        self.canvas.axes.cla()
        self.canvas.axes.imshow(self.background, extent=utils.get_map_spec())
        self.canvas.draw()


    def _createFilterPanel(self):
        # TODO
        # Work in progress
        filterPanelLayout = QGridLayout()
        # Filter options add more here
        # 'option': (position), widgets
        #==================================
        # Add more options here 
        #==================================
        yearOptions = list(self.df['YEAR'].unique().astype('str'))
        filters = {
            'year_label1': 
                {'pos':(0,0), 'widget':QLabel, 'text':'From'},
            'year_label2': 
                {'pos':(0,2), 'widget':QLabel, 'text':'to'},
            'year1':
                {'pos':(0,1), 'widget':QComboBox, 'options': yearOptions},
            'year2':
                {'pos':(0,3), 'widget':QComboBox, 'options': yearOptions},
            'update':
                {'pos':(1,0,1,4), 'widget':QPushButton},
        }
        self.filters = {}

        # build filter
        for filterName, param in filters.items():
            if param['widget'] is QLabel:
                label = param['widget'](param['text'])
                filterPanelLayout.addWidget(label, *param['pos'])
                continue
            if param['widget'] is QPushButton:
                self.filters[filterName] = param['widget'](filterName)
            elif param['widget'] is QComboBox:
                self.filters[filterName] = param['widget']()
                self.filters[filterName].addItems(param['options'])
            filterPanelLayout.addWidget(self.filters[filterName],
                *param['pos'])
        self.generalLayout.addLayout(filterPanelLayout)

        
    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)


    def _createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("...")
        self.setStatusBar(self.status)

    
    def update_stats(self, msg):
        self.status.clearMessage()
        self.status.showMessage(msg)
