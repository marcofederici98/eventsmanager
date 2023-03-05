from flask import Flask, render_template, render_template_string, request, send_file
import functions
import pandas as pd


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/events', methods=['GET', 'POST'])
def upload():
    if 'data_file' in request.files:
        global data
        data = request.files['data_file']
        if data.filename != '':  
            return functions.pipeline(data)
        else:
            return 'error, unvalid file type'

@app.route('/submit-form', methods=['POST'])
def submit_form():
    global checked_rows
    checked_rows = request.json
    return checked_rows

@app.route('/success')
def success():
    print('code:', checked_rows)
    code = pd.DataFrame(checked_rows).to_excel('Arrivati.xlsx')
    return send_file('Arrivati.xlsx')

    

if __name__ == '__main__':
    app.run(debug=True)

