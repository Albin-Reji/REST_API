import mysql.connector
from flask import Flask, render_template, jsonify, request, redirect, url_for, session

app=Flask(__name__)


app.secret_key = 'albin@democracy@123'
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
    return  render_template('post.html')


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


@app.route("/add", methods=["POST"])
def post():
    # Retrieve values from the submitted form
    id=request.form.get('id')
    name = request.form.get('name')
    map_url = request.form.get('map_url')
    img_url = request.form.get('img_url')
    location = request.form.get('loc')
    sockets = bool(request.form.get('sockets'))
    toilet = bool(request.form.get('toilet'))
    wifi = bool(request.form.get('wifi'))
    calls = bool(request.form.get('calls'))
    seats = request.form.get('seats')
    coffee_price = request.form.get('coffee_price')

    form_data = {
        "id":id,
        "name": name,
        "map_url": map_url,
        "img_url": img_url,
        "location": location,
        "sockets": sockets,
        "toilet": toilet,
        "wifi": wifi,
        "calls": calls,
        "seats": seats,
        "coffee_price": coffee_price
    }
    session['form_data'] = form_data
    sql_query = """
    INSERT INTO cafes (id, name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price)
    VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        form_data["id"],
        form_data["name"],
        form_data["map_url"],
        form_data["img_url"],
        form_data["location"],
        form_data["sockets"],
        form_data["toilet"],
        form_data["wifi"],
        form_data["calls"],
        form_data["seats"],
        form_data["coffee_price"]
    )
    mycursor.execute(sql_query, values)
    mydb.commit()

    return redirect(url_for('details'))

@app.route("/print")
def details():
    form_data = session.get('form_data')
    return jsonify(form_data)





if __name__=="__main__":
    app.run(debug=True)