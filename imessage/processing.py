import pandas as pd
import uuid
import numpy as np
import re
import sqlite3
from textblob import TextBlob 
import datetime
import shutil

source = '../../../../Library/Messages/chat.db'
dest = "chat.db"
shutil.copyfile(source, dest)

db = sqlite3.connect('chat.db')
cur = db.cursor()
pd.set_option("display.max_columns", None)



def main():
    global expressions
    people = pd.read_excel("contacts.xlsx")
    contacts = pd.DataFrame(columns=contact_columns)
    phones = pd.DataFrame(columns=phone_columns)
    emails = pd.DataFrame(columns=email_columns)

    phone_types = ['Phone : ', 'Phone : mobile', 'Phone : home', 'Phone : work', 'Phone : main', 'Phone : Other', 'Phone : work fax', 'Phone : phone', 'Phone : iPhone']
    email_types = ['Email : ', 'Email : work', 'Email : home', 'Email : other', 'Email : iCloud', 'Email : Junk']
    
    for index, person in people.iterrows():
        contact_id = str(uuid.uuid4())
        person['contacts.id'] = contact_id
        contact = {y:person[x] for (x,y) in contact_map.items()}
        contacts = contacts.append(contact, ignore_index=True)
        
        for p_type in phone_types:
            if not pd.isna(person[p_type]):
                number = re.sub("[^0-9]", "", person[p_type])
                if (len(number) > 10):
                    number = number[1:]
                phone = {'phones.id': str(uuid.uuid4()),
                         'phones.contacts.id':contact_id,
                         'phones.number':number,
                         'phones.type':phone_map[p_type]}
                phones = phones.append(phone, ignore_index=True)
        
        for e_type in email_types:
            if not pd.isna(person[e_type]):
                addr = person[e_type].strip()
                email = {'emails.id': str(uuid.uuid4()),
                         'emails.contacts.id':contact_id,
                         'emails.address':addr,
                         'emails.type':email_map[e_type]}
                emails = emails.append(email, ignore_index=True)
                
    phones['value'] = phones['phones.number']
    emails['value'] = emails['emails.address']
    
    
    message = pd.read_sql_query("select * from message", db).add_prefix("message.")
    chat_message_join = pd.read_sql_query("select * from chat_message_join", db).add_prefix("cmj.")
    chat_handle_join = pd.read_sql_query("select * from chat_handle_join", db).add_prefix("chj.")
    handle = pd.read_sql_query("select * from handle", db).add_prefix("handle.")
    chat = pd.read_sql_query("select * from chat", db).add_prefix("chat.")
    
    me = {
        'handle.ROWID': 0,
        'handle.id': '+17204404183',
        'handle.country': "US",
        'handle.service': 'iMessage',
        'handle.uncanonicalized_id': '7204404183',
        'handle.person_centric_id':None  
    } 
    handle = handle.append(me, ignore_index=True)
    
    phones1 = phones.rename(columns={"phones.contacts.id":'contacts.id'})
    emails1 = emails.rename(columns={"emails.contacts.id":'contacts.id'})
    
    phone_email_combined = pd.concat([phones1, emails1], axis=0).add_prefix("info.").drop_duplicates("info.value")
    
    message.loc[message['message.is_from_me'] == 1, 'message.handle_id'] = 0
    texts1 = handle.merge(message, left_on="handle.ROWID", right_on='message.handle_id', how='right')
    
    texts2 = chat_message_join.merge(texts1, left_on="cmj.message_id", right_on='message.ROWID', how='right')
    texts2['handle.id_clean'] = texts2['handle.id'].map(lambda x: clean(x))
    
    texts3 = phone_email_combined.merge(texts2, left_on="info.value", right_on="handle.id_clean", how='right')
    
    texts4 = contacts.merge(texts3, left_on="contacts.id", right_on="info.contacts.id", how='right')
    texts4 = texts4[sorted(list(texts4))]
    
    texts4 = texts4[~texts4['message.text'].map(lambda x: type(x) is str) == False].drop_duplicates("message.ROWID")
    
    texts4.to_csv("messages.csv", index=False)
    
    convo = texts4[list(subset.keys())].rename(columns=subset)

    epoch = int(datetime.datetime(2001, 1, 1, 0, 0).strftime('%s'))
    convo['datetime'] = convo['date'].map(lambda x: int(round(x/1000000000,0)) + epoch - 10*60*60)
    convo['datetime'] = pd.to_datetime(convo['datetime'], unit="s")
    
    convo['date_read'] = convo['date_read'].map(lambda x: int(round(x/1000000000,0)) + epoch - 10*60*60 if x > 0 else float("NaN"))
    convo['date_read'] = pd.to_datetime(convo['date_read'], unit="s")
    
    convo['date_delivered'] = convo['date_delivered'].map(lambda x: int(round(x/1000000000,0)) + epoch - 11*60*60)
    convo['date_delivered'] = pd.to_datetime(convo['date_delivered'], unit="s")
    
    convo['birthday'] = pd.to_datetime(convo['birthday'])
    
    convo = convo.reset_index().drop('index', axis=1)
    expressions = list(convo['expression'].unique())
    expressions.pop(0)
    convo['chat_id'].astype('int64', errors='ignore')
    convo['address_street'] = convo['address_street'].map(lambda x: x if type(x) != str else re.sub("\n", " ", x))
    convo['expression'] = convo['expression'].map(lambda x: expression(x))
    convo['polarity'] = convo['text'].map(lambda x: polar(x))
    convo['subjectivity'] = convo['text'].map(lambda x: subjective(x))
    convo['word_count'] = convo['text'].map(lambda x: word_count(x))
    convo['is_text'] = convo['text'].map(lambda x: is_text(x))
    convo['reaction'] = convo['text'].map(lambda x: reaction(x))
    convo['year'] = pd.DatetimeIndex(convo['datetime']).year
    convo['month'] = pd.DatetimeIndex(convo['datetime']).month
    convo['day'] = pd.DatetimeIndex(convo['datetime']).day
    convo['weekday'] = pd.DatetimeIndex(convo['datetime']).weekday
    convo['hour'] = pd.DatetimeIndex(convo['datetime']).hour
    convo['time'] = pd.DatetimeIndex(convo['datetime']).time
    convo['date'] = pd.DatetimeIndex(convo['datetime']).date
    
    convo.to_csv("convo.csv", index=False)


