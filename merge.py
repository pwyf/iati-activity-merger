from lxml import etree
import glob


fname = "test-output-files/merged-activities.xml"
activityFiles = glob.glob('test-activity-files/*.xml')

with open(fname, "wb") as f, etree.xmlfile(f) as xf:
    with xf.element("iati-activities"):
        xf.write("\n  ")
        for file in activityFiles:
            root = etree.parse(file)
            activities = root.iterfind(".//iati-activity")
            for activity in activities:
                xf.write(activity)
