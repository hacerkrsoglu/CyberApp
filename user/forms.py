from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password      
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı", max_length=150)
    password = forms.CharField(label="Parola", widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="Ad", max_length=30, required=True)
    last_name = forms.CharField(label="Soyad", max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Parola", required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Parola Tekrar", required=True)
    terms_agreed = forms.BooleanField(
        label="KVKK ve Gizlilik Politikası'nı kabul ediyorum.",
        required=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Parolalar eşleşmiyor!")
        return password_confirm

    def save(self, commit=True):
        """Şifreyi hashleyerek kullanıcıyı kaydeder."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Şifreyi hashlemek için bu şekilde kullanıyotuz
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(
        label="Mevcut Şifre", 
        widget=forms.PasswordInput,
        help_text='Mevcut şifrenizi girin'
    )
    new_password = forms.CharField(
        label="Yeni Şifre", 
        widget=forms.PasswordInput,
        help_text='En az 8 karakter, büyük-küçük harf ve rakam içermeli'
    )
    confirm_new_password = forms.CharField(
        label="Yeni Şifre Tekrar", 
        widget=forms.PasswordInput,
        help_text='Yeni şifreyi tekrar girin'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Mevcut şifreniz yanlış!")
        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        try:
            validate_password(new_password, self.user)
        except ValidationError as e:
            raise forms.ValidationError(list(e.messages))
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError({
                'confirm_new_password': "Yeni şifreler eşleşmiyor!"
            })

        return cleaned_data  
    


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="E-posta Adresi")

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Yeni Şifre"
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput, 
        label="Yeni Şifre Tekrar"
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise forms.ValidationError("Şifreler eşleşmiyor.")
        
        return cleaned_data

