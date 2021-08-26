from flask import Flask, redirect, url_for, request
import os
from os.path import dirname
import sys
from src.preprocess.prepare_free_input import prepare_featured_input

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return '<h1> </h1>'

@app.route('/generate', methods=['POST'])
def generate():
    materials = request.form['materi']
    doGenerate(materials)

def doGenerate(materials):
    print(materials)
    print("preparing feature extraction .....")
    prepare_featured_input(materials, output_file_name="free_input.txt", manual_ne_postag=False, lower=False, seed=42)
    print("prepared data")
    os.system(
        f'onmt_translate -model models/modelnya.pt \
            -src free_input.txt \
            -output free_input_pred.txt -replace_unk \
            -beam_size 2 \
            -max_length 22'
    )
    with open("free_input_pred.txt", 'r') as f_in:
        predictions = f_in.readlines()
    return predictions

if __name__ == '__main__':
    app.run(debug=True)
