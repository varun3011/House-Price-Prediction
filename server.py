from flask import Flask, request, jsonify
from flask import render_template, url_for, flash, get_flashed_messages, redirect
import util
import json
from form import PredictForm
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['house']



app = Flask(__name__)
app.config['SECRET_KEY'] = 'b0cafc1c41a7468f36893a80'

__predicted_price = None
__category = None
with open("locations_ - Copy.json", "r") as f:
    data = json.load(f)

locations_ = {}
for item in data:
    name = item["name"]
    lat = item["latitude"]
    lng = item["longitude"]
    locations_[name] = {"lat": lat, "lng": lng}

@app.route('/', methods=['GET','POST'])
# def index():

def predict_page():
    location_name = None
    lat = None
    lng = None
    if request.method == "POST":
        location_name = request.form["location"]
        lat = locations_[location_name]["lat"]
        lng = locations_[location_name]["lng"]
    
    global __predicted_price
    global __category
    global location_selected
    form = PredictForm()
    locations = util.get_location_names()
    form.location.choices = locations
    if request.method == 'POST':
        total_sqft = int(request.form['total_sqft'])
        location = request.form['location']
        location_selected=location
        print(location_selected)
        Type_selected = request.form['Type']
        print(Type_selected)

        # print(locations_)

        # bhk = int(request.form['bhks'])
        # bath = int(request.form['bathrooms'])
        __predicted_price = util.get_estimated_price(location,total_sqft)
        __predicted_price=util.type_price(__predicted_price,Type_selected)
        
        print(__predicted_price)
        if __predicted_price >= 200:
            __predicted_price /= 100
            __category = "Crores"
        elif __predicted_price >= 100 and __predicted_price <= 200:
            __predicted_price /= 100
            __category = "Crore"
        else:
            __category = "Lakhs"
        # return jsonify({'predicted_price': __predicted_price})

        # if __predicted_price <= 0:
        #     __predicted_price = None 
        #     __category = "House Not Available"
        # else:
        #     __predicted_price = round(__predicted_price, 1)
        return render_template('index1.html',locations_=list(locations_.keys()), location_name=location_name, lat=lat, lng=lng, form=form, predicted_price=__predicted_price, category=__category)

    if request.method == 'GET':
        __predicted_price = None
        return render_template('index1.html',locations_=list(locations_.keys()), location_name=location_name, lat=lat, lng=lng,form=form, predicted_price=__predicted_price, category=__category)

    render_template('index1.html')

@app.route('/submit-comment', methods=['POST'])
def submit_comment():
    name = request.form['name']
    email = request.form['email']
    comment = request.form['comment']

    comment_doc = {
        'name': name,
        'email': email,
        'comment': comment
    }

    db.comments.insert_one(comment_doc)

    return 'Comment submitted successfully!'

@app.route('/dashboard_')
def dashboard_():
    return render_template('dashboard.html')

if __name__ == "__main__":
    util.load_saved_artifacts()
    app.run(debug = True, threaded=True,host='0.0.0.0', port=80)