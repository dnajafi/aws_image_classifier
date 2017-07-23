from uuid import uuid4
import boto
import os.path
from flask import current_app as app
from werkzeug.utils import secure_filename
import boto3

def s3_upload(source_file, upload_dir=None, acl='public-read'):

    if upload_dir is None:
        upload_dir = app.config["S3_UPLOAD_DIRECTORY"]

    source_filename = secure_filename(source_file.data.filename)
    source_extension = os.path.splitext(source_filename)[1]

    destination_filename = source_filename

    # Connect to S3 and upload file.
    conn = boto.connect_s3(app.config["S3_KEY"], app.config["S3_SECRET"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    sml = b.new_key("/".join([upload_dir, destination_filename]))
    sml.set_contents_from_string(source_file.data.read())
    sml.set_acl(acl)

    return destination_filename


def download_photo(photo):
    # Connect to S3 and upload file.
    conn = boto.connect_s3(app.config["S3_KEY"], app.config["S3_SECRET"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    key = b.get_key(photo)
    key.get_contents_to_filename('./images/' + photo)



def s3_get_bucket_contents():
    # Connect to S3 and upload file.
    conn = boto.connect_s3(app.config["S3_KEY"], app.config["S3_SECRET"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    photos = []

    for key in b:
        photos.append(key.name)
        print "{name}\t{size}\t{modified}".format(name = key.name, size = key.size, modified = key.last_modified)

    return photos

def delete_photo(photo):
    # Connect to S3 and upload file.
    conn = boto.connect_s3(app.config["S3_KEY"], app.config["S3_SECRET"])
    b = conn.get_bucket(app.config["S3_BUCKET"])

    b.delete_key(photo)


def classify_photo_rekognition(photo):

    client = boto3.client('rekognition', aws_access_key_id=app.config["S3_KEY"], aws_secret_access_key=app.config["S3_SECRET"])
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': app.config["S3_BUCKET"],
                'Name': photo,
            }
        },
        MaxLabels=123
    )

    potentialLabels = response["Labels"]


    highestConfidence = 0
    labels = []

    for label in potentialLabels:
        if label["Confidence"] >= highestConfidence:
            highestConfidence = label["Confidence"]
            labels.append(label["Name"])


    return labels






















