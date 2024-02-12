from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Room, Message, Hierarchy
from library.views import get_user_current
import json
from nltk.tokenize import word_tokenize

@login_required(login_url='core:message_login_required')
def rooms_home(request):
    # BLOCK START
    #==================================================================  
    section, title_page, title_sheet = 'chatc2', 'Chat C2', 'Chat C2'
    rooms = list_user_room = None

    # BLOCK MAIN
    #================================================================== 
    user_current = get_user_current(request.user.username)

    #...
    rooms = Room.objects.filter(user=user_current.id)
    list_user_room = [(s.user, list(s.user.all()),) for s in rooms]

    #...
    if len(rooms)<=1: return redirect('room:room_chat',rooms[0].slug)
    elif len(rooms)>1: return redirect('room:room_chat',rooms[0].slug)

    # BLOCK END
    #================================================================== 
    context = {'rooms':rooms,'user_current':user_current,'list_user_room':list_user_room, 
               'section':section, 'title_page':title_page, 'title_sheet':title_sheet}
    template = 'room/rooms_home.html'
    return render(request, template, context)

#...
@login_required
def room_chat(request, slug):
    # BLOCK START
    #==================================================================  
    room = messages_room_first = hierarchy_user = user_current = None
    list_room_user, dict_room_user, section = [], {}, 'chatc2'
    section, title_page, title_sheet = 'chatc2', 'Chat C2', 'Chat C2'
    first_room, second_room, messages_room_second = None, None, None

    # BLOCK MAIN
    #================================================================== 
    user_current = get_user_current(request.user)
    user_photo   = user_current.profile.photo

    #...
    room  = Room.objects.get(slug=slug)
    rooms_user = Room.objects.filter(user=user_current)
    
    #...
    for _ in rooms_user:
        dict_room_user[_]={'room':_.room,'user':_.user}
        list_room_user.append(_.slug)

    #...
    if len(list_room_user)>1: 
        first_room, second_room = list_room_user[0], list_room_user[1]
        messages_room_first  = Message.objects.filter(room__slug=first_room)[0:216]
        messages_room_second = Message.objects.filter(room__slug=second_room)[0:216]
    else: 
        first_room = list_room_user[0]
        messages_room_first = Message.objects.filter(room__slug=slug)[0:72]

    lst, dic = [], {}
    for __, _ in enumerate(messages_room_first):
        #print('>> ',_.content)
        token_msg = str(_.content).split(" ")
        lst.append(token_msg)

    for w in range(0, len(lst)):
        for count, q in enumerate(range(0, len(lst[w]))):
            color = '#FFFFFF'
            if lst[w][q]=='[ACT]': bgcolor = '#00FFFF'
            elif lst[w][q]=='[AGT]': bgcolor = '#F1C40F'
            elif lst[w][q]=='[DRT]': bgcolor = '#5d5dd9'
            elif lst[w][q]=='[VHC]': bgcolor = '#9B59B6'
            elif lst[w][q]=='[UNT]': bgcolor = '#3498DB'
            elif lst[w][q]=='[WEP]': bgcolor = '#E74C3C'
            elif lst[w][q]=='[PLC]': bgcolor = '#1ABC9C'
            else: 
                bgcolor = 'transparent'
                color = '#000000'
            dic[w,count] = {count:{'term':lst[w][q], 'bgcolor':bgcolor, 'color':color}}          
            print(color)  
        break

    #print('\n\n\n')
    #print(lst[0][1])
    #print(dic)
    print('\n\n')

    # BLOCK END
    #==================================================================     
    template = 'room/room_chat.html'
    context  = {'user_current':user_current,'room':room,'messages_room_first':messages_room_first,
                'messages_room_second':messages_room_second,'rooms_user':rooms_user,'hierarchy_user':
                hierarchy_user,'dict_room_user':dict_room_user,'section':section,'first_room':first_room,
                'second_room':second_room, 'title_page':title_page, 'title_sheet':title_sheet,
                'list_room_user':list_room_user, 'user_photo':json.dumps(str(user_photo)), 
                'hidden_scroll':True,'dic':dic}    
    return render(request, template, context)