expressions = []

contact_map = {
    'contacts.id':'contacts.id',
    'Last name': 'contacts.last_name',
    'First name': 'contacts.first_name',
    'Middle name': 'contacts.middle_name',
    'Job title': 'contacts.job_title',
    'Company': 'contacts.company',
    'URL : homepage': 'contacts.url_home',
    'URL : Profile': 'contacts.url_profile',
    'Birthday': 'contacts.birthday',
    'Address : home : Street': 'contacts.address_street_home',
    'Address : home : City': 'contacts.address_city_home',
    'Address : home : State': 'contacts.address_state_home',
    'Address : home : Country': 'contacts.address_country_home',
    'Address : home : ZIP': 'contacts.address_zip_home',
    'Address : work : Street': 'contacts.address_street_work',
    'Address : work : City': 'contacts.address_city_work',
    'Address : work : State': 'contacts.address_state_work',
    'Address : work : Country': 'contacts.address_country_work',
    'Address : work : ZIP': 'contacts.address_zip_work',
    'Related name : mother': 'contacts.related_mother',
    'Related name : father': 'contacts.related_father',
    'Related name : child': 'contacts.related_child',
    'Note': 'contacts.note'
}

contact_columns = ['contacts.id','contacts.last_name','contacts.first_name','contacts.middle_name','contacts.job_title','contacts.company','contacts.url_home','contacts.url_profile','contacts.birthday','contacts.related_mother','contacts.related_father','contacts.related_child','contacts.note']

phone_map = {
    'contacts.id':'phones.contacts.id',
    'phones.id':'phones.id',
    'Phone : ': 'phones.phone',
    'Phone : mobile': 'phones.mobile',
    'Phone : home': 'phones.home',
    'Phone : work': 'phones.work',
    'Phone : main': 'phones.main',
    'Phone : Other': 'phones.other',
    'Phone : work fax': 'phones.fax',
    'Phone : phone': 'phones.phone_phone',
    'Phone : iPhone': 'phones.iphone'
}

