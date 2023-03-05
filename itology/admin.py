from django.contrib import admin

from itology.models import Advert, Client, Comment, Role, Section, Team

admin.site.register(Client)
admin.site.register(Role)
admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(Team)
admin.site.register(Advert)
