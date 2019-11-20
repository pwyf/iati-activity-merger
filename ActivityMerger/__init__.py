import os
from flask import Flask, request, redirect, url_for, abort
from flask import send_from_directory, render_template
from werkzeug.utils import secure_filename
from ActivityMerger import merge

ALLOWED_EXTENSIONS = {'xml'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    UPLOAD_FOLDER='input',
    OUTPUT_FOLDER='output',
    OUTPUT_FILE='merged.xml',
)


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
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                       filename))
        output = os.path.join(app.config['OUTPUT_FOLDER'],
                              app.config['OUTPUT_FILE'])
        outcome = merge.merger(app.config['UPLOAD_FOLDER'], output)
        if outcome:
            return redirect(url_for('download_and_remove'))
    return render_template('upload.html')


@app.route('/download')
def download_and_remove():
    path = os.path.join(app.root_path, "..",
                        app.config['OUTPUT_FOLDER'], app.config['OUTPUT_FILE'])

    def generate():
        with open(path) as merged:
            yield from merged

        os.remove(path)

    r = app.response_class(generate(), mimetype='Application/xml')
    r.headers.set('Content-Disposition', 'attachment', filename='merged.xml')
    return r
