import pandas as pd
from duckduckgo_search import ddg_images

def file_ext(filename):
    return filename.split('/')[-1].split('.')[-1]

def csv_data(file_path):
    delimiters = [',', ';']
    encoders = ['utf-8', 'latin-1']
    for d in delimiters:
        try:
            df = pd.read_csv(file_path, encoding = encoders[0], delimiter = d)
        except:
            df = pd.read_csv(file_path, encoding = encoders[1], delimiter = d)
        if df.shape[1]>1:
            return df

def add_ghost(data):
    columns = list(data.columns)
    name_cols = columns [:2]
    others = columns[2:]
    data['ghost'] = data[columns[0]] + ' ' + data[columns[1]]
    data_cols = ['ghost'] + name_cols + others
    return data [data_cols]
    

def file_to_data(file_path):
    if file_path == 'demo.xlsx':
        ext = file_ext(file_path)
    else:
        ext = file_ext(file_path.filename)
    data = None
    if ext in ['csv', 'xlsx', 'xlx']:
        if ext == 'csv':
            data = csv_data(file_path)
        else:
            data = pd.read_excel(file_path)
            if file_path == 'demo.xlsx':
                data = add_ghost(data)
    else:
        return 'File non valido'
    return data

def search_data(data):
    columns = list(data.columns)
    name_cols = columns[0:2]
    others = columns[2:]
    df = data[name_cols]
    images = []
    buttons = []
    ht = 200
    df['ghost'] = data[name_cols[0]] + ' ' + data[name_cols[1]]
    df['query'] = data[name_cols[0]] + ' ' + data[name_cols[1]] + ' volto'
    for query in df['query']:
        search = ddg_images(query, max_results=1)
        url = search[0]['image']
        idb = 'button_' + (query[:-6].replace(' ', '_'))
        button=f'<a href="{url}" target="blank"> <span id="{idb}">Visualizza intera</span> </a>'
        img_html='<img src="'+url+f'" height="{ht}">'
        images.append(img_html)
        buttons.append(button)
    df['img'] = images
    df['buttons'] = buttons
    df['Pic']=df['img']+'<br>'+df['buttons']
    df['enc'] = df[name_cols[0]] + '_' + df[name_cols[1]]
    for i in others:
        df[i] = data[i]
    checkboxes=[]
    for i in df['enc']:
        idc = 'check_' + i
        checkbox = f'<input id="{idc}" type="checkbox" form="MyTable" class="checks"/>'
        checkboxes.append(checkbox)
    df['Arrivo'] = checkboxes
    data_cols = ['ghost'] + ['Pic'] + name_cols + others + ['Arrivo']
    return df[data_cols]

def df_to_html(df):
    #creo doc e aggiungo stile
    code='''<div>
        <input type="text" id="myInput" onkeyup="search()" placeholder="Ricerca per nome...">
	    <button id="submit-btn" action="/submit-form">Esporta</button>
        </div><table id="myTable">'''
    code+='<tr>'
    #aggiungere intestazioni
    for i in df:
        code+='<th>'
        code+=str(i)
        code+='</th>'
    code+='</tr>'
    #itero tra le righe per aggiungere i table data
    for i in df.T:
        code+='<tr>'
        for j in range(0,len(df.T[i])):
            code+='<td>'
            code+=df.T[i][j]
            code+='</td>'
        code+='</tr>'
    code+='</table>'
    
    return code


def add_script(html):
    head = '''
    <!DOCTYPE html><html>
    <head>
      <title>Events</title>
      <!-- Include jQuery library -->
      <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
      <script src="./static/js/scripts.js"></script>
      <link rel="stylesheet" href="./static/styles/events.css">
    </head>
    '''
    closing = '</table></body></html>'  

    page = head + html + closing
    return page
    
def pipeline(file_path):
    data = file_to_data(file_path)
    #print('data:', data)
    df = search_data(data) 
    #print('df:', df)
    return df

def pipeline2(df):
    html = df_to_html(df)
    #print('html:', html)
    page = add_script(html)
    return page


def colonna_arrivi(data, checked_rows):
    arrivi=[]
    a = list(data['ghost'])
    b = list(pd.DataFrame(checked_rows)['column1'])
    for i in a:
        if i in b:
            arrivi.append('Arrivato')
        else:
            arrivi.append('No')
    columns = list(data.columns)
    name_cols = columns[2:4]
    others = columns[4:]
    data['Arrivo'] = arrivi
    data_cols = name_cols + others
    final_data = data[data_cols]
    final_data['Arrivo'] = arrivi
    return final_data
