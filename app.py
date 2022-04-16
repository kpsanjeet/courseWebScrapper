from flask import Flask, render_template, request, jsonify
import pymongo
import mysql.connector as conn

app = Flask(__name__)

@app.route('/database', methods=['POST']) # for calling the API from Postman/SOAPUI
def raed_database():

    ###################%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%####################################
    # For Mongodb

    # For Mysql

    ##########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##################

    # Inputs from via postman
    dbName = request.json['dbName']
    query = request.json['query']

    if (request.method=='POST'):

        if dbName == 'mongodb':

            db_config = "mongodb+srv://test:test@cluster0.tjuqz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
            client = pymongo.MongoClient(db_config)
            mdb = client["ineuron"]  # Database
            coll = mdb["courseDetails"]  # Collection

            def read_document(query: 'str') -> 'dict':
                field1 = {query: 1, '_id': False}
                doc = list(filter(lambda dict_: len(dict_) > 0, coll.find({}, field1)))[0]
                return list(doc.values())[0]

            result = read_document(query)
            client.close()
            return jsonify(result)
        else:
            mysql_db = conn.connect(host='127.0.0.1',
                              database='ineuronCourses',
                              user='root',
                              password='iitbhu')
            cursor = mysql_db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            mysql_db.close()
            return jsonify(result)



if __name__ == '__main__':
    app.run()
