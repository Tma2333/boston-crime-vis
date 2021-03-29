import logging
from functools import partial
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit

from . import utils

class bosCrimeMapCtrl(object):

    def __init__ (self, view, df):
        self.df = df
        self.filters = {}
        self._view = view
        self._connectSignals()

    
    def _update_location(self):
        lat, lon = utils.get_location(self.df, self.filters)
        msg = self._construct_status_msg()
        self._view.update_stats(msg)
        self._view.clear_location()
        self._view.update_location(lat, lon, 'r')


    def _construct_status_msg(self):
        msg = ''
        for header, keys in self.filters.items():
            msg += header + ': '
            msg += ','.join(str(key) for key in keys)
            msg += '; '
        logging.debug(msg)
        return msg



    def _update_filters(self, dfheader, uiheader):
        logging.debug('dfheader: {}'.format(dfheader))
        logging.debug('uiheader: {}'.format(uiheader))
        
        qtWidget = self._view.filters[uiheader]
        #==================================
        # add filter update here
        #==================================
        if isinstance(qtWidget, QComboBox):
            # years filter
            if uiheader == 'year1' or 'year2':
                year1 = int(qtWidget.currentText())
                if uiheader == 'year1':
                    year2 = self._view.filters['year2'].currentText()
                else:
                    year2 = self._view.filters['year1'].currentText()
                years = sorted([year1, int(year2)])
                years[1] += 1
                years = list(range(years[0], years[1]))
                logging.debug(years)
                # update filters
                self.filters[dfheader] = years
                logging.debug('filter: {}'.format(self.filters[dfheader]))
        elif isinstance(qtWidget, QPushButton):
            pass
        elif isinstance(qtWidget, QLineEdit):
            pass
    
        
        
    def _connectSignals(self):
        #==================================
        # add signal headling here
        #==================================
        # update bottom
        self._view.filters['update'].clicked.connect(self._update_location)
        # year filters
        self._update_filters('YEAR', 'year1')
        self._view.filters['year1'].currentTextChanged.connect(
            partial(self._update_filters, 'YEAR', 'year1'))
        self._view.filters['year2'].currentTextChanged.connect(
            partial(self._update_filters, 'YEAR', 'year2'))
        