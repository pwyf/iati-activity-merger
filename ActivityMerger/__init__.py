import os, uuid, shutil
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
    OUTPUT_FOLDER='output'
)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        outputFile = str(uuid.uuid4().hex) + '.xml'
        uploadFolder = os.path.join(app.config['UPLOAD_FOLDER'], 
                                    str(uuid.uuid4().hex))
        os.mkdir(uploadFolder)

        if 'files[]' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(uploadFolder,
                                       filename))

        outcome = merge.merger(uploadFolder, os.path.join(app.config['OUTPUT_FOLDER'], outputFile))
        if outcome:
            shutil.rmtree(uploadFolder)
            return redirect(url_for('download_and_remove', filename=outputFile))
    return render_template('upload.html')


@app.route('/download/<filename>')
def download_and_remove(filename):
    path = os.path.join(app.root_path, "..",
                        app.config['OUTPUT_FOLDER'], filename)

    def generate():
        with open(path) as merged:
            yield from merged

        os.remove(path)

    r = app.response_class(generate(), mimetype='Application/xml')
    r.headers.set('Content-Disposition', 'attachment', filename='merged.xml')
    return r
