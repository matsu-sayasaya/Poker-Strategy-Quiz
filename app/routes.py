import os
from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
from app.utils import parse_csv, validate_csv
from app.forms import UploadForm
import logging
import io

logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    questions = []
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            try:
                # ファイルをメモリ上で読み込む
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                df = pd.read_csv(stream, header=None)
                logger.debug(f"CSV file read: {df}")
                if validate_csv(df):
                    questions = parse_csv(df)
                    if questions:
                        logger.debug(f"Questions parsed successfully: {questions}")
                    else:
                        logger.warning("No valid questions found in CSV")
                        return render_template('index.html', form=form, error="No valid questions found in CSV")
                else:
                    logger.warning("Invalid CSV format")
                    return render_template('index.html', form=form, error="Invalid CSV format")
            except Exception as e:
                logger.error(f"Error processing CSV: {str(e)}", exc_info=True)
                return render_template('index.html', form=form, error=f"Error processing CSV: {str(e)}")
        else:
            logger.warning("Invalid file type")
            return render_template('index.html', form=form, error="Invalid file type")
    return render_template('index.html', form=form, questions=questions)

@bp.route('/check', methods=['POST'])
def check():
    data = request.json
    selected_size = data.get('selected_size')
    selected_frequency = data.get('selected_frequency')
    correct_size = data.get('correct_size')
    correct_frequency = data.get('correct_frequency')  # この行を修正

    # 値が None の場合のエラーハンドリングを追加
    if selected_size is None or selected_frequency is None or correct_size is None or correct_frequency is None:
        return jsonify({
            "error": "Invalid input data"
        }), 400

    # 判定ロジックの実装
    size_result = 'Correct' if selected_size == correct_size else 'Wrong'
    
    if selected_frequency == correct_frequency:
        frequency_result = 'Correct'
    elif abs(selected_frequency - correct_frequency) <= 5:
        frequency_result = 'Close'
    else:
        frequency_result = 'Wrong'

    return jsonify({
        "size_result": size_result,
        "frequency_result": frequency_result
    })

