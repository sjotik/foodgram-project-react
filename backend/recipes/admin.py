from django.contrib import admin


from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'slug')
    list_filter = ('name',)
    list_editable = ('color',)
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
