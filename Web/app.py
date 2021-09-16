from flask import Flask, render_template, url_for, jsonify, request, redirect
import numpy as np
import gravity_plot
import pandas as pd
import os
from os.path import join, dirname, realpath

app = Flask(__name__)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def apply_corrections(df, values):

    missing_corrections = False

    # If Tide Correction is selected
    if request.form.getlist('tide-corr'):
        if 'Tidal Correction' in df.columns:
            tide_correction_list = df['Tidal Correction'].tolist()
            for i in range(len(values)):
                values[i] += tide_correction_list[i]
        else:
            missing_corrections = True

    # If Gravity Correction is selected
    if request.form.getlist('grav-corr'):
        if 'Gravity Correction' in df.columns:
            gravity_correction_list = df['Gravity Correction'].tolist()
            for i in range(len(values)):
                values[i] += gravity_correction_list[i]
        else:
            missing_corrections = True

    return missing_corrections


# Get the uploaded files
@app.route("/", methods=['GET', 'POST'])
def upload_files():

    # Default landing page
    if request.method == 'GET':
        return render_template('index.html')

    # Display map
    else:
        csv_file = request.files['file']
        df = pd.read_csv(csv_file)
        lat_list = df['Latitude(deg)'].tolist()
        long_list = df['Longitude(deg)'].tolist()
        values_list = df['Values'].tolist()

        missing_corrections = apply_corrections(df, values_list)

        polygons, c_bar, lat, long = gravity_plot.gmap_output(lat_list, long_list, values_list)

        return jsonify(polygon_values=polygons, color_bar_values=c_bar, lat=lat, long=long,
                       missing_corrections=missing_corrections)


if __name__ == '__main__':
    app.run(debug=True)
