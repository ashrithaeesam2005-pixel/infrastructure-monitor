from flask import Flask, render_template
from flask_cors import CORS

from routes.predict_route import predict_bp
from routes.complaint_route import complaint_bp
from routes.report_route import report_bp

from database.db import init_db

app = Flask(__name__)

CORS(app)

init_db()

app.register_blueprint(predict_bp)
app.register_blueprint(complaint_bp)
app.register_blueprint(report_bp)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)