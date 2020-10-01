#!/bin/sh

# AWS CLI MUST be installed to run this script
# For more info, please visit:
#    https://linuxhint.com/install_aws_cli_ubuntu/

# To run this file:
# $ sh gdelt-to-s3.sh <fileformat>
#
# Example: To process files from September 
#    $ sh gdelt-to-s3.sh 20200901 20200930
#
# export EC2_ACCESS_KEY=<Access Key>
# export EC2_SECRET_KEY=<Secret Key>

THIS_FILE=${1}  # Save first parameter
END_FILE=${2}  # Save second parameter
MY_BUCKET='gelt-folder/gdelt-data/'

# Function to download a file, transfer to S3, then delete

transfer_data(){
  curl -O http://data.gdeltproject.org/events/$THIS_FILE.export.CSV.zip
  unzip $THIS_FILE.export.CSV.zip
  echo 'Uploading '${THIS_FILE}.export.CSV' to s3...'
  # Copy file to S3
  aws s3 cp $THIS_FILE.export.CSV s3://$MY_BUCKET
  echo 'Uploaded to s3...'
  echo 'Deleting .zip file...'
  rm -f $THIS_FILE.export.CSV.zip
  echo 'Deleted .zip file...'
  echo 'Deleting .csv file...'
  rm -f $THIS_FILE.export.CSV
  echo 'Deleted .csv file...'
  echo 'Done with '$THIS_FILE''
}

# Loop over the date range provided
for THIS_FILE in `seq $THIS_FILE $END_FILE`
do
  transfer_data $THIS_FILE
done

# Print out number of objects in bucket as well as bucket size
aws s3 ls --summarize --human-readable --recursive s3://gelt-folder | tail -n 2 | awk -F" " '{print $1 $2 $3 $4}'
