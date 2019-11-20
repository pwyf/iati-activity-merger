# IATI Activity Merger

This tool will take multiple IATI activity files and merge them into a single activity file.

N.B. No validation is performed, nor is the `reporting-org` checked at present.

This tool is in `BETA` therefore it is worth uploading the file to [IATI CoVE](https://iati.cove.opendataservices.coop/) to ensure your input and/or output is valid.

## Deployment

Probably a reverse proxy of some sort pointing at flask

```bash
export FLASK_APP=ActivityMerger
flask run -h 0.0.0.0
```