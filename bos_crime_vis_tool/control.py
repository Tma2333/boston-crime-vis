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


    def _clear_location(self):
        self._view.clear_location()
    

    def _update_location(self):
        lat, lon = utils.get_location(self.df, self.filters)
        msg = self._construct_status_msg()
        self._view.update_stats(msg)
        self._view.update_location(lat, lon, self._color, size=self._size)


    def _construct_status_msg(self):
        msg = ''
        for header, keys in self.filters.items():
            msg += header + ': '
            msg += ','.join(str(key) for key in keys)
            msg += '; '
        logging.debug(msg)
        return msg


    def _update_color(self, color):
        self._color = color


    def _update_size(self):
        size = self._view.filters['size'].currentText()
        logging.debug('size: {}'.format(size))
        if size == 'Auto':
            self._size = None
            return
        try:
            self._size = float(size)
        except:
            logging.warn('Not a valid number')
            return
        


    def _update_filters(self, dfheader, uiheader):
        logging.debug('dfheader: {}'.format(dfheader))
        logging.debug('uiheader: {}'.format(uiheader))
        
        qtWidget = self._view.filters[uiheader]
        #==================================
        # add filter update here
        #==================================
        if isinstance(qtWidget, QComboBox):
            # years filter
            if uiheader == 'year1' or uiheader == 'year2':
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

            # month filter
            if uiheader == 'month1' or uiheader == 'month2':
                month1 = int(qtWidget.currentText())
                if uiheader == 'month1':
                    month2 = self._view.filters['month2'].currentText()
                else:
                    month2 = self._view.filters['month1'].currentText()
                months = sorted([month1, int(month2)])
                months[1] += 1
                months = list(range(months[0], months[1]))
                logging.debug(months)
                # update filters
                self.filters[dfheader] = months
                logging.debug('filter: {}'.format(self.filters[dfheader]))

            # weeks filter
            elif uiheader == 'week1' or uiheader =='week2':
                weekOptions = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                week1 = qtWidget.currentText()
                if uiheader == 'week1':
                    week2 = self._view.filters['week2'].currentText()
                else:
                    week2 = self._view.filters['week1'].currentText()
                index1 = weekOptions.index(week1)
                index2 = weekOptions.index(week2)
                if index1 >= index2:
                    weeks = weekOptions[index2:index1+1]
                else:
                    weeks = weekOptions[index1:index2+1]
                # update filters
                self.filters[dfheader] = weeks
                logging.debug('filter: {}'.format(self.filters[dfheader]))

            # hour filter
            if uiheader == 'hour1' or uiheader == 'hour2':
                hour1 = int(qtWidget.currentText())
                if uiheader == 'hour1':
                    hour2 = self._view.filters['hour2'].currentText()
                else:
                    hour2 = self._view.filters['hour1'].currentText()
                hours = sorted([hour1, int(hour2)])
                hours[1] += 1
                hours = list(range(hours[0], hours[1]))
                logging.debug(hours)
                # update filters
                self.filters[dfheader] = hours
                logging.debug('filter: {}'.format(self.filters[dfheader]))
            # offense type
            elif uiheader == 'type':
                all_type = list(self.df['OFFENSE_CODE_GROUP'].unique().astype('str'))
                offense_type = qtWidget.currentText()
                if offense_type == 'All':
                    self.filters[dfheader] = 'all'
                else:
                    self.filters[dfheader] = [offense_type]
                logging.debug('filter: {}'.format(self.filters[dfheader]))
            # district filter
            elif uiheader == 'district':
                all_district = list(self.df['DISTRICT'].unique().astype('str'))
                all_district.remove('nan')
                district_index = {'Downtown':['A1'], 'Charlestown':['A15'], 'East Boston':['A7'],
                                  'Roxbury':['B2'], 'Mattapan':['B3'], 'South Boston':['C6'],
                                  'Dorchester':['C11'], 'South End':['D4'], 'Brighton':['D14'],
                                  'West Roxbury':['E5'], 'Jamaica Plain':['E13'], 'Hyde Park':['E18'],
                                  'All': 'all'}
                district = qtWidget.currentText()
                district = district_index[district]
                self.filters[dfheader] = district
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
        self._view.filters['clear'].clicked.connect(self._clear_location)
        # year filters
        self._update_filters('YEAR', 'year1')
        self._view.filters['year1'].currentTextChanged.connect(
            partial(self._update_filters, 'YEAR', 'year1'))
        self._view.filters['year2'].currentTextChanged.connect(
            partial(self._update_filters, 'YEAR', 'year2'))
        # month filters
        self._update_filters('MONTH', 'month1')
        self._view.filters['month1'].currentTextChanged.connect(
            partial(self._update_filters, 'MONTH', 'month1'))
        self._view.filters['month2'].currentTextChanged.connect(
            partial(self._update_filters, 'MONTH', 'month2'))            
        # week filters
        self._update_filters('DAY_OF_WEEK', 'week1')
        self._view.filters['week1'].currentTextChanged.connect(
            partial(self._update_filters, 'DAY_OF_WEEK', 'week1'))
        self._view.filters['week2'].currentTextChanged.connect(
            partial(self._update_filters, 'DAY_OF_WEEK', 'week2'))
        # hour filters
        self._update_filters('HOUR', 'hour1')
        self._view.filters['hour1'].currentTextChanged.connect(
            partial(self._update_filters, 'HOUR', 'hour1'))
        self._view.filters['hour2'].currentTextChanged.connect(
            partial(self._update_filters, 'HOUR', 'hour2'))                 
        # district filters 
        self._update_filters('DISTRICT', 'district')
        self._view.filters['district'].currentTextChanged.connect(
            partial(self._update_filters, 'DISTRICT', 'district'))
        # type filters
        self._update_filters('OFFENSE_CODE_GROUP', 'type')
        self._view.filters['type'].currentTextChanged.connect(
            partial(self._update_filters, 'OFFENSE_CODE_GROUP', 'type'))       
        # size
        self._size = None
        self._view.filters['size'].currentTextChanged.connect(self._update_size)
        # colors
        self._color = 'red'
        for colorButtom in self._view.filters['color']:
            colorButtom.clicked.connect(partial(self._update_color, colorButtom.text()))