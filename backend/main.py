from flask import Flask, request, jsonify, render_template
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from copywriter import generate_marketing_copy
from brand_style import BrandStyleManager
from config import settings

app = Flask(__name__)

# Initialize brand style manager

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        marketing_copy = generate_marketing_copy(prompt)
        return render_template('index.html', generated_copy=marketing_copy)
    # generated_copy = generate_marketing_copy("Generate a marketing campaign for our new comers")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='localhost', port=8000, debug=True)