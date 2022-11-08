from flask import Flask, render_template, jsonify, request
import numpy as np
import datetime
import math
import pandas as pd
import pickle
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
app = Flask(__name__)

UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dtModel = pickle.load(open('dt.sav', 'rb'))
time_list = []
for hour in range(24):
    for minute in range(3):
        time_list.append([minute, hour])


def get_colour_bar():
    colour_bar_values = []
    minutes = ["05", "25", "45"]
    hours = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
             "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
             "20", "21", "22", "23"]
    for j in hours:
        for i in minutes:
            colour_bar_values.append(j + ":" + i)
    return colour_bar_values



# Get the uploaded files
@app.route("/", methods=['GET', 'POST'])
def index():

    # Default landing page
    if request.method == 'GET':
        return render_template('index.html')

    # Display map
    else:
        date = request.form.get('date')

        date_split = date.split("-")
        new_date = datetime.datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
        day_week_holiday = [new_date.weekday(), math.floor(int(date_split[2]) / 7)]  # Day, Week

        next_date = new_date + datetime.timedelta(days=1)
        next_date_day_week_holiday = [next_date.weekday(), math.floor(int(next_date.day) / 7)]  # Day, Week
        next_date_string = str(next_date.year) + '-' + str(next_date.month) + '-' + str(next_date.day)

        ph_2022 = pd.read_csv('holidays.csv')

        if ph_2022['Date'].str.contains(date).any():  # Holiday
            day_week_holiday.append(1)
        else:
            day_week_holiday.append(0)

        if ph_2022['Date'].str.contains(next_date_string).any():  # Holiday
            next_date_day_week_holiday.append(1)
        else:
            next_date_day_week_holiday.append(0)

        prediction_total = []
        # cluster	min	hour	day	week	holiday
        for i in range(len(time_list)):
            prediction_all_clusters = []
            for cluster in range(25):
                prediction_all_clusters.append(int(dtModel.predict(np.array(
                    [cluster] + time_list[i] + day_week_holiday).reshape(1, -1))))

            prediction_total.append(prediction_all_clusters)

        next_day_predictions = []
        for cluster in range(25):
            next_day_predictions.append(int(dtModel.predict(np.array(
                    [cluster] + [0, 0] + next_date_day_week_holiday).reshape(1, -1))))  # 12am next day

        # Future - Current
        for i in range(len(time_list)):
            if i == len(time_list) - 1:  # Account for last time of the day, minus the next day 12am
                for cluster in range(25):
                    prediction_total[i][cluster] = next_day_predictions[cluster] - prediction_total[i][cluster]

            else:
                for cluster in range(25):
                    prediction_total[i][cluster] = prediction_total[i+1][cluster] - prediction_total[i][cluster]

        return jsonify(color_bar_values=get_colour_bar(), predicted_values=prediction_total)
    # Values are sent in [hour:minute][cluster]


if __name__ == '__main__':
    app.run(debug=True)
