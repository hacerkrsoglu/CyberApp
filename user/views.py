from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import activation_token
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import UserProfileForm,PasswordChangeForm,PasswordResetRequestForm,PasswordResetForm
from scanner.models import Scanner 
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User

def index(request):
    if request.user.is_authenticated:  # Kullanıcı giriş yapmışsa
        return redirect("user:dashboard")  # Dashboard'a yönlendir
    return render(request, "index.html")  # Giriş yapmamışsa ana sayfa göster 


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False  # Kullanıcıyı başlangıçta aktif yapmıyor
        user.save()

        # Aktivasyon bağlantısını oluşturduk burda
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = activation_token.make_token(user)
        activation_link = request.build_absolute_uri(
            f"/user/activate/{uid}/{token}/"
        )

        # E-posta gönderdiğimdeki taslak
        subject = "Hesabınızı Aktive Edin"
        message = f"""
        Hesabınızı aktive etmek için aşağıdaki bağlantıya tıklayın:
        {activation_link}
        
        Bu bağlantı 24 saat geçerlidir.
        """
        send_mail(
            subject, 
            message, 
            'noreply@example.com', 
            [user.email],
            fail_silently=False,
        )

        messages.success(request, "Aktivasyon e-postası gönderildi. Lütfen e-posta kutunuzu kontrol edin.")
        return redirect("index")
    return render(request, "register.html", {"form": form})
def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form":form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username , password = password)

        if user is None:
            messages.info(request,"Kullanıcı Adı veya Parola Hatalı")
            return render(request,"login.html",context)
        messages.success(request,"Başarıyla Giriş Yaptınız.")
        login(request,user)
        return redirect("user:dashboard")
    return render(request,"login.html",context)

def logoutUser(request):
    logout(request)
    messages.success(request,"Başarıyla Çıkış Yaptınız")
    return redirect("index")

@login_required(login_url="user:login")
def dashboard(request):
    return render(request,"dashboard.html")

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Hesabınız aktifleştirildi. Giriş yapabilirsiniz.")
        return redirect("user:login")
    else:
        return HttpResponse("Aktivasyon bağlantısı geçersiz.")
    

@login_required(login_url="user:login")
def profile_view(request):
    
    approved_sites = Scanner.objects.filter(user=request.user, is_approved=True)
    unapproved_sites = Scanner.objects.filter(user=request.user, is_approved=False)

    return render(request, 'profile.html', {
        'approved_sites': approved_sites,
        'unapproved_sites': unapproved_sites,
    })

@login_required(login_url="user:login")
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil başarıyla güncellendi.")
            return redirect('user:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Şifreyi değiştirmek için
            request.user.set_password(form.cleaned_data['new_password'])
            request.user.save()
            messages.success(request, 'Şifreniz başarıyla değiştirildi.')
            return redirect('user:login')
        else:
            # Eğer form geçerli değilse, hata mesajı gösteriyoruz 
            messages.error(request, 'Şifrenizi değiştirme işlemi başarısız oldu.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                
                # Token oluşturduk burda
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                
                # Reset linki oluşturuyoruz şifre sıfrılamak için
                reset_link = request.build_absolute_uri(
                    f"/user/password-reset-confirm/{uid}/{token}/"
                )
                
                # E-posta gönderiyor burda
                subject = "Şifre Sıfırlama"
                message = f"""
                Şifrenizi sıfırlamak için aşağıdaki linke tıklayın:
                {reset_link}
                
                Bu link 24 saat geçerlidir.
                """
                
                send_mail(
                    subject, 
                    message, 
                    'noreply@example.com', 
                    [email],
                    fail_silently=False,
                )
                
                messages.success(request, "Şifre sıfırlama bağlantısı e-postanıza gönderildi.")
                return redirect('user:login')
            
            except User.DoesNotExist:
                messages.error(request, "Bu e-posta adresine kayıtlı kullanıcı bulunamadı.")
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'password_reset_request.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                messages.success(request, "Şifreniz başarıyla sıfırlandı.")
                return redirect('user:login')
        else:
            form = PasswordResetForm()
        
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Geçersiz şifre sıfırlama bağlantısı.")
        return redirect('login')    
    
def privacy_policy(request):
    return render(request, "privacy_policy.html")
    