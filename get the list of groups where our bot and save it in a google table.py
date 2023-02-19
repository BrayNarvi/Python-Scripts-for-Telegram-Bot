#Remember that initially your telegram bot if it is a member of a group, it accepts messages beginning with / and where the name of the bot is mentioned.
#To receive all the text from the entire group you need in the settings of the bot through BotFather do - /setprivacy disabled 


import requests
import pandas as pd

#enter the token
token = '111111111111111111'

url = f'https://api.telegram.org/bot{token}/getUpdates'

payload = {
    "offset": 0,
    "limit": 100,
    "timeout": None
}

response = requests.post(url, json=payload)

chat_data = []

for update in response.json()['result']:
    temp_chat_dict = {}
    
    if 'message' in update:
        temp_chat_dict.update(update['message']['chat'])
        chat_data.append(temp_chat_dict)
    else:
        continue
    
chat_table = pd.DataFrame(chat_data)

if chat_table.empty:
    print('Чатов нет')
else:
    chat_table = chat_table.drop_duplicates()
chat_table = chat_table.reset_index(drop=True)    
chat_table

#The script below saves the resulting data in a specific Google Table. 
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Sign in to the Google API
scope = ['https://www.googleapis.com/auth/drive']

#You need to create a service account and get JSON KEy and put it in the script folder named credentials.json
#Also don't forget to enable google tables API in your Google Cloud project
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# открываем таблицу
sheet_url = 'https://docs.google.com/spreadsheets/d/1111111111111/edit#gid=0'
sheet = client.open_by_url(sheet_url).sheet1

# Saving data to a google table
if not chat_table.empty:
    # add new data to the end of the table
    sheet.insert_rows(chat_table.astype(str).values.tolist(), row=len(sheet.get_all_values())+1)
