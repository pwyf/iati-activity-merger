from lxml import etree
from datetime import datetime
import os, glob


def merger(activityFolder, outputFile):
    activityFiles = glob.glob(os.path.join(activityFolder, '*.xml'))
    totalActivities = 0
    with open(outputFile, "wb") as f, etree.xmlfile(f) as xf:
        attribs = {"generated-datetime": str(datetime.now().isoformat()),
                   "version": "2.03"}
        with xf.element("iati-activities", attribs):
            xf.write("\n  ")
            for file in activityFiles:
                root = etree.parse(file)
                activities = root.iterfind(".//iati-activity")
                for activity in activities:
                    totalActivities += 1
                    xf.write(activity)
    return totalActivities
