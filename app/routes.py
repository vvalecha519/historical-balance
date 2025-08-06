import os

from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory, send_file
from werkzeug.utils import secure_filename
from app import app
from libs.Report import Report
from datetime import datetime


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
            
            # Process file in memory instead of saving to disk
            report = Report(uploaded_file)
            output_data = report.generate_token_balance_report(block_no)
            response = report.adapt_to_pd_and_output(output_data)
            
            return response

    return render_template('single-block.html')


@app.route('/block-range', methods=['GET', 'POST'])
def block_range():

    if request.method == 'POST':
        start_block = request.form['start_block']
        end_block = request.form['end_block']
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in UPLOAD_EXTENSIONS:
                abort(400)
            
            # Process file in memory instead of saving to disk
            report = Report(uploaded_file)
            output_data = report.generate_token_balance_report_in_block_range(start_block, end_block)
            response = report.adapt_to_pd_and_output(output_data)
            
            return response

    return render_template('block-range.html')


@app.route('/date-range', methods=['GET', 'POST'])
def date_range():

    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in UPLOAD_EXTENSIONS:
                abort(400)
            
            # Process file in memory instead of saving to disk
            report = Report(uploaded_file)
            output_data = report.generate_token_balance_report_in_date_range(start_date, end_date)
            response = report.adapt_to_pd_and_output(output_data)
            
            return response

    return render_template('date-range.html', as_attachment=True)
