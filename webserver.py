from flask import Flask, send_file

from weatherdata.data_handler import DataHandler

app = Flask(__name__)
data_handler = DataHandler()
data_handler.get_weather_data()


@app.route('/weather', methods=['GET'])
def get_weather():
    data_handler.get_weather_data()
    # Replace this with your actual weather data fetching logic
    # return "200/ok"


# TODO: Use ony one endpoint to get all images
@app.route('/get_temp_image', methods=['GET'])
def get_temp_image():
    image_path = 'figures/Temperature.png'
    return send_file(image_path, mimetype='image/png')


@app.route('/get_cloud_image', methods=['GET'])
def get_cloud_image():
    image_path = 'figures/Clouds.png'
    return send_file(image_path, mimetype='image/png')


@app.route('/get_wind_image', methods=['GET'])
def get_wind_image():
    image_path = 'figures/WindVisibility.png'
    return send_file(image_path, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
