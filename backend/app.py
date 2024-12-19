from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Model class for storing information
class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Paths
MODEL_PATH = 'model/resnet50_finetuned.h5'
UPLOAD_FOLDER = 'static/uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the fine-tuned ResNet50 model
model = load_model(MODEL_PATH)


### ROUTES FOR FRONTEND ###
# @app.route('/', methods=['GET'])
# def home():
#     info = Info.query.first()
#     return jsonify({
#         'info': 'Welcome to the COVID-19 X-ray Classifier App!',
#         'description': info.description if info else 'No description available.'
#     })

# About the model page
@app.route('/about', methods=['GET'])
def about():
    evaluation_chart_path = "static/evaluation_chart.png"
    return jsonify({
        'model': 'ResNet50 (Fine-tuned)',
        'dataset': 'COVID19-DATASET with Train, Test, and Validation splits',
        'metrics': {
            'accuracy': 0.95,
            'precision': 0.94,
            'recall': 0.96
        },
        'evaluation_chart': evaluation_chart_path
    })


# Future improvements page
@app.route('/future', methods=['GET'])
def future():
    return jsonify({
        'improvements': [
            "Expand dataset to include more diverse X-ray images.",
            "Add support for more lung conditions.",
            "Improve model generalizability through transfer learning.",
            "Enable real-time X-ray classification with mobile integration."
        ]
    })


# Contact us page
@app.route('/contact', methods=['GET'])
def contact():
    return jsonify({
        'email': 'abdelhadysayed_p@sci.asu.edu.eg',
        'github': 'https://github.com/abdelhadysayed/covid-classifier',
        'phone': '+1234567890'
    })


# Upload or capture image for prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    img_file = request.files['image']
    img_path = os.path.join(UPLOAD_FOLDER, img_file.filename)
    img_file.save(img_path)

    img = image.load_img(img_path, target_size=(224, 224))  # Match model input size
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    class_idx = np.argmax(prediction)
    class_name = "COVID-19" if class_idx == 0 else "Normal"

    return jsonify({
        'class': class_name,
        'message': f'The X-ray indicates {class_name}.',
        'uploaded_image': img_path
    })


# Serve evaluation chart for the "About the Model" page
@app.route('/evaluation_chart', methods=['GET'])
def evaluation_chart():
    chart_path = 'static/evaluation_chart.png'
    if os.path.exists(chart_path):
        return send_file(chart_path, mimetype='image/png')
    else:
        return jsonify({'error': 'Evaluation chart not found.'}), 404


@app.route('/update_info', methods=['POST'])
def update_info():
    description = request.json.get('description')
    if not description:
        return jsonify({'error': 'No description provided'}), 400

    info = Info.query.first()
    if info:
        info.description = description
    else:
        info = Info(description=description)
        db.session.add(info)
    db.session.commit()

    return jsonify({'message': 'Info updated successfully'})



if __name__ == '__main__':
    app.run(debug=True)
