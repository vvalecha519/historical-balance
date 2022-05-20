import os

from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory
from werkzeug.utils import secure_filename
from app import app
from libs.Report import Report


UPLOAD_EXTENSIONS = ['.xls', '.xlsx']
UPLOAD_PATH = 'uploads'

GENERATED_REPORT_PATH = 'generated_reports'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/single-block', methods=['GET', 'POST'])
def single_block():
    
    if request.method == 'POST':
        block_no = request.form['block_no']
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in UPLOAD_EXTENSIONS:
                abort(400)
            filepath = os.path.join(UPLOAD_PATH, filename)
            print(filepath)
            uploaded_file.save(filepath)

            report = Report(filepath)
            output_data = report.generate_token_balance_report(block_no)
            output_filename = report.output_report(output_data)

            return send_from_directory(GENERATED_REPORT_PATH, output_filename)

    return render_template('single-block.html')


@app.route('/block-range', methods=['GET', 'POST'])
def block_range():
    return render_template('single-block.html')


@app.route('/date-range', methods=['GET', 'POST'])
def date_range():
    return render_template('single-block.html')


@app.route('/generate-report', methods=['GET', 'POST'])
def generate_report():

    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in UPLOAD_EXTENSIONS:
                abort(400)
            filepath = os.path.join(UPLOAD_PATH, filename)
            uploaded_file.save(filepath)


            return send_from_directory(GENERATED_REPORT_PATH, output_filename)

    return render_template('generate-report.html')