from flask import Flask, render_template, url_for, jsonify, request, redirect
import numpy as np
import gravity_plot
import pandas as pd
import os
from os.path import join, dirname, realpath

app = Flask(__name__)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Get the uploaded files
@app.route("/", methods=['GET', 'POST'])
def uploadFiles():

    if request.method == 'GET':
        return render_template('index.html')

    else:
        csv_file = request.files['file']
        df = pd.read_csv(csv_file)
        lat_list = df['Latitude(deg)'].tolist()
        long_list = df['Longitude(deg)'].tolist()
        values_list = df['Values'].tolist()
        if 'Tidal Correction' in df.columns:
            tide_correction_list = df['Tidal Correction'].tolist()
        else:
            tide_correction_list = None

        polygons, c_bar, lat, long = gravity_plot.gmap_output(lat_list, long_list, values_list, tide_correction_list)
        return render_template('index.html', polygon_array=polygons, color_bar=c_bar, lat=lat, long=long)






# @app.route('/hello', methods=['GET', 'POST'])
# def hello():
#
#     # POST request
#     if request.method == 'POST':
#         print('Incoming..')
#         print(request.get_json())  # parse as JSON
#         return 'OK', 200
#
#     # GET request
#     else:
#         print("Czechoslovakia")
#         message = {'greeting':'Hello from Flask!'}
#         return jsonify(message)  # serialize and use JSON headers
#
# @app.route('/test')
# def test_page():
#     # look inside `templates` and serve `index.html`
#     return render_template('ajax.html')



if __name__ == '__main__':
    app.run(debug=True)