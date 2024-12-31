from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User

@login_required
def messages_view(request):
    # Kullanıcının gönderdiği mesajlar
    sent_messages = Message.objects.filter(sender=request.user)

    # Kullanıcının aldığı mesajlar
    received_messages = Message.objects.filter(receiver=request.user)

    return render(request, 'messages.html', {
        'sent_messages': sent_messages,
        'received_messages': received_messages,
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST or None )
        if form.is_valid():
            try:
                admin_user = User.objects.get(username='hacer')  # Admin kullanıcı olarak sadece bana gelecek
                message = form.save(commit=False)
                message.sender = request.user  # Mesajı gönderen kullanıcı
                message.receiver = admin_user  # Varsayılan alıcı olarak admini ayarladım
                message.save()
                return redirect('messaging:messages')  # Mesajlar sayfasına yönlendiriyo
            except User.DoesNotExist:
                return render(request, 'send_message.html', {
                    'form': form,
                    'error': "Admin kullanıcı bulunamadı."
                })
        else:
            return render(request, 'send_message.html', {
                'form': form,
                'error': "Form doğrulama hatası. Lütfen bilgileri kontrol edin.",
                'form_errors': form.errors
            })
    else:
        form = MessageForm()
    context = {
        "form": form
    }
    return render(request, 'send_message.html', context)
@login_required

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    return render(request, 'message_detail.html', {
        'message': message,
        'user': request.user,  # Şablonda kullanılacak 'user' değişkeni
    })
