from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    #return HttpResponse("<h3>Anasayfa</h3>")
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")
