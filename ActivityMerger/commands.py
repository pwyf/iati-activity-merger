# from datetime import datetime, timedelta
import time
import shutil
import os
import click

from ActivityMerger import app


@app.cli.command()
@click.option("-a", "--all", "flush_all", is_flag=True)
def flush_data(flush_all):
    """
    Delete folders that are older than RETENTION_DAYS (config.py)
    (or all folders, using the --all switch)
    """

    input_path = app.config["UPLOAD_FOLDER"]
    output_path = app.config["OUTPUT_FOLDER"]
    retention_seconds = 86400 * app.config["RETENTION_DAYS"]

    for folder in os.listdir(input_path):
        try:
            if flush_all:
                shutil.rmtree(os.path.join(input_path, folder))
            else:
                if (
                    os.path.getmtime(os.path.join(input_path, folder))
                    < time.time() - retention_seconds
                ):
                    shutil.rmtree(os.path.join(input_path, folder))
        except OSError:
            print(f"Error removing folder: {os.path.join(input_path, folder)}")
            pass

    for filename in os.listdir(output_path):
        try:
            if flush_all:
                os.remove(os.path.join(output_path, filename))
            else:
                if (
                    os.path.getmtime(os.path.join(output_path, filename))
                    < time.time() - retention_seconds
                ):
                    os.remove(os.path.join(output_path, filename))
        except OSError:
            print(f"Error removing file: {os.path.join(output_path, filename)}")
            pass

