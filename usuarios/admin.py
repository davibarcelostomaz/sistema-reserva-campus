   from django.contrib import admin
   from django.contrib.auth.admin import UserAdmin

   from .models import Usuario


   @admin.register(Usuario)
   class UsuarioAdmin(UserAdmin):
       fieldsets = UserAdmin.fieldsets + (
           ('Perfil de acesso', {'fields': ('perfil',)}),
       )
       add_fieldsets = UserAdmin.add_fieldsets + (
           ('Perfil de acesso', {'fields': ('perfil',)}),
       )
       list_display = ('username', 'email', 'first_name', 'last_name', 'perfil', 'is_staff')
       list_filter = UserAdmin.list_filter + ('perfil',)
