from django import forms
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    email_password = forms.CharField(widget=forms.PasswordInput, label='Email Password')
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'email_password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        return user