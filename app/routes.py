import io
import pandas as pd

@bp.route('/', methods=['GET', 'POST'])
def index():
    form = UploadForm()
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
                        return render_template('index.html', form=form, questions=questions)
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
    return render_template('index.html', form=form)

