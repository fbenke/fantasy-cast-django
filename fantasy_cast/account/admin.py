from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin

from account.models import CustomUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_username()
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):

    add_form = UserCreationForm

    list_display = ('email', 'is_admin', 'username')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)


class CustomTokenAdmin(TokenAdmin):

    def user_email(self, obj):
        return obj.user.email

    def user_id(self, obj):
        return obj.user.id

    list_display = ('user_email', 'key', 'created')
    list_per_page = 20

    readonly_fields = ('user_id', 'user_email', 'key')
    fields = readonly_fields

try:
    admin.site.unregister(Token)
except admin.sites.NotRegistered:
    pass
admin.site.register(Token, CustomTokenAdmin)
