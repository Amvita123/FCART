from django import forms
from FCART_APP.models import User
from django.core.exceptions import ValidationError


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone_no = forms.CharField(max_length=10, min_length=10, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_no', 'gender', 'address', 'verify_through', 'role', 'password']

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError("Password and confirm_password does not match, Enter a correct password")
        return confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Username is required")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

