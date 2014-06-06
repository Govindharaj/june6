
import csv
from traindb.traindb import traindb as dbConnection
from config.config import config as setting
from log.log import log as logger
import argparse
import sys
def importcsv(dataType):

    c = setting()
    l = logger('exportData')
    databasePath = c.get('parser', 'db_path')
    db = dbConnection(databasePath, l)
    try:
        filename= c.get ('exportcsv', 'output_path') + '/import-data-' + dataType + '.csv'
        reader = csv.reader(open(filename, 'r'), delimiter=',')

        if 'station' == dataType:
            tablename = 'stationinfo'
        elif 'train' == dataType:
            tablename = 'traininfo'

        rowno = 1
        fields = ''
        for data in reader:
            if 1 == rowno:
                # Validating colums
                validColumns(dataType, data)
                # Drop the schema of table
                try:
                    db.cursor.execute('drop table ' + tablename)
                except Exception as e:
                    pass
                # create the table
                sql = createTable(tablename, data)
                db.cursor.execute(sql)
                # build the insert query
                sql = insertTable(tablename, data)
            else:
                # execute the  insert query
                try:
                    db.cursor.execute(sql, data)
                    db.connection.commit()
                except (IOError, Exception) as e:
                    print 'Error: Inserting row :' + e
            rowno += 1
        #db.connection.commit()
    except (IOError, Exception) as e:
            print e

def validColumns(dataType, data):
    err = 0

    if 'station' == dataType and 'code' not in data:
        print 'Column name code is required'
        err = 1
    elif 'train' == dataType and 'number' not in data:
        print 'Column name number is required'
        err = 1
    if 'nameEnglish' not in data:
        print 'Column name nameEnglish is required'
        err = 1
    if 'nameHindi' not in data:
        print 'Column name nameHindi is required'
        err = 1

    if err == 1:
        sys.exit(0)



def createTable(tableName, fields):
    sql= 'create table ' + tableName + ' ('

    for field in fields:
        sql += field + ' varchar(150) '
        if field == 'code' or field == 'number':
            sql += 'primary key '
        else:
            sql += ' DEFAULT (\'\') '
        sql += ','
    sql = sql[:-1] + ')'
    return sql

def insertTable(tablename, fields):
    f = ''
    v = ''
    i = 0
    for field in fields:
        f += ' \'' + field + '\','
        v += ' ?,'
        i += 1

    sql = 'INSERT INTO '+ tablename +' (' + f[:-1] + ' ) VALUES (' + v[:-1] + ') '
    return sql

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Exporting the data from db table to csv')
    parser.add_argument('-t','--type', help='export station/train info', required=False, default='station', choices=['station','train'])
    args = vars(parser.parse_args())
    dataType = args['type']
    importcsv(dataType)
