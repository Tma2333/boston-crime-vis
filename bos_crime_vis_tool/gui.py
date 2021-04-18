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
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtWidgets import QRadioButton
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
        self.setGeometry(100, 100, 1150, 700)
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
            try:
                size = 1/(num/300)
            except ZeroDivisionError:
                pass
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
        monthOptions = [str(i) for i in sorted(self.df['MONTH'].unique())]
        hourOptions = [str(i) for i in sorted(self.df['HOUR'].unique())]
        weekOptions = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        districtOptions = ['All', 'Downtown', 'Charlestown', 'East Boston', 'Roxbury',
                           'Mattapan', 'South Boston', 'Dorchester', 'South End',
                           'Brighton', 'West Roxbury', 'Jamaica Plain', 'Hyde Park']
        colorOptions = ['red', 'cyan', 'blue', 'green', 
                        'magenta', 'orange', 'indigo', 'lime']
        typeOptions = list(self.df['OFFENSE_CODE_GROUP'].unique().astype('str'))
        typeOptions.remove('HUMAN TRAFFICKING - INVOLUNTARY SERVITUDE')
        typeOptions.insert(0,'All')
        sizeOptions = [str(i) for i in range(1, 10)]
        sizeOptions.insert(0,'Auto')
        year_row = 1
        month_row = year_row + 2
        week_row = month_row + 2
        hour_row = week_row +2
        type_row = hour_row + 1
        district_row = type_row + 1
        color_row = district_row + 1
        size_row = color_row + 1
        clear_row = size_row + 1
        update_row = clear_row + 1
        filters = {
            # year
            'year_label': 
                {'pos':(year_row-1,0), 'widget':QLabel, 'text':'Year:'},            
            'year_label1': 
                {'pos':(year_row,0), 'widget':QLabel, 'text':'From'},
            'year_label2': 
                {'pos':(year_row,2), 'widget':QLabel, 'text':'to'},
            'year1':
                {'pos':(year_row,1), 'widget':QComboBox, 'options': yearOptions, 'default':'2015'},
            'year2':
                {'pos':(year_row,3), 'widget':QComboBox, 'options': yearOptions, 'default':'2018'},
            # month
            'month_label': 
                {'pos':(month_row-1,0), 'widget':QLabel, 'text':'Month:'},                  
            'month_label1': 
                {'pos':(month_row,0), 'widget':QLabel, 'text':'From'},
            'month_label2': 
                {'pos':(month_row,2), 'widget':QLabel, 'text':'to'},
            'month1':
                {'pos':(month_row,1), 'widget':QComboBox, 'options': monthOptions, 'default':'1'},
            'month2':
                {'pos':(month_row,3), 'widget':QComboBox, 'options': monthOptions, 'default':'12'},            
            # week
            'week_label': 
                {'pos':(week_row-1,0), 'widget':QLabel, 'text':'Week:'},                  
            'week_label1': 
                {'pos':(week_row,0), 'widget':QLabel, 'text':'From'},
            'week_label2': 
                {'pos':(week_row,2), 'widget':QLabel, 'text':'to'},
            'week1':
                {'pos':(week_row,1), 'widget':QComboBox, 'options': weekOptions, 'default':'Monday'},
            'week2':
                {'pos':(week_row,3), 'widget':QComboBox, 'options': weekOptions, 'default':'Sunday'},
            # hour
            'hour_label': 
                {'pos':(hour_row-1,0), 'widget':QLabel, 'text':'hour:'},                  
            'hour_label1': 
                {'pos':(hour_row,0), 'widget':QLabel, 'text':'From'},
            'hour_label2': 
                {'pos':(hour_row,2), 'widget':QLabel, 'text':'to'},
            'hour1':
                {'pos':(hour_row,1), 'widget':QComboBox, 'options': hourOptions, 'default':'0'},
            'hour2':
                {'pos':(hour_row,3), 'widget':QComboBox, 'options': hourOptions, 'default':'23'},
            # crime type   
            'type_label':
                {'pos':(type_row,0), 'widget':QLabel, 'text':'Type'},
            'type':
                {'pos':(type_row,1,1,3), 'widget':QComboBox, 'options': typeOptions},
            # district
            'district_label':
                {'pos':(district_row,0), 'widget':QLabel, 'text':'District'},
            'district':
                {'pos':(district_row,1,1,3), 'widget':QComboBox, 'options': districtOptions},
            # color
            'color':
                {'pos':(color_row,0,1,4), 'widget':QRadioButton,'options': colorOptions},
            # size   
            'size_label':
                {'pos':(size_row,0), 'widget':QLabel, 'text':'Size'},
            'size':
                {'pos':(size_row,1,1,3), 'widget':QComboBox, 'options': sizeOptions},
            # buttoms
            'clear':
                {'pos':(clear_row,0,1,4), 'widget':QPushButton},
            'update':
                {'pos':(update_row,0,1,4), 'widget':QPushButton},
        }
        self.filters = {}

        # build filter
        for filterName, param in filters.items():
            if param['widget'] is QLabel:
                label = param['widget'](param['text'])
                filterPanelLayout.addWidget(label, *param['pos'], 
                    alignment=QtCore.Qt.AlignBottom)
                continue
            if param['widget'] is QPushButton:
                self.filters[filterName] = param['widget'](filterName)
            elif param['widget'] is QComboBox:
                self.filters[filterName] = param['widget']()
                self.filters[filterName].addItems(param['options'])
                if filterName in ('type', 'size'):
                    lineEdit = QLineEdit()
                    self.filters[filterName].setLineEdit(lineEdit)
                    completer = QCompleter(param['options'])
                    completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
                    self.filters[filterName].setCompleter(completer)

                if 'default' in param:
                    self.filters[filterName].setCurrentText(param['default'])
            elif param['widget'] is QLineEdit:
                self.filters[filterName] = param['widget']()
                if 'options' in param:
                    completer = QCompleter(param['options'])
                    self.filters[filterName].setCompleter(completer)
            # color custom build     
            elif filterName == 'color':
                colorBox = QtWidgets.QGridLayout()
                self.filters['color']  = []
                pos_r = 0
                pos_c = 0
                for option in param['options']:
                    colorQRButton = QRadioButton(option)
                    colorBox.addWidget(colorQRButton, pos_r, pos_c)
                    if pos_c == 3:
                        pos_r += 1
                        pos_c = 0
                    else:
                        pos_c += 1
                    self.filters['color'].append(colorQRButton)
                filterPanelLayout.addLayout(colorBox, *param['pos'], 
                    alignment=QtCore.Qt.AlignBottom)
                continue
            filterPanelLayout.addWidget(self.filters[filterName],
                *param['pos'], alignment=QtCore.Qt.AlignBottom)
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
