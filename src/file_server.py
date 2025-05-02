# filepath: c:\Users\elorente\Documents\CodeApi\PiMediaManager\src\file_server.py
from flask import Flask, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "media_storage")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"
        file = request.files["file"]
        if file.filename == "":
            return "No selected file"
        if file:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            return f"Archivo {file.filename} subido exitosamente"
    return '''
    <!doctype html>
    <title>Subir Archivo</title>
    <h1>Subir Archivo</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Subir>
    </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)