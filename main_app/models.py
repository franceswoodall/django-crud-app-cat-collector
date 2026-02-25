from django.db import models
from django.urls import reverse 
from datetime import date

from django.contrib.auth.models import User

# Add the Toy model
class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toy-detail', kwargs={'pk': self.id})
        '''when we create a new toy we want the redirect to happen to the toy itself
        instead of the index page, so it basically helps us redirect - see canvas notes for more detail'''

class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy) #we rearranged toy to be at the top of the page because otherwise we can't access it 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): #if we don't write thCis we would just see a random object number
        return self.name 
    
    def get_absolute_url(self):
        return reverse('cat-detail', kwargs={'pk': self.id})
    
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
        #we are basically saying today, has the cat had three meals? 

MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Feeding(models.Model): 
    date = models.DateField()
    meal = models.CharField(
    max_length=1, 
    choices = MEALS, 
    default=MEALS[0][0])

    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"
    
    class Meta: 
        ordering = ['-date']
    
