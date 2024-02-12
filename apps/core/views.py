from django.shortcuts import render, redirect
from library.views import get_user_current
from room.models import Room
from library.views import *

#------------------------------------------------------------------------
#
#------------------------------------------------------------------------
def core_home(request):
    # BLOCK START
    #==================================================================  
    template = context = user_current = None 
    section, title_page, title_sheet = 'core', 'Project', 'Project'
        
    # BLOCK CENTER
    #================================================================== 
    user_current = get_user_current(request.user)
    room_user = Room.objects.all()
    #print(f'\n\n\n{user_current}\n\n\n')

    #...
    if not user_current: user = User.objects.get(username='flavio')
    else: user = user_current
    register_audit_user(user, section)


    # BLOCK END
    #==================================================================      
    context  = {'section':section,'title_page':title_page,'title_sheet':title_sheet,
                'user_current':user_current, 'room_user':room_user}        
    template = 'core/content/home/home.html'
    return render (request, template, context)

#------------------------------------------------------------------------
#
#------------------------------------------------------------------------
def message_login_required(request):
    # BLOCK START
    #==================================================================  
    template = context = user_current = None 
    section, title_page, title_sheet = 'core', 'Project', 'Project'
        
    # BLOCK CENTER
    #================================================================== 
    user_current = get_user_current(request.user)
    room_user = Room.objects.all()
    message_text = 'To access the chat rooms you need to log in.'
    message_color = 'alert-warning'
    message_signup = None

    # BLOCK END
    #==================================================================      
    context  = {'section':section,'title_page':title_page,'title_sheet':title_sheet,
                'user_current':user_current,'room_user':room_user, 'message_text':
                message_text, 'message_color':message_color,'message_signup':message_signup,}        
    template = 'core/content/home/home.html'
    return render (request, template, context)
