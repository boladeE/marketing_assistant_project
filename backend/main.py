from flask import Flask, request, jsonify, render_template, redirect, url_for
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from copywriter import generate_marketing_copy
from brand_style import BrandStyleManager
from config import settings
import os
import json
import datetime

app = Flask(__name__)

# Initialize brand style manager
brand_style_manager = BrandStyleManager()
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
campaign_prompt = []

def load_campaigns():
    campaigns_file = os.path.join(data_dir, "past_campaigns", "campaigns.json")
    if os.path.exists(campaigns_file):
        with open(campaigns_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            campaigns = data.get("campaigns", [])
            return campaigns
    return []

def save_campaigns(campaigns):
    campaigns_file = os.path.join(data_dir, "past_campaigns", "campaigns.json")
    os.makedirs(os.path.dirname(campaigns_file), exist_ok=True)
    with open(campaigns_file, 'w', encoding='utf-8') as f:
        json.dump({"campaigns": campaigns}, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def root():
    global prompt
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        campaign_prompt.pop()
        campaign_prompt.append(prompt)
        marketing_copy = generate_marketing_copy(prompt)
        return render_template('index.html', generated_copy=marketing_copy)
    return render_template('index.html')

@app.route('/campaigns')
def view_campaigns():
    campaigns = load_campaigns()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/save-edit', methods=['POST'])
def save_edit():
    edited_copy = request.form.get('editedCopy')
    global campaign_prompt
    prompt = campaign_prompt[-1]
    campaigns = load_campaigns()
    new_campaign = {
        "prompt": prompt,
        "content": edited_copy,
        "timestamp": datetime.datetime.now().isoformat()
    }
    campaigns.append(new_campaign)
    save_campaigns(campaigns)
    
    return render_template('index.html', generated_copy="Campaign saved successfully")

@app.route('/update-campaign', methods=['POST'])
def update_campaign():
    index = int(request.form.get('index'))
    edited_copy = request.form.get('editedCopy')
    
    campaigns = load_campaigns()
    if 0 <= index < len(campaigns):
        campaigns[index]['content'] = edited_copy
        campaigns[index]['timestamp'] = datetime.datetime.now().isoformat()
        save_campaigns(campaigns)
    
    return redirect(url_for('view_campaigns'))

@app.route('/delete-campaign', methods=['POST'])
def delete_campaign():
    index = int(request.form.get('index'))
    
    campaigns = load_campaigns()
    if 0 <= index < len(campaigns):
        campaigns.pop(index)
        save_campaigns(campaigns)
    
    return redirect(url_for('view_campaigns'))

if __name__ == "__main__":
    app.run(host='localhost', port=8000, debug=True)