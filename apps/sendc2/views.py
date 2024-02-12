from django.shortcuts import render
from django.core.files import File
from pathlib import Path
from library.views import get_acronym_kind_ents, get_sentiment_anlisys_message, \
get_entities_c2_message, get_count_grammar_message, get_classify_priority_message, \
make_message_with_ents, get_user_current, make_list_with_properties_ents, \
make_list_with_grammar_message, get_sentence_message, get_time_processing, \
get_host_and_ip_sender, get_host_and_ip_receiver, get_tokens_at_message
from library.categories import load_nlp
import spacy
from spacy import displacy
import nltk
from nltk.tokenize import TreebankWordTokenizer
from nltk.util import ngrams
import re
import json
from datetime import datetime

import numpy as np
from time import process_time
import os

#... models
from sendc2.models import Communication
from django.contrib.auth.models import User

#... forms
from sendc2.forms import CommunicationForm

#---------------------------------------------------
# flavio. 
#---------------------------------------------------
def sendc2_home(request):
    # BLOCK START
    #==================================================================  
    section, title_page, title_sheet = 'sendc2', 'Send Message', 'Send Message'  
    template = ''   
        
    # BLOCK MAIN
    #==================================================================  
    user_current = get_user_current(request.user.username)

    user_agent = User.objects.all()

    high,low = [_ for _ in user_agent if _.username=='001brg'], \
    [_ for _ in user_agent if _.username=='010btl']

    # BLOCK END
    #==================================================================       
    context  = {'section':section,'title_page':title_page,'title_sheet':title_sheet,
                'user_current':user_current, 'sender':high[0], 'receiver':low[0]}   
    template = 'sendc2/home/home.html'    
    return render (request, template, context)


#---------------------------------------------------
#
#---------------------------------------------------
def sendc2_message(request):
    # BLOCK START
    #==================================================================  
    form_communication = CommunicationForm()
    section, title_page, title_sheet = 'sendc2', 'Send Message', 'Send Message'
    template = 'sendc2/home/home.html'
        
    # BLOCK MAIN
    #==================================================================  
    user_agent = User.objects.all()
    high, low  = [_ for _ in user_agent if _.username=='001brg'], \
    [_ for _ in user_agent if _.username=='010btl']

    if request.method == 'POST':
        form_communication = CommunicationForm(data=request.POST, files=request.FILES)

        #...
        if form_communication.is_valid():
            data = form_communication.save(commit=False)

            #... get items of the message to handle it
            data.sender = str(form_communication.cleaned_data['sender']).lower()
            data.receiver = str(form_communication.cleaned_data['receiver']).lower()
            data.message = str(form_communication.cleaned_data['message'])
            # form_communication.save()

            #... recognize entities
            context = make_entity_recognize(data.message)

            #...
            context = {'section':section,'title_page':title_page,'title_sheet':title_sheet,
                       'sender':data.sender,'receiver':data.receiver,'sent_message': data.message,
                       'context':context}   

            return render (request, template, context)
        
        else:
            #print(form_communication.errors)
            raise("form_post", form_communication.errors)      


    # BLOCK END
    #==================================================================       
    context  = {'section':section,'title_page':title_page, 'title_sheet':title_sheet} 
    template = 'sendc2/home/home.html'   
    return render (request, template, context)


#---------------------------------------------------
#
#---------------------------------------------------
def make_entity_recognize(message_raw=None):  
    # BLOCK INIT
    #==================================================================  
    message_with_ents = ''
    ents_name, ents_kind, ents_init, ents_end, list_message_ents = [],[],[],[],[]
    noun_count = verb_count = pron_count = adje_count = punc_count = adve_count = 0
    conj_count = det_count = other_count = count_ents = num_count = 0
    lst_noun, lst_verb, lst_adve, lst_pron, lst_adje, lst_punc, lst_conj, lst_det,\
    lst_num, lst_other, len_sent, lst_sent  = [],[],[],[],[],[],[],[],[],[],[],[]

    nlp_maisc2 = load_nlp()[0]
    datetime_now = datetime.now() 
    date = str(datetime_now.strftime("%d/%m/%Y"))
    start_processing = process_time()

    # BLOCK MAIN
    #==================================================================  
    message_raw = str(message_raw).replace("'","")

    doc_message = nlp_maisc2(message_raw)
 
    message_tokens, len_tokens = get_tokens_at_message(message_raw)

    host_sender, ip_sender = get_host_and_ip_sender()
  
    host_receiver, ip_receiver = get_host_and_ip_receiver()

    lst_ents_posi, lst_ents_text, lst_ents_kind = make_list_with_properties_ents(message_tokens)
  
    lst_noun, lst_verb, lst_adve, lst_pron, lst_adje, lst_punc, lst_conj, lst_det, lst_num,\
    lst_other = make_list_with_grammar_message(message_raw)
    
    list_message_ents, dict_message_ents, count_ents = get_entities_c2_message(doc_message)

    message_with_ents = make_message_with_ents(list_message_ents)

    #print(f'\n\n\n{ message_with_ents }\n\n\n')

    noun_count, verb_count, pron_count, adje_count, punc_count, num_count, adve_count, \
    conj_count, det_count, other_count = get_count_grammar_message(message_raw)

    message_priority = get_classify_priority_message(message_raw, count_ents)

    message_sentiment = get_sentiment_anlisys_message(list(message_tokens))

    len_sent, lst_sent = get_sentence_message(message_raw)

    finish_processing = process_time()

    #... calculate duration
    time_processing = finish_processing - start_processing

    #... convert to string
    time_processing = "{0:.5f}".format(time_processing)
    finish_processing = str(finish_processing)
    start_processing = str(start_processing)

    context = {'ents_name':ents_name,'ents_kind':ents_kind,'ents_init':ents_init,'ents_end':ents_end,
               'message_with_ents':message_with_ents,'message_raw':message_raw,'message_tokens':message_tokens,
               'len_tokens':len_tokens,'date':date,'host_sender':host_sender,'host_receiver':host_receiver,
               'ip_sender':ip_sender,'ip_receiver':ip_receiver,'dict_message_ents':dict_message_ents,
               'start_processing':start_processing,'message_priority':message_priority,
               'finish_processing':finish_processing,'time_processing':time_processing,
               'message_sentiment':message_sentiment,'list_message_ents':list_message_ents,
               'noun_count':noun_count,'verb_count':verb_count,'pron_count':pron_count,'adje_count':adje_count,
               'punc_count':punc_count,'adve_count':adve_count,'conj_count':conj_count,'det_count':det_count,
               'other_count':other_count,'num_count':num_count,'lst_ents_posi':lst_ents_posi,
               'lst_ents_text':lst_ents_text,'lst_ents_kind':lst_ents_kind,'lst_noun':lst_noun,
               'lst_verb':lst_verb,'lst_adve':lst_adve,'lst_pron':lst_pron,'lst_adje':lst_adje,
               'lst_punc':lst_punc,'lst_conj':lst_conj,'lst_det':lst_det,'lst_num':lst_num,
               'lst_other':lst_other, 'len_sent':len_sent,'lst_sent':lst_sent }

    make_dictionary_message(context)

    return context


