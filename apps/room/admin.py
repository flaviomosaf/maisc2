from django.contrib import admin
from .models import Room, Message, Grupo, Hierarchy

# @admin.register(Room)
# class RoomAdmin(admin.ModelAdmin):
#     list_dispaly = ['id', 'name', 'slug',]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room', 'user', 'content', 'created']

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ['group',]

@admin.register(Hierarchy)
class HierarchyAdmin(admin.ModelAdmin):
    list_display = ['user', 'parent', 'child','room','created']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'slug', 'get_user', 'created']

    def get_user(self, obj):
        return [user.username for user in obj.user.all()]

