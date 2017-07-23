from flask import Flask, render_template, flash
from flask_wtf import Form
from flask_wtf.file import FileField
from tools import s3_upload, s3_get_bucket_contents, delete_photo, download_photo, classify_photo_rekognition
import time

app = Flask(__name__)
app.config.from_object('config')


class UploadForm(Form):
    example = FileField('Example File')


@app.route('/', methods=['POST', 'GET'])
def upload_page():

		labels = []

		current_photos = s3_get_bucket_contents()
		form = UploadForm()
		if form.validate_on_submit():
				if len(current_photos) > 0:
						for photo in current_photos:
								delete_photo(photo)
				output = s3_upload(form.example)
				# flash('{src} uploaded to S3 as {dst}'.format(src=form.example.data.filename, dst=output))
				flash('attempting to classify your image: {dst}'.format(dst=output))

				# download_photo(output)

				# path_to_photo_directory = './images/'
				labels = classify_photo_rekognition(output)


		return render_template('upload.html', form=form, labels=labels)

@app.route('/bucketContents', methods=['POST', 'GET'])
def contents_page():
		photos = s3_get_bucket_contents()
		return render_template('contents.html', photos=photos)

if __name__ == '__main__':
    app.run()
