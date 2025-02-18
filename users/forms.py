from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth.forms import UserCreationForm  
from django import forms
import re
from tasks.forms import StyleformedMixing
from django.contrib.auth.forms import AuthenticationForm
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','password2','email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for fieldname in ['username','password1','password2']:
            self.fields[fieldname].help_text = None

class CustomRegistrationForm(StyleformedMixing,forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','confirm_password','email']
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', password1):
            errors.append(
                'Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password1):
            errors.append(
                'Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password1):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password1):
            errors.append(
                'Password must include at least one special character.')

        if errors:
            raise forms.ValidationError(errors)

        return password1    
    
    # User model er attribute gula override korsi
    def clean(self): #non field error
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password1 != confirm_password:
            raise forms.ValidationError("Password didn't match")
        return cleaned_data

    def clean_email(self): 
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("this email is already in use, please enter another email")
        return email

class LoginForm(StyleformedMixing, AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        
class AssignRoleForm(StyleformedMixing,forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="select a role"
    )

class CreateGroupForm(StyleformedMixing,forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset = Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required = False,
        label = 'Assign Permission'
    )
    class Meta:
        model = Group
        fields = ['name','permissions']
    