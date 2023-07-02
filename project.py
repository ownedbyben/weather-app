from flask import Flask, request, render_template, send_from_directory
import requests
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from prometheus_client import Counter
import os
import json
import datetime

app = Flask(__name__)

bg_color = os.environ.get('BG_COLOR', 'lightblue')

# Define the path to the data folder
data_folder = os.path.join(app.root_path, 'data')
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Add prometheus wsgi middleware to route /metrics requests
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

city_views_total = Counter('city_views_total', 'Description of counter', ['city'])

@app.route("/")
def index():
    return render_template('form.html')


@app.route('/history')
def history():
    # Get the list of JSON files in the data folder
    files = [f for f in os.listdir(data_folder) if f.endswith('.json')]
    return render_template('history.html', files=files, bg_color=bg_color)

@app.route('/history/download/<filename>')
def download_file(filename):
    # Return the requested file from the data folder
    return send_from_directory(data_folder, filename, as_attachment=True)


@app.route('/result', methods=["POST"])
def result():
    try:
        return rtrn_param()
    except Exception as e:
        return f"could not find the locate weather for {request.form['cc_location']}: {e}"



def rtrn_param():
    items = locate()
    country = items[2]
    location = items[3]
    days = api()
    temp_day = days[0]
    temp_night = days[1]

    # Save the search query data to a JSON file
    save_search_query(location, country, temp_day, temp_night)

    return render_template('result.html', country=country, location=location, temp_day=temp_day, temp_night=temp_night)


def locate():
    location = request.form['cc_location']

    res = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={location}").json()
    lat = (res['results'][0]['latitude'])
    lon = (res['results'][0]['longitude'])
    country = (res['results'][0]['country'])

    return lat, lon, country, location


def api():
    locate_result = locate()
    city_views_total.labels(city=locate_result[3]).inc()
    lati = (locate_result[0])
    long = (locate_result[1])

    res = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lati}&longitude={long}&daily=temperature_2m_max,temperature_2m_min&timezone=auto')
    json_obj = res.json()
    temp_day = (json_obj['daily']['temperature_2m_max'])
    if temp_day is None:
        raise Exception("temp_day exception")

    temp_night = (json_obj['daily']['temperature_2m_min'])
    if temp_night is None:
        raise Exception("temp_night exception")

    return temp_day, temp_night

def save_search_query(location, country, temp_day, temp_night):
    now = datetime.datetime.now()
    data = {
        'date': now.strftime('%Y-%m-%d'),
        'city': location,
        'country': country,
        'temp_day': temp_day,
        'temp_night': temp_night
    }

    filename = f"{now.strftime('%Y-%m-%d')}-{location}.json"
    filepath = os.path.join(data_folder, filename)

    with open(filepath, 'w') as file:
        json.dump(data, file)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port='5000')
