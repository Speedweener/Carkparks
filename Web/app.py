from flask import Flask, render_template, url_for, jsonify, request
import numpy as np
import gravity_plot

app = Flask(__name__)
lat_sample, long_sample, values = gravity_plot.generate_values()
polygons, c_bar, lat, long = gravity_plot.gmap_output(lat_sample, long_sample, values)

# @app.route('/update_decimal', methods=['POST'])
# def update_decimal():
#     random_number = np.random.rand()
#     return jsonify('', render_template('random_decimal_model.html', x=random_number))


@app.route('/')
def index():
    return render_template('index.html', polygon_array=polygons, color_bar=c_bar, lat=lat, long=long)


if __name__ == '__main__':
    app.run(debug=True)
