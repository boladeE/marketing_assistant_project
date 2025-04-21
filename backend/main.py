from flask import Flask, request, jsonify, render_template, redirect, url_for
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from copywriter import generate_marketing_copy
from brand_style import BrandStyleManager
from config import settings
from database import Database
import os
import json
import datetime

app = Flask(__name__)

# Initialize brand style manager and database
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
campaign_prompt = []
db = Database()

@app.route('/', methods=['GET', 'POST'])
def root():
    global prompt
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        campaign_prompt.append(prompt)
        marketing_copy = generate_marketing_copy(prompt)
        return render_template('index.html', generated_copy=marketing_copy)
    return render_template('index.html')

@app.route('/campaigns')
def view_campaigns():
    campaigns = db.get_all_campaigns()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/save-edit', methods=['POST'])
def save_edit():
    edited_copy = request.form.get('editedCopy')
    global campaign_prompt
    prompt = campaign_prompt[-1]
    db.add_campaign(prompt, edited_copy)
    return render_template('index.html', generated_copy="Campaign saved successfully")

@app.route('/update-campaign', methods=['POST'])
def update_campaign():
    index = int(request.form.get('index'))
    edited_copy = request.form.get('editedCopy')
    db.update_campaign(index, edited_copy)
    return redirect(url_for('view_campaigns'))

@app.route('/delete-campaign', methods=['POST'])
def delete_campaign():
    index = int(request.form.get('index'))
    db.delete_campaign(index)
    return redirect(url_for('view_campaigns'))

if __name__ == '__main__':
    app.run(debug=True)