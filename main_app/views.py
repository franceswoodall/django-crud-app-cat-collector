from django.shortcuts import render
from .models import Cat
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# Create your views here.
def home(request):
    return render(request, 'home.html')

#about view
#request is an argument that render needs - it's an arg 
#we always write request not req in our functions
#django knows if you use django template language (which is our about.html) 
# it knows where to look i.e. within templates file
#the second argument is alwasy the file it is rendering and must be in the same app folder

def about(request):
    return render(request, 'about.html') 

#replaced by class-based view below
# def cat_index(request):
#     cats = Cat.objects.all()
#     return render(request, 'cats/index.html', {'cats': cats})

class CatList(ListView): 
    model = Cat 

#replaced by class-based view below
# def cat_detail(request, cat_id):
#     cat = Cat.objects.get(id=cat_id)
#     return render(request, 'cats/details.html', { 'cat': cat})

class CatDetail(DetailView): 
    model = Cat 

class CatCreate(CreateView):
    model = Cat 
    fields = '__all__' #this means i want all the fields on my model to be in the form 

class CatUpdate(UpdateView): 
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = reverse_lazy('cat-index')