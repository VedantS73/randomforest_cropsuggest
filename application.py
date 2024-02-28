from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import webbrowser
from threading import Timer
import pickle
from utils import getweather, get_weather_by_lat_lon, get_weather_by_polygon, get_7_day_forecast

model = pickle.load(open('RandomForest69.pkl','rb'))
print(1)

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return "Try to use /predict endpoint"

@app.route('/predict',methods=['POST'])
def predict():
    N = request.form.get('N')
    P = request.form.get('P')
    K = request.form.get('K')

    temperature = request.form.get('temperature')
    humidity = request.form.get('humidity')
    ph = request.form.get('ph')
    rainfall = request.form.get('rainfall')

    input_query = np.array([[N,P,K,temperature,humidity,ph,rainfall]])
    # result = model.predict(input_query)[0]

    N = 4  # Change this to the desired number of top suggestions
    predicted_probabilities = model.predict_proba(input_query)
    top_n_indices = np.argsort(-predicted_probabilities, axis=1)[:, :N]
    top_n_crops = [[model.classes_[index] for index in indices] for indices in top_n_indices]

    predic_list = []

    for i, crops in enumerate(top_n_crops):
        predic_list = crops

    print(predic_list)

    return jsonify({'crop':predic_list})

@app.route('/curr_weather',methods=['GET'])
def curr_weather():
    return getweather()

@app.route('/curr_loc_data',methods=['POST'])
def curr_weathere():
    print("hello server recieved a request")
    print(request.json)
    data = request.json

    if 'lat' in data and 'lon' in data:
        lat = data['lat']
        lon = data['lon']
        weather_data = get_weather_by_lat_lon(lat, lon)
        return weather_data
    elif 'points' in data:
        print("polygon")
        points = data['points']
        weather_data = get_weather_by_polygon(points)
        return weather_data
    else:
        return jsonify({'error': 'Invalid parameters'})

@app.route('/seven_day_forecast',methods=['POST'])
def seven_day():
    print("hello thus is moeeeee moeeee")
    data = request.json
    data = data['pointreq']
    print("data is: ",data)

    lat = data['lat']
    lon = data['lon']
    weather_data = get_7_day_forecast(lat, lon)
    return weather_data

    
if __name__ == '__app__':
    app.run(debug=True)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:2000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(port=2000)
