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
        self._view.clear_location()
        self._view.update_location(lat, lon, 'r')


    def _update_filters(self, iheader, eheader):
        logging.debug('iheader: {}'.format(iheader))
        logging.debug('eheader: {}'.format(eheader))
        
        external = self._view.filters[eheader]
        if isinstance(external, QComboBox):
            if eheader == 'year':
                key = int(external.currentText())
                if key == 'all':
                    self.filters[iheader] = []
                    logging.debug('filter: {}'.format(self.filters[iheader]))
                else:
                    self.filters[iheader] = list([key])
                    logging.debug('filter: {}'.format(self.filters[iheader]))
        
        
    def _connectSignals(self):
        # update bottom
        self._view.filters['update'].clicked.connect(self._update_location)
        # year filters
        self._update_filters('YEAR', 'year')
        self._view.filters['year'].currentTextChanged.connect(
            partial(self._update_filters, 'YEAR', 'year'))