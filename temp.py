from flask import Flask, render_template, request, send_file, jsonify
import os
from PIL import Image

app = Flask(__name__)

# Create a directory for uploaded images if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def generate_image_html(image_filename):
    return f'''
    <h1>Uploaded Image</h1>
    <img src="/show_image/{image_filename}" alt="Uploaded Image">
    '''





@app.route('/')
def index():
    return render_template('temp.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400  # Bad Request

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No image selected'}), 400  # Bad Request

    # Save the uploaded image
    image.save(os.path.join(UPLOAD_FOLDER, image.filename))

    # Generate HTML to display the uploaded image
    image_html = generate_image_html(image.filename)

    return image_html


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/show_image/<filename>')
def show_image(filename):
    # Construct the path to the uploaded image
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    # Return the image file
    return send_file(image_path, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
