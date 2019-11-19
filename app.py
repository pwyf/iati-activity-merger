import os
from flask import Flask, request, redirect, url_for
from flask import send_from_directory, render_template
from werkzeug.utils import secure_filename
import merge

UPLOAD_FOLDER = './test-activity-files'
OUTPUT_FOLDER = './test-output-files'
OUTPUT_FILE = 'merged-activities.xml'
ALLOWED_EXTENSIONS = {'xml'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['OUTPUT_FILE'] = OUTPUT_FILE
app.secret_key = "secret key"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/merged')
def uploaded_file():
    return send_from_directory(app.config['OUTPUT_FOLDER'],
                               app.config['OUTPUT_FILE'])


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            print(file)
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        output = os.path.join(app.config['OUTPUT_FOLDER'],
                              app.config['OUTPUT_FILE'])
        outcome = merge.merger(app.config['UPLOAD_FOLDER'], output)
        if outcome:
            return redirect(url_for('uploaded_file'))
    return render_template('upload.html')


if __name__ == '__main__':
    app.run()
