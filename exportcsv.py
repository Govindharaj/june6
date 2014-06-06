#!/usr/bin/python
##
#   @file       exportcsv.py
#
#   @brief      read class definitions.
#
#   @package    exportcsv
#   @module     exportcsv
#   @copyright

##
#   @class      exportcsv
#   @brief      export csv class definition
#
#   @module    exportcsv
#   @see

import csv
import time
import socket
from traindb.traindb import traindb as dbConnection
from config.config import config as setting
from log.log import log as logger
class exportcsv:
    db = None
    c = None
    def __init__(self):
        self.c = setting()
        self.logging = logger('export')
        databasePath = self.c.get('parser', 'db_path')
        self.db = dbConnection(databasePath, self.logging)
        self.writeCsv()
        dataClean = int(self.c.get('exportcsv', 'data_clean'))
        if 1 == int(dataClean):
            self.db.deleteAllTicketDetails()

    def writeCsv(self):
        filename= self.c.get ('exportcsv', 'output_path') + '/' + socket.gethostname() + '.csv'
        file  = open(filename, "a")
        writer = csv.writer(file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
        data = self.db.getAllTickets()
        for row in data:
            writer.writerow(list(row))
        file.close()

if __name__ == "__main__":
    exportcsv()