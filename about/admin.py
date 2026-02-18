from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from about.models import AboutPage, Contact

# Register your models here.


@admin.register(AboutPage)
class AboutPageAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'updated_on')
    search_fields = ['title', 'author']
    list_filter = ('updated_on',)
    summernote_fields = ('content',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'type', 'read')
    search_fields = ['name', 'email', 'message']
    list_filter = ('type', 'read')
