from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'first_name', 'last_name', 'bio', 'role')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('role',)
    list_editable = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
