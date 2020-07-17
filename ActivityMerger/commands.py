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

    path = app.config["UPLOAD_FOLDER"]
    retention_seconds = 86400 * app.config["RETENTION_DAYS"]

    for folder in os.listdir(path):
        if flush_all:
            shutil.rmtree(os.path.join(path, folder))
        else:
            if (
                os.path.getmtime(os.path.join(path, folder))
                < time.time() - retention_seconds
            ):
                shutil.rmtree(os.path.join(path, folder))

