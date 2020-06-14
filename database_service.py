import psycopg2 as psy
from flask import Flask, jsonify
from flask import request
import json


connection = psy.connect(user="tester", password="password",host="localhost", database="my_barmej")


app = Flask(__name__)

@app.route('/get_total_data_count', methods=['GET'])
def get_total_data_count():
    count = 0
    cursor = connection.cursor()
    label_name = request.args.get('label_name')
    try:
      
        if label_name == "positive":  
            cursor.execute("select count(text_id) from data_labling where label_id = 1 ;")
            count =  cursor.fetchall()
        elif label_name == "positive" and count == 1000:
            cursor.execute("select count(text_id) from data_labling where label_id = 1 limit 1000;")
            count = cursor.fetchall()
        elif label_name == "negative":  
            cursor.execute("select count(text_id) from data_labling where label_id = 0 ;")
            count = cursor.fetchall()
        elif label_name == "negative" and count == 1000:
            cursor.execute("select count(text_id) from data_labling where label_id = 0 limit 1000;")
            count = cursor.fetchall()
        elif label_name == "all":  
            cursor.execute("select count(text_id) from data_labling;")
            count =  cursor.fetchall()

        return jsonify(count)

    except Exception as error:
        print ("ERROR IN get_total_data_count ")
        print ("Exception TYPE:", type(error))



@app.route('/get_data', methods=['GET'])
def get_data():
    cursor = connection.cursor()
    count = request.args.get('count')
    skip = request.args.get('skip')
    sort_order = request.args.get('sort_order')
    try:
        query = "select x.text , y.label_id from data_input as x INNER JOIN data_labling as y ON x.id=y.id order by x.input_date %s limit %s offset %s ;"
        param = (sort_order, count, skip)
        cursor.execute(query % param)
        label_text = cursor.fetchall()
        text, label = zip(*label_text)
        return jsonify(label_text)

    except Exception as error:
        print("Exception TYPE:", type(error))




if __name__ == "__main__":
    app.run(debug=True, port=3000)
