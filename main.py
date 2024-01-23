import json

import mysql.connector
from flask import Flask, render_template, jsonify, request

app=Flask(__name__)
# Connect to MySQL using mysql.connector
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="albin@democracy@1234",
        database="rest"


)

mycursor = mydb.cursor()



def convertJsonyfy(random_cafe):
    price = random_cafe[10].replace('£', "")
    json_response = {
                    "id": random_cafe[0],
                    "name": random_cafe[1],
                    "map_url": random_cafe[2],
                    "img_url": random_cafe[3],
                    "location": random_cafe[4],
                    "seats": random_cafe[9],
                    "has_toilet": random_cafe[6],
                    "has_wifi": random_cafe[7],
                    "has_sockets": random_cafe[5],
                    "can_take_calls": random_cafe[8],
                    "coffee_price": price
                }
    return json_response

@app.route("/")
def home():
    return  render_template('index.html')


@app.route("/random", methods=['GET'])
def get_random_cafe():
    mycursor.execute("SELECT name FROM cafes ORDER BY RAND() LIMIT 1")
    for i in mycursor:
        mycursor.execute(f"SELECT * FROM cafes WHERE name='{i[0]}'")
        for random_cafe in mycursor:
            # for i in range(11):
            price=random_cafe[10].replace('£', "")

            json_response = {
                "id": random_cafe[0],
                "name": random_cafe[1],
                "map_url": random_cafe[2],
                "img_url": random_cafe[3],
                "location": random_cafe[4],
                "seats": random_cafe[9],
                "has_toilet": random_cafe[6],
                "has_wifi": random_cafe[7],
                "has_sockets": random_cafe[5],
                "can_take_calls": random_cafe[8],
                "coffee_price": price
            }

    return jsonify(json_response)

@app.route("/getall", methods=['GET'])
def getAll():
    mycursor.execute("SELECT * FROM cafes ")
    jsonList = []
    for i in mycursor:
        jsonList.append(convertJsonyfy(i))
    return jsonify(jsonList)



@app.route('/search', methods=["GET"])
def search():
    loc=request.args.get('loc')

    mycursor.execute(f"SELECT * FROM cafes WHERE location='{loc}'")
    resList = []
    for val in mycursor:
        resList.append(convertJsonyfy(val))
    if resList:
        return jsonify(resList)
    else:
        return  jsonify({"error":"location not founnd",
                         "code":404})

@app.route("/process_data", methods=["POST","GET"])
def post():
    if request.method=="POST":
        res=request.form
        return render_template("index.html", result=res)





if __name__=="__main__":
    app.run(debug=True)