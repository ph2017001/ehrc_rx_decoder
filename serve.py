import os
from flask import Flask, jsonify, request, render_template
import pandas as pd


from flask_cors import CORS
import time
from multiprocessing import Process

from EHRC_Rx_Processor import *

ehrc_data = pd.read_excel("EHRC_Master.xlsx", sheet_name="ehrc_data")

BASE_URL = os.path.abspath(os.path.dirname(__file__))
APP_FOLDER = os.path.join(BASE_URL,"auto-complete")
# DIST_FOLDER = os.path.join(APP_FOLDER,"dist")
# UI_FOLDER = os.path.join(DIST_FOLDER,"auto-complete/")

print(APP_FOLDER)
app = Flask(__name__)
# app = Flask(__name__,static_folder=APP_FOLDER, template_folder=APP_FOLDER,static_url_path='/static')
CORS(app)


print("\nModel init Complete...\n")
def get_args(req):
    args = {}
    if request.method == 'POST':
        args = request.json
    elif request.method == "GET":
        args = request.args
    return args


@app.route('/getMedicines',methods=['GET'])
def getMedicines():
    medicines = ehrc_data['MOLECULE_NAME'].to_list()
    return jsonify({'results':medicines})


@app.route('/getDetails',methods=['POST'])
def getDetails():
    req_json = get_args(request)
    data = req_json['presc_text_list']
    suggestions_accepted = req_json['suggestions_accepted']
    print(suggestions_accepted)
    result = []
    for text in data:
    #for i in splitPrescriptionLines(data):
        print("**"*10)
        print(text)
        result.append(startExtraction(text,separator_list,dosage_suffix,ehrc_data,suggestions_accepted))

    return jsonify(result)


@app.route('/editor')
def getEditor():
    return render_template('editor.html')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')  # Catch All urls, enabling copy-paste url
def home(path):
    print("inside home",path)
    return render_template('editor.html')







def main(host="0.0.0.0", port=9078):
    app.run(host=host, port=port, debug=True,threaded=False)


if __name__ == "__main__":
    main()
