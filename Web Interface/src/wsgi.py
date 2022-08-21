from flask import Flask, render_template
from serialInterface import SerialContact

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False,
                template_folder="../templates", static_folder="../static")
    with app.app_context():
        app.SerialContact = SerialContact()
        return app


app = init_app()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/dronePos", methods=["POST"])
def callDronePos():

    return {"lat":app.SerialContact.getDroneLat(),"lon":app.SerialContact.getDroneLon()}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2020, debug=True)

