from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

# model to save the ingredients input of the user
class IngredientInput(models.Model):
    # id of the user that is saving the ingredients
    user_id = models.CharField('', max_length=500)
    # string with the ingredients
    input_string = models.CharField('', max_length=500)

# model to save the data of the Recipe selected by the user
class selectedRecipes(models.Model):
    # id of the user that is selecting the recipe
    user_id = models.CharField('', max_length=500)
    # id of the recipe from spoonacular
    api_id = models.CharField('', max_length=100)
    # title of the recipe
    title = models.CharField('', default='recipe', max_length=500)
    # url of the image of the recipe
    image = models.CharField('', default='image', max_length=500)
    # string including the used ingredients that were entered by the user
    usedIngredients = models.CharField('', default='ingredients', max_length=10000)
    # string including the additional ingredients needed for the recipe
    missedIngredients = models.CharField('', default='ingredients', max_length=10000)
