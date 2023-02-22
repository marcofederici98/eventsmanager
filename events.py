#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import time
from flask import Flask, render_template


# In[2]:


df=pd.read_excel("persone_famose.xlsx")


# In[3]:


df=pd.read_csv('vips.csv', delimiter=';' )


# In[4]:


df


# In[5]:


df=df.drop(0)


# In[6]:


df


# In[7]:


df['enc_name']=df['Nome']+'_'+df['Cognome']
df


# In[8]:


base_url="https://keywordimage.com/image.php?q="


# In[9]:


'''for i in df['nome completo']:
    name=i+'.jpeg'
    url=base_url+i+"_viso"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    img_tag = soup.find("img")
    img_url = img_tag.get("src")
    f=open(name,'wb')
    response_img = requests.get(img_url)
    f.write(response_img.content)
    f.close()
    time.sleep(3)
    img = mpimg.imread(name)
    imgplot = plt.imshow(img)
    plt.title(name)
    plt.show()'''
    
    


# In[10]:


img_urls=[]
buttons=[]
for i in df['enc_name']:
    wt=200
    ht=wt
    name=i+'.jpeg'
    url=base_url+i+"_viso"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    img_tag = soup.find("img")
    img_url = img_tag.get("src")
    button=f'<a href="{img_url}" target="blank"> <button id="{i}">Visualizza intera</button> </a>'
    img_html='<img src="'+img_url+f'" height="{ht}">'
    img_urls.append(img_html)
    buttons.append(button)
    time.sleep(2)


# In[11]:


df['img']=img_urls
df['buttons']=buttons

df['Pic']=df['img']+'<br>'+df['buttons']
df['Personaggio']=df['Nome']+' '+df['Cognome']
print(buttons)


# In[12]:


for i in buttons:
    print(i)


# In[13]:


checkbox='<form><input type="checkbox" class="checks"></form>'
df['Arrivo']=[checkbox for i in range(0,len(df))]


# In[14]:


df


# In[15]:


df=df[['Pic', 'Personaggio', 'Arrivo']]


# In[16]:


df


# In[17]:


def df_to_html(df):
    #creo doc e aggiungo stile
    code='<table>'
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
            
            
            
        
        
        
    


# In[18]:


html_code=df_to_html(df)


# In[19]:


html_code


# In[ ]:




