from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# In-memory opslag (bijvoorbeeld)
sensor_data = {'temperature': 0, 'humidity': 0}
settings = {'interval': 60}  # in seconden

# Webpagina met form
html_template = """
<!doctype html>
<title>ESP32 Sensor Dashboard</title>
<h1>Sensorwaarden</h1>
<p>Temperatuur: {{ temp }} °C</p>
<p>Luchtvochtigheid: {{ hum }} %</p>

<h2>Instellingen aanpassen</h2>
<form action="/set" method="post">
  Interval (seconden): <input type="number" name="interval" value="{{ interval }}">
  <input type="submit" value="Opslaan">
</form>
"""

@app.route("/")
def index():
    return render_template_string(html,
                                    temperature=sensor_data["temperature"],
                                  humidity=sensor_data["humidity"],
                                  interval=settings["interval"])

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    sensor_data.update(data)
    return "OK"

@app.route("/config", methods=["GET"])
def config():
    return jsonify(settings)

@app.route("/set", methods=["POST"])
def set_interval():
    settings["interval"] = int(request.form["interval"])
    return index()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)