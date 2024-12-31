import time
import urllib.parse
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib import messages
from zapv2 import ZAPv2
from .forms import ScannerForm
from .models import Scanner
import re

zap = ZAPv2(apikey=settings.ZAP_API_KEY)  # ZAP API bağlantısı
zap.core.baseurl = settings.ZAP_URL  # ZAP URL'si

@login_required
def scanner(request):
    if request.method == 'POST':
        form = ScannerForm(request.POST)
        if form.is_valid():
            site = form.save(commit=False)
            site.user = request.user  # URL'yi ekleyen kullanıcıyı ilişkilendiriyo
            site.save()
            messages.success(request, "URL başarıyla kaydedildi. Admin onayı bekleniyor.")
            return redirect('scanner:scanner')
        else:
            messages.error(request, "URL kaydedilirken bir hata oluştu.")
    else:
        form = ScannerForm()

    # Kullanıcının sadece onaylanmış URL'lerini listelemek için yaptık bunu
    approved_sites = Scanner.objects.filter(user=request.user, is_approved=True)
    return render(request, 'scanner.html', {'form': form, 'approved_sites': approved_sites})

@login_required
def start_scan(request, site_id):
    site = get_object_or_404(Scanner, id=site_id, user=request.user)

    if not site.is_approved:
        messages.error(request, "Bu URL için tarama yapma izniniz yok.")
        return redirect('scanner:scanner')

    # URL'nin geçerli bir formatta olup olmadığını kontrol etmek için
    url_regex = re.compile(r'^(https?://)?([a-z0-9-]+(\.[a-z0-9-]+)+)(:[0-9]{1,5})?(/.*)?$')
    if not url_regex.match(site.url):
        messages.error(request, "Geçersiz URL formatı.")
        return redirect('scanner:scanner')

    # Tarama işlemini başlatmak için 
    try:
        # ZAP API'ye bağlanıp bağlantı durumunu kontrol et
        if hasattr(zap.core, 'version') and callable(zap.core.version):  # Fonksiyonun varlığını ve çağrılabilirliğini kontrol ettik burda
            version = zap.core.version()  # ZAP versiyonunu al
            print(f"ZAP Version: {version}")  # ZAP versiyonunu kontrol et
        else:
            print("zap.core.version is not callable or does not exist.")

        # URL'nin protokolünü kontrol et ve eksikse http ekle
        url = site.url.strip()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url  # Varsayılan olarak http:// ekle

        # URL'yi encode etmeden önce kontrol et
        encoded_url = urllib.parse.quote(url, safe=":/")  # Safe parametreye ':/' ekleyerek bu karakterlerin encode edilmemesini sağlıyoruz

     
        zap.urlopen(encoded_url)  # Hedef URL'yi açmak iiçin
        scan_id = zap.ascan.scan(encoded_url)

        # Tarama işleminin tamamlanmasını bekle
        max_wait_time = 600  # Maksimum bekleme süresi ( 10 dakika)
        elapsed_time = 0
        while int(zap.ascan.status(scan_id)) < 100 and elapsed_time < max_wait_time:
            time.sleep(5)
            elapsed_time += 5

            if elapsed_time >= max_wait_time:
                messages.error(request, "Tarama çok uzun sürdü ve zaman aşımına uğradı.")
                return redirect('scanner:scanner')

        # Tarama sonuçlarını almak için
        scan_results = zap.core.alerts(baseurl=site.url)

        if not scan_results:
            messages.error(request, f"{site.url} için tarama sonucu bulunamadı.")
            return redirect('scanner:scanner')
        
        # JSON verisini string'e dönüştürür ve kaydeder
        site.results = json.dumps(scan_results)  # JSON verisini string olarak kaydeder burda
        site.save()

        messages.success(request, f"Tarama tamamlandı: {site.url}")
    except Exception as e:
        messages.error(request, f"Tarama sırasında bir hata oluştu: {str(e)}")

    return redirect('scanner:scan_results', site_id=site.id)

@login_required
def scan_results(request, site_id):
    site = get_object_or_404(Scanner, id=site_id, user=request.user)

    # Eğer sonuç yoksa, kullanıcıya daha anlamlı bir mesaj göstermek için mesaj
    if not site.results:
        messages.error(request, f"{site.url} için tarama sonucu bulunamadı.")
        return redirect('scanner:scanner')

    try:
        # JSON verisini bir Python objesine dönüştürüp templataya aktarmak için
        scan_results = json.loads(site.results)
    except json.JSONDecodeError:
        messages.error(request, "Tarama sonuçları geçersiz formatta. Lütfen tekrar deneyin.")
        return redirect('scanner:scanner')

    return render(request, 'scanner_results.html', {'site': site, 'results': scan_results})


@staff_member_required
def approve_url(request, site_id):
    site = get_object_or_404(Scanner, id=site_id)
    site.is_approved = True
    site.save()

    messages.success(request, f"URL {site.url} başarıyla onaylandı.")
    return redirect('scanner:admin_dashboard')

@staff_member_required
def admin_dashboard(request):
    unapproved_sites = Scanner.objects.filter(is_approved=False)  # Onaylanmamış siteleri göstermek içinn
    return render(request, 'scanner/admin_dashboard.html', {'sites': unapproved_sites})
