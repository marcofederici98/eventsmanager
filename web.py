from flask import Flask, render_template, request, send_file
import functions
import pandas as pd

app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/events', methods=['GET', 'POST'])
def upload():
    if 'data_file' in request.files:
        global df
        data = request.files['data_file']
        if data.filename != '':
            df = functions.pipeline(data)
            return functions.pipeline2(df)
        else:
            return 'error, unvalid file type'
    return "Errore, controlla il tipo di file caricato"

@app.route('/submit-form', methods=['POST'])
def submit_form():
    global checked_rows
    checked_rows = request.json
    return checked_rows

@app.route('/success')
def success():
    print('code:', checked_rows)
    print(df)
    code = pd.DataFrame(functions.colonna_arrivi(df, checked_rows)).to_excel('Arrivati.xlsx')
    #code = pd.DataFrame(checked_rows).to_excel('Arrivati.xlsx')
    return send_file('Arrivati.xlsx')

    

if __name__ == '__main__':
    app.run(debug=True)

