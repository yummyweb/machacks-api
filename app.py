from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/processing", methods=["POST"])
def processing():
    app.config['UPLOAD_FOLDER'] = "~/Dev/machacks-api/uploads"
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return { "nice": "pig" }


if __name__ == "__main__":
    app.run(debug=True)
