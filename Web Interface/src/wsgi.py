from flask import Flask, render_template
from serialInterface import SerialContact
import drone_pb2

requestTypes = {
    "dronePos": 1,
    "servo": 2
}

expectedLengths = {
    "dronePos": 18,
    "servo": 4
}

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False,
                template_folder="../templates", static_folder="../static")
    with app.app_context():
        return app


app = init_app()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/<apiCall>")
def callApi(apiCall):
    with SerialContact() as conn:
        myReq = drone_pb2.Request()
        myReq.requesttype = requestTypes[apiCall]
        requestBytes = myReq.SerializeToString()
        responseBytes = conn.makeRequest(requestBytes,expectedLengths[apiCall])
        if apiCall == "dronePos":
            myResponse = drone_pb2.LocationResponse()
            myResponse.ParseFromString(responseBytes)

            return {"lat":myResponse.lat,"lon":myResponse.lon}

        elif apiCall == "servo":
            myResponse = drone_pb2.InsecticideResponse()
            return {"code":myResponse.successful,"outOfJuice":myResponse.outOfJuice}
        



# print(myResponse.lat)
# print(myResponse.lon)

    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2020, debug=True)

