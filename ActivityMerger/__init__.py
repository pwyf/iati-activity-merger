import os, uuid, shutil
from flask import Flask, request, redirect, url_for, abort
from flask import send_from_directory, render_template
from flask_assets import Environment as FlaskAssets, Bundle
from werkzeug.utils import secure_filename
from ActivityMerger import merge


ALLOWED_EXTENSIONS = {'xml'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    UPLOAD_FOLDER='/var/www/input',
    OUTPUT_FOLDER='/var/www/output'
)

assets = FlaskAssets(app)
assets.register('js_base', Bundle(
    os.path.join('js', 'jquery-1.12.4.js'),
    os.path.join('js', 'bootstrap-3.3.7.js'),
    filters='jsmin',
    output=os.path.join('gen', 'js.%(version)s.min.js'))
)
assets.register('js_activity', Bundle(
    os.path.join('js', 'activity.js'),
    filters='jsmin',
    output=os.path.join('gen', 'activity.%(version)s.min.js'))
)
assets.register('css_base', Bundle(
    os.path.join('css', 'bootstrap.css'),
    os.path.join('css', 'font-awesome.css'),
    os.path.join('css', 'app.css'),
    filters='cssmin',
    output=os.path.join('gen', 'css.%(version)s.min.css'))
)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        outputFile = str(uuid.uuid4().hex) + '.xml'
        outputFullpath = os.path.join(app.config['OUTPUT_FOLDER'], outputFile)
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

        outcome = merge.merger(uploadFolder, outputFullpath)
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
