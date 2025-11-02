from django.shortcuts import render
from rest_framework import generics
from basic_api.models import DRFPost
from basic_api.serializers import DRFPostSerializer
from basic_api.models import dosen
from basic_api.serializers import dosenSerializer
from basic_api.models import mahasiswa
from basic_api.serializers import mahasiswaSerializer
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from basic_api.forms import DRFPostForm



# Create your views here.
class API_objects(generics.ListCreateAPIView):
    queryset = DRFPost.objects.all()
    serializer_class = DRFPostSerializer

class API_objects_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DRFPost.objects.all()
    serializer_class = DRFPostSerializer

class dosen_objects(generics.ListCreateAPIView):
    queryset = dosen.objects.all()
    serializer_class = dosenSerializer

class dosen_objects_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = dosen.objects.all()
    serializer_class = dosenSerializer

class mahasiswa_objects(generics.ListCreateAPIView):
    queryset = mahasiswa.objects.all()
    serializer_class = mahasiswaSerializer

class mahasiswa_objects_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = mahasiswa.objects.all()
    serializer_class = mahasiswaSerializer

def list_buku(request):
    list_buku = DRFPost.objects.all()
    print("Lihat data buku :")
    print(list_buku)
    data = {"list_buku": list_buku}
    return render(request, "card.html", data)


def edit_buku(request, id):
    obj = get_object_or_404(DRFPost, id=id)
    print(obj)
    form = DRFPostForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("list-buku"))
    context = {}
    context['form'] = form
    return render(request, "editpage.html", context)

def create_buku(request):
    if request.method == 'POST':
        form = DRFPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('list-buku'))
    else:
        form = DRFPostForm()

    context = {'form': form}
    return render(request, 'create.html', context)

