from django.shortcuts import render
from apps.base.models import Index, About_us, Image
# Create your views here.

def index(request):
    about_all = About_us.objects.all()
    image_id = Image.objects.latest('id')
    index = Index.objects.latest('id')
    return render(request, "index.html", locals())