#---------------------------------------------------
#
#---------------------------------------------------
def make_dictionary_message(args):
    message_json = {
        'message':{
            'main':{
                'message_raw':args['message_raw'],
                'message_with_ents':args['message_with_ents'],
            },
            'properties':{
                'tokens':args['message_tokens'],
                'date':args['date'], 
                'tokens_len':args['len_tokens'],
                'host_sender':args['host_sender'], 
                'host_receiver':args['host_receiver'], 
                'ip_sender': args['ip_sender'], 
                'ip_receiver':args['ip_receiver'],
                'start_processing':args['start_processing'],
                'finish_processing':args['finish_processing'], 
                'time_processing':args['time_processing'],
            },
            'priority':{
                'status':args['message_priority'],
            },
            'entities':{
                'ents_posi':args['lst_ents_posi'],
                'ents_text':args['lst_ents_text'],
                'ents_kind':args['lst_ents_kind']
            },
            'sentence':{
                'len_sent':args['len_sent'],
                'lst_sent':str(args['lst_sent'])
            },
            'grammar':{
                'count':{
                    'tot_noun' :str(args['noun_count']),'tot_verb' :str(args['verb_count']),
                    'tot_pron' :str(args['pron_count']),'tot_adej' :str(args['adje_count']),
                    'tot_punc' :str(args['punc_count']),'tot_adve' :str(args['adve_count']),
                    'tot_conj' :str(args['conj_count']),'tot_det'  :str(args['det_count']),
                    'tot_num'  :str(args['num_count']),'tot_other':str(args['other_count'])
                },
                'concept':{
                    'lst_noun':args['lst_noun'],'lst_verb':args['lst_verb'],'lst_adve':args['lst_adve'],
                    'lst_pron':args['lst_pron'],'lst_adje':args['lst_adje'],'lst_punc':args['lst_punc'],
                    'lst_conj':args['lst_conj'],'lst_det':args['lst_det'],'lst_num':args['lst_num'],
                    'lst_other':args['lst_other']
                },
            }
        }
    }

    # message_json = json.dumps(api_maisc2)
    save_message_json(message_json)

    return message_json


#---------------------------------------------------
#
#---------------------------------------------------
def save_message_json(*args):
    message = args[0]
    with open("static/download/data_message_json.json", "w") as write_file:        
        json.dump(message, write_file, indent=4, sort_keys=True)

    return True


#---------------------------------------------------
# flavio. make a table with the elements of the message
#---------------------------------------------------
def make_table_output(message=None):   
    table_entity = BeautifulTable()
    doc_entity = nlp(message)

    table_entity.columns.header = ['ENTIDADE', 'TIPO', 'POSITION', 'START', 'END', ]

    for __, _ in enumerate(doc_entity.ents): 
        table_entity.rows.append([_.text, _.label_, __, _.start_char, _.end_char])

    return table_entity


#---------------------------------------------------
# flavio. Render the result to browser
#---------------------------------------------------
def render_result_to_web(doc):
    colors = {
        "ACTION"    : '#00FFFF',
        "DIRECTION" : '#CCCCFF',
        "EQUIPAMENT": '#D35400',
        "MEMBER"    : '#F1C40F',
        "PLACE"     : '#1ABC9C',
        "UNIT"      : '#3498DB',
        "VEHICLE"   : '#9B59B6',
        "WEAPONS"   : '#E74C3C',
        "ACTION"    : '#ca3ce7',
        "ORGANIZATION":'#3ce1e7'}
    
    options = {"ents": ["ACTION","DIRECTION",
                "EQUIPAMENT","MEMBER",
                "PLACE","UNIT","ORGANIZATION",
                "VEHICLE","WEAPONS",],
                "colors": colors}
    
    render_entity_ux = displacy.serve(doc, style="ent", auto_select_port=True, options=options)   

    return render_entity_ux
