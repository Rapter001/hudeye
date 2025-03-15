import os
from flask import jsonify
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
from email.mime.multipart import MIMEMultipart
from werkzeug.exceptions import RequestEntityTooLarge
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, make_response

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "svg", "gif", "mp4", "webp", "ogg", "webm", "bmp"}
app.secret_key = "#U*P5g@x1SwvqP"

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

@app.errorhandler(RequestEntityTooLarge)
def handle_file_size_error(error):
    flash("File is too large. Maximum size allowed is 10 MB.", "error")
    return redirect(url_for("upload"))

@app.route("/")
def home():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", files=files)

@app.route("/get_files")
def get_files():
    try:
        files = [filename for filename in os.listdir("uploads") if os.path.isfile(os.path.join("uploads", filename))]
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                try:
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    flash("File uploaded successfully!", "success")
                except Exception as e:
                    flash("Error uploading file. Please try again.", "error")
            else:
                flash("File type not allowed. Please upload a file of allowed type.", "error")
        else:
            flash("No file selected. Please choose a file to upload.", "error")
    return render_template("upload.html")

@app.route("/view")
def view_files():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("view.html", files=files, upload_folder="uploads")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    response = make_response(send_from_directory(app.config["UPLOAD_FOLDER"], filename))
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    response.headers["CDN-Cache-Control"] = "public, max-age=31536000"
    response.headers["Cloudflare-CDN-Cache-Control"] = "public, max-age=31536000"
    return response

@app.route("/view/<filename>")
def view_file(filename):
    response = make_response(send_from_directory(app.config["UPLOAD_FOLDER"], filename))
    response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
    response.headers["CDN-Cache-Control"] = "public, max-age=31536000"
    response.headers["Cloudflare-CDN-Cache-Control"] = "public, max-age=31536000"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)