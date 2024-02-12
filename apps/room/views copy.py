from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Room, Message, Hierarchy
from library.views import get_user_current
from .models import Room, Message, Hierarchy

def roomc2_home(request):
    user_current = room_user = None
    template, context = 'roomc2/rooms/chat_room.html', {'user_cureent':user_current}

    user_current = get_user_current(request.user)
    room_user = Room.objects.filter(user=user_current)

    if len(room_user)>1:
        return redirect ('room:room_open', room_user[0].slug)

    return render (request, template, context)

#def roomc2_home(request):
    # context, template, open_room = {}, 'roomc2/rooms/chat_room.html', None
    # num_rooms, room_one, room_two = False, None, None

    # user_current = get_user_current(request.user)
    # rooms_user = Room.objects.filter(user=user_current)

    # if len(rooms_user)>1:num_rooms, room_one, room_two = True, rooms_user[0].slug, rooms_user[1].slug
    # else: room_one = rooms_user[0].slug

    # print(f'\n\n\n >> user : {user_current}')
    # print(f' >> len_ : {len(rooms_user)}')
    # print(f' >> rooms: {open_room}\n\n\n')

    # context ={'rooms_user':rooms_user, 'user_current':user_current, 'room_one':room_one,
    #           'room_two':room_two,'num_rooms':num_rooms,}

    # return render (request, template, context)



def roomc2_open(request, slug):
    # BLOCK INIT
    #==================================================================  
    title_page, title_sheet, section = 'Maisc2', 'Chat c2', 'chatc2' 
    room = messages_room = hierarchy_user = user_current = None
    dict_room_user, template = {}, 'roomc2/rooms/chat_one.html'  
        
    # BLOCK MAIN
    #==================================================================  
    message = 'Em construção, em breve estará funcionando!'
    user_current = get_user_current(request.user)

    room           = Room.objects.get(slug=slug)
    messages_room  = Message.objects.filter(room=room)[0:40]
    hierarchy_user = Hierarchy.objects.filter(user = user_current.id)
    rooms_user     = Room.objects.filter(user=user_current)

    #... Mosafi => get all rooms of the logged user
    for _ in rooms_user:dict_room_user[_]={'room':_.room,'user':_.user}


    # BLOCK END
    #==================================================================       
    context = {'user_current':user_current,'room':room,'messages_room':messages_room,
               'rooms_user':rooms_user,'hierarchy_user':hierarchy_user,'dict_room_user':
               dict_room_user,}
    return render(request, template, context)


#...
@login_required
def room_open(request, slug):
    # BLOCK START
    #==================================================================  
    room = messages_room = hierarchy_user = user_current = None
    dict_room_user, template = {}, 'roomc2/rooms/chat_one.html'

    # BLOCK CENTER
    #================================================================== 
    #... Mosafi => get current user
    user_current = get_user_current(request.user)

    #... Mosafi => get data of models
    #room           = Room.objects.get(slug=slug)
    messages_room  = Message.objects.filter(room=room)[0:40]
    hierarchy_user = Hierarchy.objects.filter(user = user_current.id)
    rooms_user     = Room.objects.filter(user=user_current)

    #... Mosafi => get all rooms of the logged user
    for _ in rooms_user:dict_room_user[_]={'room':_.room,'user':_.user}

    print(f'\n\n\n >> {len(rooms_user)}\n\n\n')

    # BLOCK END
    #==================================================================     
    context = {'user_current':user_current,'room':room,'messages_room':messages_room,
               'rooms_user':rooms_user,'hierarchy_user':hierarchy_user,'dict_room_user':
               dict_room_user,}
    return render(request, template, context)


