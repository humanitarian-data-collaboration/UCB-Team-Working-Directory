from flask import Flask, redirect, request, render_template, url_for, send_from_directory, make_response
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import os
import hashlib
import pandas as pd
from werkzeug.utils import secure_filename
import pickle


#This is not but-free, still have some problems...

UPLOAD_FOLDER = '\datasets'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        file.save(os.getcwd())
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            df = pd.read_csv(file)
            # resp = make_response(df.to_csv())
            # resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
            # resp.headers["Content-Type"] = "text/csv"
            # return resp  
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File (only CSV files accepted)</h1>
    <form action={{url_for('tag', dataset='df')}} method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    ''' 

@app.route('/tag/<dataset>', methods=['POST'])
def tag(dataset):
	#getting our trained model	
	model = pickle.load(open("model.pkl", "rb"))   	
	input_dataset = request.get_json()
	tags = model.predict(input_dataset).to_list()
	#Add one row to the dataset
	for i in range(len(tags)):
		input_dataset.loc1[1: i] = tags[i]
	response = {}
	response['tags'] = tags
	#returning the response object as json
    return flask.jsonify(response)

if __name__ == '__main__':
     app.run(debug=True)

     




