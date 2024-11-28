import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ScannerForm
from .models import Scanner
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from zapv2 import ZAPv2
from django.conf import settings

zap = ZAPv2(apikey=settings.ZAP_API_KEY)  # Sadece API anahtarı veriyoruz
zap.core.baseurl = settings.ZAP_URL 

@login_required
def scanner(request):
    if request.method == 'POST':
        form = ScannerForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.user = request.user  # URL'yi ekleyen kullanıcıyı ilişkilendir
            site.save()
            messages.success(request, "URL başarıyla kaydedildi.")

            # ZAP taraması başlatılıyor
            target_url = site.url

            # ZAP ile taramayı başlat
            try:
                zap.urlopen(target_url)  # İlk olarak hedef URL'yi açıyoruz
                scan_id = zap.ascan.scan(target_url)  # ZAP taramasını başlatıyoruz

                # Tarama işleminin bitmesini bekleyelim
                while int(zap.ascan.status(scan_id)) < 100:  # Tarama tamamlanana kadar bekle
                    time.sleep(5)

                messages.success(request, f"Tarama tamamlandı: {target_url}")
            except Exception as e:
                messages.error(request, f"Tarama sırasında bir hata oluştu: {str(e)}")

            return redirect('user:dashboard')  # Kullanıcıyı dashboard sayfasına yönlendir

        else:
            messages.error(request, "URL kaydedilirken bir hata oluştu.")
    else:
        form = ScannerForm()

    return render(request, 'scanner.html', {'form': form})

@staff_member_required
def approve_url(request, site_id):
    # Siteyi alırken hatalı ID'yi engellemek için get_object_or_404 kullanıyoruz.
    site = get_object_or_404(Scanner, id=site_id)
    
    site.is_approved = True
    site.save()
    
    messages.success(request, f"URL {site.url} başarıyla onaylandı.")
    return redirect('admin_dashboard')  # Admin kontrol paneline yönlendir

@staff_member_required
def admin_dashboard(request):
    unapproved_sites = Scanner.objects.filter(is_approved=False)  # Onaylanmamış siteler
    return render(request, 'scanner/admin_dashboard.html', {'sites': unapproved_sites})
