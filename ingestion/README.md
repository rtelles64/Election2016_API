# Ingestion

`gdelt-to-s3.sh` is a shell script to collect the raw data files from the GDELT Project and ingest them into S3.

## Run this file:

To run the shell script, run this command:

```
$ sh gdelt-to-s3.sh <fileformat>
```

For example: To process files from September 

```
$ sh gdelt-to-s3.sh 20200901 20200930
```
