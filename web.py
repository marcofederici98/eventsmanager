from flask import Flask, render_template, request, send_file
import functions
import pandas as pd

app = Flask(__name__, template_folder="templates")


@app.route('/', methods=['GET'])
def index():
    global df
    df = None
    return render_template('index.html')


@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/events', methods=['GET', 'POST'])
def upload():
    global df
    if 'data_file' in request.files:
        data = request.files['data_file']
        if data.filename != '':
            df = functions.pipeline(data)
            return functions.pipeline2(df)
        else:
            return 'error, unvalid file type'
    return "Errore, controlla il tipo di file caricato"

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    return render_template('events.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    global checked_rows
    checked_rows = request.json
    return checked_rows

@app.route('/success')
def success():
    print('code:', checked_rows)
    global df
    if df is not None :
        code = pd.DataFrame(functions.colonna_arrivi(df, checked_rows)).to_excel('Arrivati.xlsx')
    else:
        df = functions.file_to_data('persone_famose.xlsx')
        code = pd.DataFrame(functions.colonna_arrivi(df, checked_rows)).to_excel('Arrivati.xlsx')
    #code = pd.DataFrame(checked_rows).to_excel('Arrivati.xlsx')
    return send_file('Arrivati.xlsx')

    

if __name__ == '__main__':
    app.run(debug=True)

