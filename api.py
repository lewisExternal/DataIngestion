import sqlite3
from flask import Flask
from flask import request, jsonify
import pandas as pd 
import db_lib

app = Flask(__name__)

def main():
  
    # define database name 
    database = r"pythonsqlite.db"
    
    @app.route('/api/v1/overviewreport', methods=['GET'])
    def return_overviewreport():
       
        # get connection to db 
        conn = db_lib.create_connection(database)
        print("Connection to the DB established.")

        # query for the report 
        if conn is not None:
            result = db_lib.overview_report(conn)
        else: 
            return "Error: DB call failed."

        resultDict = {
                        "num_meters": result[0],
                        "num_files": result[1]
                    }

        return jsonify(resultDict)
   
    @app.route('/api/v1/lastfilereport', methods=['GET'])
    def return_lastfilereport():
       
        # get connection to db 
        conn = db_lib.create_connection(database)
        print("Connection to the DB established.")

        # query for the report 
        if conn is not None:
            result = db_lib.last_file_report(conn)
        else: 
            return "Error: DB call failed."

        resultDict = {
                        "last_file": result[0],
                        "time_stamp": result[1]
                    }

        return jsonify(resultDict)

    @app.route('/api/v1/meterdata', methods=['GET'])
    def return_meterdata():
       
        # get connection to db 
        conn = db_lib.create_connection(database)
        print("Connection to the DB established.")

        if 'meter' in request.args:
            meter_data = str(request.args['meter'])
        else:
            return "Error: No date field provided. Please specify a date."

        # query for the report 
        if conn is not None:
            result = db_lib.meter_data(conn,meter_data)
        else: 
            return "Error: DB call failed."
        
        # add result to dict 
        resultDict = {}
        counter = 0 
        for row in result:
            resultDict[str(counter)] = str(row)
            counter =  counter + 1 

        return jsonify(resultDict)

    # run the app 
    app.run()

if __name__ == '__main__':
    main()