from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2020, debug=True)

