import sys
import logging
import argparse
from PyQt5 import QtCore, QtWidgets
import bos_crime_vis_tool as vis_tool

def main(args):
    # logging setup
    if args.logger_level == 'DEBUG':
        logging_level=logging.DEBUG
    elif args.logger_level == 'INFO':
        logging_level=logging.INFO
    elif args.logger_level == 'WARN':
        logging_level=logging.WARN
    elif args.logger_level == 'ERROR':
        logging_level=logging.ERROR

    logging.basicConfig(format='[%(levelname)s]%(asctime)s %(message)s', 
        datefmt='%H:%M:%S', 
        level=logging_level)
    # import data
    df = vis_tool.utils.import_data()
    # setup qt application
    app = QtWidgets.QApplication([])
    view = vis_tool.gui.bosCrimeMapUI(df=df)
    view.show()
    control = vis_tool.control.bosCrimeMapCtrl(view, df)
    sys.exit(app.exec())
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--logger_level', dest='logger_level',
                        help='logger level', default='INFO',
                        choices=['DEBUG','INFO','WARN','ERROR'])
    args = parser.parse_args()
    main(args)