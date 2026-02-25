from django.shortcuts import render, redirect
from .models import Cat, Toy
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import FeedingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.


class Home(LoginView):
    template_name = 'home.html' 

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #for now get mw what i have
        toys_cat_doesnt_have = Toy.objects.exclude(id__in = self.object.toys.all().values_list('id'))
        #id__in is built in to Django & Python that helps us work with many to many relationships
        #object in this instance is Cat
        #values list is a function that turns things into a list
        context['feeding_form']= FeedingForm()
        context['toys'] = toys_cat_doesnt_have
        return context 

class CatCreate(CreateView):
    model = Cat 
    fields = ['name', 'breed', 'description', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form) #super is parent inheritance class 

class CatUpdate(UpdateView): 
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = reverse_lazy('cat-index')

def add_feeding(request, pk):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = pk
        new_feeding.save()
    return redirect('cat-detail', pk=pk )

class ToyCreate(CreateView): 
    model = Toy
    fields = '__all__'

class ToyList(ListView): 
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = reverse_lazy('toy-index')

def associate_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('cat-detail', pk=cat_id)

def remove_toy(request, cat_id, toy_id): 
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('cat-detail', pk=cat_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cat-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
  