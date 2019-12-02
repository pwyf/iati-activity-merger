# IATI Activity Merger

This tool will take multiple IATI activity files and merge them into a single activity file.

Notes:
- There is no explicit ordering to activities in the merged file
- No validation is performed
- The reporting-org is not checked for consistently and so currently it is possible to merge files from different publishers.

This tool is in `BETA` therefore it is worth uploading the file to [IATI CoVE](https://iati.cove.opendataservices.coop/) to ensure your input and/or output is valid.

## Deployment

Probably a reverse proxy of some sort pointing at flask

```bash
export FLASK_APP=ActivityMerger
flask run -h 0.0.0.0
```
