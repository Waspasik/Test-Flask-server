import pymongo
import json
from bson.json_util import dumps
from flask import Flask, render_template, request, redirect


app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://test_user:user231@cluster0.zglhhzj.mongodb.net/?retryWrites=true&w=majority")
db = client.testDB
collection = db.users


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return render_template('create-user.html')
    else:
        return render_template('base.html')


@app.route('/create-user', methods=['POST', 'GET'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        collection.insert_one({'username': username, 'password': password})    # write data to database
        return redirect('/get-users')
    else:
        return render_template('create-user.html')


@app.route('/get-users', methods=['GET'])
def show_users():
    users = [user for user in collection.find()]
    return json.loads(dumps(users, indent=3, ensure_ascii=False))    # return users from database in JSON


if __name__ == '__main__':
    app.run(debug=True)