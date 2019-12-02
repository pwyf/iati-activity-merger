import os, uuid, shutil
from datetime import datetime
from flask import Flask, request, abort
from flask import render_template, redirect, url_for
from werkzeug.utils import secure_filename
from ActivityMerger import merge, app

ALLOWED_EXTENSIONS = {'xml'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        outputFile = str(uuid.uuid4().hex) + '.xml'
        outputFullpath = os.path.join(app.config['OUTPUT_FOLDER'], outputFile)
        uploadFolder = os.path.join(app.config['UPLOAD_FOLDER'], 
                                    str(uuid.uuid4().hex))
        os.mkdir(uploadFolder)

        if 'files[]' not in request.files:
            render_template('upload.html', error=False)
        files = request.files.getlist('files[]')
        for file in files:
            if file.filename == '':
                return render_template('upload.html', error=False)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(uploadFolder,
                                       filename))

        totalActivities = merge.merger(uploadFolder, outputFullpath)
        if totalActivities > 0:
            shutil.rmtree(uploadFolder)
            return redirect(url_for('download_file', filename=outputFile, noFiles=len(files)))
        else:
            return render_template('upload.html', error=True)


    return render_template('upload.html', error=False)

@app.route('/<noFiles>-<filename>', methods=['GET'])
def download_file(filename, noFiles):
    mergeTime = datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
    return render_template('download.html', filename=filename, timestamp=mergeTime, noFiles=noFiles)

@app.route('/download/<filename>')
def download_and_remove(filename):
    path = os.path.join(app.root_path, "..",
                        app.config['OUTPUT_FOLDER'], filename)

    def generate():
        with open(path) as merged:
            yield from merged

    r = app.response_class(generate(), mimetype='Application/xml')
    r.headers.set('Content-Disposition', 'attachment', filename='merged.xml')
    return r