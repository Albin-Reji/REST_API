import mysql.connector
from flask import Flask, render_template, jsonify, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = Key

# Connect to MySQL using mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=PassWord, 
    database="rest"
)

mycursor = mydb.cursor()


def convert_jsonify(random_cafe):
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
    return render_template('index.html')


@app.route("/random", methods=['GET'])
def get_random_cafe():
    mycursor.execute("SELECT name FROM cafes ORDER BY RAND() LIMIT 1")
    for i in mycursor:
        mycursor.execute(f"SELECT * FROM cafes WHERE name='{i[0]}'")
        for random_cafe in mycursor:
            json_response = convert_jsonify(random_cafe)
    return jsonify(json_response)


@app.route("/getall", methods=['GET'])
def get_all():
    mycursor.execute("SELECT * FROM cafes")
    json_list = [convert_jsonify(i) for i in mycursor]
    return jsonify(json_list)


@app.route('/search', methods=["GET"])
def search():
    loc = request.args.get('loc')
    mycursor.execute(f"SELECT * FROM cafes WHERE location='{loc}'")
    res_list = [convert_jsonify(val) for val in mycursor]
    if res_list:
        return jsonify(res_list)
    else:
        return jsonify({"error": "location not found", "code": 404})


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        try:
            # Retrieve values from the submitted form
            id = int(request.form.get('id'))
            name = request.form.get('name')
            map_url = request.form.get('map_url')
            img_url = request.form.get('img_url')
            location = request.form.get('loc')
            sockets = 'sockets' in request.form
            toilet = 'toilet' in request.form
            wifi = 'wifi' in request.form
            calls = 'calls' in request.form
            seats = request.form.get('seats')
            coffee_price = request.form.get('coffee_price')

            form_data = {
                "id": id,
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

            # SQL query to insert data
            sql_query = """
            INSERT INTO cafes (id, name, map_url, img_url, location, has_sockets, has_toilet, has_wifi, can_take_calls, seats, coffee_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

            # Execute the query
            mycursor.execute(sql_query, values)
            mydb.commit()

            return redirect(url_for('details'))

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "Failed to add cafe details", "details": str(err)})

    # Render the form for GET request
    return render_template('post.html')


@app.route("/print")
def details():
    form_data = session.get('form_data')
    return jsonify(form_data)

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_cafe(id):
    if request.method == "POST":
        try:
            # Retrieve values from the submitted form
            name = request.form.get('name')
            map_url = request.form.get('map_url')
            img_url = request.form.get('img_url')
            location = request.form.get('loc')
            sockets = 'sockets' in request.form
            toilet = 'toilet' in request.form
            wifi = 'wifi' in request.form
            calls = 'calls' in request.form
            seats = request.form.get('seats')
            coffee_price = request.form.get('coffee_price')

            # SQL query to update data
            sql_query = """
            UPDATE cafes 
            SET name=%s, map_url=%s, img_url=%s, location=%s, has_sockets=%s, has_toilet=%s, has_wifi=%s, can_take_calls=%s, seats=%s, coffee_price=%s 
            WHERE id=%s
            """
            values = (
                name,
                map_url,
                img_url,
                location,
                sockets,
                toilet,
                wifi,
                calls,
                seats,
                coffee_price,
                id
            )

            # Execute the query
            mycursor.execute(sql_query, values)
            mydb.commit()

            return redirect(url_for('details'))

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "Failed to update cafe details", "details": str(err)})

    else:
        # Fetch existing cafe details for the given ID
        mycursor.execute(f"SELECT * FROM cafes WHERE id={id}")
        cafe = mycursor.fetchone()
        if cafe:
            return render_template('update.html', cafe=cafe)
        else:
            return jsonify({"error": "Cafe not found", "code": 404})


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete_cafe(id):
    if request.method == "POST":
        try:
            # SQL query to delete cafe based on the id
            sql_query = "DELETE FROM cafes WHERE id = %s"
            values = (id,)
            mycursor.execute(sql_query, values)
            mydb.commit()
            return redirect(url_for('home'))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return jsonify({"error": "Failed to delete cafe", "details": str(err)})

    else:
        # Fetch existing cafe details for confirmation
        mycursor.execute(f"SELECT * FROM cafes WHERE id={id}")
        cafe = mycursor.fetchone()
        if cafe:
            return render_template('delete.html', cafe=cafe)
        else:
            return jsonify({"error": "Cafe not found", "code": 404})


if __name__ == "__main__":
    app.run(debug=True)
