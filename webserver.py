from flask import Flask, send_file, render_template

from exceptionhandler.exception_handler import print_debug_message
from weatherdata.data_handler import DataHandler

#
data_handler = DataHandler()
data_handler.get_weather_data()

RETURN_NOT_FOUND = "400"

# TODO Do not use it in a production deployment. Use a production WSGI server instead.
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


# TODO: Why is the fetching/data processing is running twice on start?

@app.route('/weather', methods=['GET'])
def get_weather():

    # data_handler.get_weather_data()
    # Replace this with your actual weather data fetching logic
    return "200/ok"


# TODO: Use ony one endpoint to get all images
@app.route('/get_temp_image', methods=['GET'])
def get_temp_image():
    print_debug_message("Webserver", "returning temp image")
    image_path = 'figures/Temperature.png'
    return send_file(image_path, mimetype='image/png')


@app.route('/get_cloud_image', methods=['GET'])
def get_cloud_image():
    image_path = 'figures/Clouds.png'
    try:
        return send_file(image_path, mimetype='image/png')
    except FileNotFoundError as e:
        return RETURN_NOT_FOUND


@app.route('/get_wind_image', methods=['GET'])
def get_wind_image():
    image_path = 'figures/WindVisibility.png'
    try:
        return send_file(image_path, mimetype='image/png')
    except FileNotFoundError as e:
        return RETURN_NOT_FOUND


@app.route('/', methods=['GET'])
def clouds():
    image_path = 'Ellwangen-Rindelbach.html'
    try:
        return render_template(image_path)  # send_file(image_path, mimetype='html')
    except FileNotFoundError:
        return RETURN_NOT_FOUND


if __name__ == '__main__':
    #data_handler.get_weather_data()
    app.run(host='0.0.0.0', port=5000, debug=True)  # host='0.0.0.0',