phone_columns = ['phones.id','phones.contacts.id','phones.number', 'phones.type']

email_map = {
    'contacts.id':'emails.contacts.id',
    'emails.id':'emails.id',
    'Email : ': 'emails.email',
    'Email : work': 'emails.work',
    'Email : home': 'emails.home',
    'Email : other': 'emails.other',
    'Email : iCloud': 'emails.icloud',
    'Email : Junk': 'emails.junk'
}

email_columns = ['emails.id','emails.contacts.id','emails.address', 'emails.type']

subset = {
    'message.ROWID': 'message_id',
    'cmj.chat_id': 'chat_id',
    'contacts.id': 'contact_id',
    'message.text': 'text',
    'contacts.first_name': 'first_name',
    'contacts.last_name': 'last_name',
    'info.emails.address': 'email_address',
    'info.phones.number': 'phone_number',
    'message.date': 'date',
    'message.date_delivered': 'date_delivered',
    'message.date_read': 'date_read',
    'contacts.address_street_home': 'address_street',
    'contacts.address_city_home': 'address_city',
    'contacts.address_state_home': 'address_state',
    'contacts.address_zip_home': 'address_zip',
    'contacts.birthday': 'birthday',
    'contacts.company': 'company',
    'contacts.job_title': 'job_title',
    'contacts.url_home': 'home_page',
    'contacts.url_profile': 'profile_page',
    'handle.service': 'handle_service',
    'message.expressive_send_style_id': 'expression',
    'message.cache_roomnames':'group_name',
    'message.is_delivered': 'is_delivered',
    'message.is_from_me': 'is_from_me',
    'message.is_read': 'is_read'
}

expressions_clean = {
    'com.apple.MobileSMS.expressivesend.loud': "Loud Send",
    'com.apple.messages.effect.CKHeartEffect': "Heart Effect",
    'com.apple.MobileSMS.expressivesend.invisibleink': "Invisibile Ink Send",
    'com.apple.messages.effect.CKEchoEffect': "Echo Effect",
    'com.apple.MobileSMS.expressivesend.gentle': "Gentle Send",
    'com.apple.MobileSMS.expressivesend.impact': "Impact Send",
    'com.apple.messages.effect.CKConfettiEffect': "Confetti Effect",
    'com.apple.messages.effect.CKSpotlightEffect': "Spotlight Effect",
    'com.apple.messages.effect.CKFireworksEffect': "Fireworks Effect",
    'com.apple.messages.effect.CKSparklesEffect': "Sparkles Effect",
    'com.apple.messages.effect.CKHappyBirthdayEffect': "Happy Birthday Effect"
}

def clean(x):
    x = re.sub("[^0-9a-zA-Z@.]","", x)
    try:
        int(x)
        if len(x) > 10:
            x = x[1:]
    except:
        pass
    return x


def word_count(x):
    if type(x) is str:
        x = re.sub('[^a-zA-Z\s]', '', x)
        x = re.sub('\s+', ' ', x)
        x = re.sub('\n', ' ', x)
        x = x.strip()
        return x.count(" ") + 1
    else:
        return float("NaN")


def is_text(x): 
    if type(x) is str:
        return 1
    else:
        return 0
    
    
def polar(x):
    if type(x) is str:
        return TextBlob(x).polarity
    else:
        return float("NaN")

    
def subjective(x):
    if type(x) is str:
        return TextBlob(x).subjectivity
    else:
        return float("NaN")

    
def expression(x):
    exp = float("NaN")
    for expression in expressions:
        if x == expression:
            exp = expressions_clean[expression]
    return exp


def reaction(x):
    # x = re.sub('“', "\"", x)
    # x = re.sub('”', "\"", x)
    if x == None:
        return float("NaN")
    reactions = ['Loved “', 'Loved a', 'Liked “', 'Liked a', 'Disliked “', 'Disliked a', 'Laughed at “', 'Laughed at a', 'Emphasized “', 'Emphasized a', 'Questioned “', 'Questioned a']
    for reaction in reactions:
        if reaction in x:
            return reaction
    return float("NaN")


main()