from flask import Flask, send_file, render_template

from weatherdata.data_handler import DataHandler

#
# data_handler = DataHandler()
# data_handler.get_weather_data()


# TODO Do not use it in a production deployment. Use a production WSGI server instead.
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

@app.route('/weather', methods=['GET'])
def get_weather():

    # data_handler.get_weather_data()
    # Replace this with your actual weather data fetching logic
    return "200/ok"


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


@app.route('/', methods=['GET'])
def clouds():
    image_path = 'Ellwangen-Rindelbach-Cloud Coverage.html'
    return render_template(image_path)# send_file(image_path, mimetype='html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # host='0.0.0.0',
