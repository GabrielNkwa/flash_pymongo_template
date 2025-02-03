from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import webbrowser
import time

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://192.168.1.6:27017/Play1"
mongo = PyMongo(app)



@app.route("/")
def home():
    return render_template("test_play.html")

@app.route("/action1", methods=['GET','POST'])
def act1():
    nm = request.form.get("yid")
    age = request.form.get("yage")
    sex = request.form.get("ygender")
    pspt = request.files.get("ypt")
    print(nm,age,sex,pspt.filename)
    mongo.save_file(pspt.filename, pspt)
    data = {"Name": nm,"Age":age, "Gender":sex, "Passport":pspt.filename}
    mongo.db.USERS.insert_one(data)
    return render_template("test_play.html")

@app.route("/show")
def shh():
    data = mongo.db.USERS.find()
    data = list(data)
    return render_template('show_test.html', info=data)

@app.route('/loadpic/<pic>')
def gsg(pic):
    fid = mongo.db.fs.files.find_one({'filename':pic})
    id = fid['_id']
    img_path = mongo.db.fs.chunks.find_one({'files_id': fid['_id']})
    return img_path['data']


if __name__ == "__main__":
    webbrowser.open('http://localhost:5000')
    app.run('0.0.0.0', debug=True)