# IATI Activity Merger

This tool will take multiple IATI activity files and merge them into a single activity file.
No validation is performed, nor is the reporting-org checked at present.

## Deployment

Probably a reverse proxy of some sort pointing at flask

```bash
export FLASK_APP=ActivityMerger
flask run -h 0.0.0.0
```