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


def process(pandas_dataset, dataframe):
    if (not pandas_dataset.empty):
            dataset_df = pandas_dataset
            headers = list(dataset_df.columns.values)
            headers = clean_cols(headers)
            tags = list(dataset_df.iloc[0,:])
            for i in range(len(headers)):
                try:
                    splitted = re.split('[(^\s+)+#]', tags[i])
                    splitted = list(filter(None, splitted))
                    hashtag = splitted[0]
                    attributes = splitted[1:]
                    dic = {'Header': headers[i], 'Tag': hashtag, 'Attributes': attributes, 
                           'Data': list(dataset_df.iloc[1:, i]), 
                           'Relative Column Position': (i+1) / len(dataset_df.columns), 
                           'Dataset_name': os.path.basename(path), 
                           'Organization': organization,
                           'Index': index}
                    dataframe.loc[len(dataframe)] = dic
                except:
                    print("Error: different number of headers and tags")
            count += 1
        os.remove(path)
        print("File Removed!")
        return


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
            input_dataset = pd.read_csv(file)
                # process the untagged dataset
            
            process(input_dataset, )
            model = pickle.load(open("model.pkl", "rb"))
            output_dataset = model.predict(input_dataset.values.to_list())


            resp = make_response(output_dataset.to_csv())
            resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
            resp.headers["Content-Type"] = "text/csv"
            return resp  
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File (only CSV files accepted)</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    ''' 

 # action={{url_for('tag', dataset='df')}}   

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

     




