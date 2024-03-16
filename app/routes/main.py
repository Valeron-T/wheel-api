from flask import Blueprint, request, jsonify
from app import mongo
from app.task import process_pdf

bp = Blueprint('main', __name__)


@bp.route('/')
def home_page():
    online_users = mongo.db.users.find({'name': "John Doe"})
    return jsonify({"message": f'{online_users.next()} is online'})


@bp.route('/upload', methods=['POST'])
def upload_pdf():
    """
    Accepts and processes a pdf asynchronously with celery.
    :return: JSON response containing task ID
    """
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file part'})

    pdf = request.files['pdf']

    # Trigger Celery task
    task = process_pdf.delay(pdf.read())
    print(f"Task accepted with id: {task}")
    return jsonify({'task_id': task.id}), 202  # Accepted
