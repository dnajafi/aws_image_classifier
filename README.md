Image Classifier App Built in Flask to familiarize myself with AWS Rekognition

The app uses AWS S3 to store files in the cloud and AWS Rekognition to classify objects in the image that is uploaded.

Note that I have not included config.py in the github link since it includes some of my AWS credentials.
If interested in using this code be sure to include a config.py file in the main parent directory with the
following credentials:

S3_LOCATION = 'location of your S3 bucket' # looks like https://s3-us-west-2.amazonaws.com
S3_KEY = 'your S3 key for one of your AWS users' # see IAM tutorials on AWS
S3_SECRET = 'your S3 key for one of your AWS users' # see IAM tutorials on AWS
S3_UPLOAD_DIRECTORY = ''
S3_BUCKET = '' # name of your S3 bucket



I also used a virtualenv environment when using this on my machine.

Note: be sure to run 'pip install -r requirements.txt' to include all required dependencies
