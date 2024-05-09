from django.contrib import admin

from .models import User, Group, Page, Note

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Page)
admin.site.register(Note)
