
import csv
from traindb.traindb import traindb as dbConnection
from config.config import config as setting
from log.log import log as logger
import argparse
def exportcsv(dataType):

    c = setting()
    l = logger('exportData')
    databasePath = c.get('parser', 'db_path')
    db = dbConnection(databasePath, l)
    try:
        filename= c.get ('exportcsv', 'output_path') + '/export-data-' + dataType + '.csv'
        file  = open(filename, "w")
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        data = []
        if 'station' == dataType:
            headers = db.getAllStationInfoHeaders()
            data = db.getAllStationInfo()
        elif 'train' == dataType:
            headers = db.getAllTrainInfoHeaders()
            data = db.getAllTrainInfo()
        # Writing the values
        writer.writerow(list(headers))
        for row in data:
            writer.writerow(list(row))
        file.close()

    except (IOError, Exception) as e:
            print e

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Exporting the data from db table to csv')
    parser.add_argument('-t','--type', help='export station/train info', required=False, default='station', choices=['station','train'])
    args = vars(parser.parse_args())
    dataType = args['type']
    exportcsv(dataType)