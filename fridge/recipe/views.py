from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import requests
import json
from .models import IngredientInput, selectedRecipes
from .forms import IngredientInputForm
from django.contrib import messages



# Create your views here.

# View for the about_me page
def index(request):
    return render(request, 'recipe/base.html')

# View for inserting the ingredients
@login_required(login_url='recipe:loginPage')
def ingredients(request):
    # define input form that is taking the ingredients
    form = IngredientInputForm(request.POST or None)
    # check if user has inserted input into the field
    if form.is_valid():
        current_user = request.user
        ingredient_object = IngredientInput()
        ingredient_object.input_string =  form.cleaned_data.get('input_string')
        ingredient_object.user_id = current_user.id

        # save the ingredient data into sqlite3 database (model IngredientInput)
        ingredient_object.save()
        # redirect to next page (selection of the recipe)
        response = redirect('selection/')
        return response
    # as long as no input is inserted, show the form
    return render(request, 'recipe/ingredients.html', {'form':form})

@login_required(login_url='recipe:loginPage')
def selection(request):
    # get the current user
    current_user = request.user
    # get the last inserted ingredients out of the database for the current user
    form = IngredientInput.objects.filter(user_id=current_user.id).order_by("-id")[0]
    # save the ingredient data into a string
    string_rare = form.input_string
    # delete whitespace out of string
    string_rare.replace(" ","")
    # build a list out of the strings
    form_list = string_rare.split(',')
    # sort the list
    form_list.reverse()

    # build the query string
    ingredients_request_string = form_list.pop()
    while form_list:
        element = form_list.pop()
        ingredients_request_string = ingredients_request_string + ",+" + element
    request_string = "https://api.spoonacular.com/recipes/findByIngredients?ingredients=" \
                     + ingredients_request_string +\
                     "&number=3&apiKey=595e60e99825426482565ac727c1ffb6"
    print(request_string)
    # try to get data (possible failures: wrong ingredients, no recipes found, api-limit reached)
    try:
        # get back a json file and unpack it
        response = requests.get(request_string)
        response = json.loads(response.text)

        # pop 3 recipes out of the response
        recipe1 = response.pop()
        recipe2 = response.pop()
        recipe3 = response.pop()

        # build the data that should be displayed on the website for every recipe
        # first recipe
        id1 = recipe1["id"]
        title1 = recipe1["title"]
        image1 = recipe1["image"]
        usedIngredientCount1 = recipe1["usedIngredientCount"]
        missedIngredientCount1 = recipe1["missedIngredientCount"]
        usedIngredients1 = {}
        for i in range(usedIngredientCount1):
            ingredient_list = recipe1["usedIngredients"].pop()
            usedIngredients1[ingredient_list["id"]] = ingredient_list["original"]
        missedIngredients1 = {}
        for i in range(missedIngredientCount1):
            ingredient_list = recipe1["missedIngredients"].pop()
            missedIngredients1[ingredient_list["id"]] = ingredient_list["original"]

        # second recipe
        id2 = recipe2["id"]
        title2 = recipe2["title"]
        image2 = recipe2["image"]
        usedIngredientCount2 = recipe2["usedIngredientCount"]
        missedIngredientCount2 = recipe2["missedIngredientCount"]
        usedIngredients2 = {}
        for i in range(usedIngredientCount2):
            ingredient_list = recipe2["usedIngredients"].pop()
            usedIngredients2[ingredient_list["id"]] = ingredient_list["original"]
        missedIngredients2 = {}
        for i in range(missedIngredientCount2):
            ingredient_list = recipe2["missedIngredients"].pop()
            missedIngredients2[ingredient_list["id"]] = ingredient_list["original"]

        # third recipe
        id3 = recipe3["id"]
        title3 = recipe3["title"]
        image3 = recipe3["image"]
        usedIngredientCount3 = recipe3["usedIngredientCount"]
        missedIngredientCount3 = recipe3["missedIngredientCount"]
        usedIngredients3 = {}
        for i in range(usedIngredientCount3):
            ingredient_list = recipe3["usedIngredients"].pop()
            usedIngredients3[ingredient_list["id"]] = ingredient_list["original"]
        missedIngredients3 = {}
        for i in range(missedIngredientCount3):
            ingredient_list = recipe3["missedIngredients"].pop()
            missedIngredients3[ingredient_list["id"]] = ingredient_list["original"]

        # check what recipe is selected (what button is clicked on the website)
        if request.method == 'POST':
            # selected recipe: 1
            if request.POST.get("selection1"):
                # save the data of the recipe 1 into the database in the table selectedRecipes
                recipeObject = selectedRecipes()
                recipeObject.user_id = current_user.id
                recipeObject.api_id = id1
                recipeObject.title = title1
                recipeObject.image = image1
                # save the ingredient lists as strings in the json-format
                recipeObject.missedIngredients = json.dumps(missedIngredients1)
                recipeObject.usedIngredients = json.dumps(usedIngredients1)
                recipeObject.save()
                # redirect to the recipe view
                response = redirect('/recipe/')
                return response

            # selected recipe: 2
            if request.POST.get("selection2"):
                # save the data of the recipe 2 into the database in the table selectedRecipes
                recipeObject = selectedRecipes()
                recipeObject.user_id = current_user.id
                recipeObject.api_id = id2
                recipeObject.title = title2
                recipeObject.image = image2
                # save the ingredient lists as strings in the json-format
                recipeObject.missedIngredients = json.dumps(missedIngredients2)
                recipeObject.usedIngredients = json.dumps(usedIngredients2)
                recipeObject.save()
                # redirect to the recipe view
                response = redirect('/recipe/')
                return response

            # selected recipe: 3
            if request.POST.get("selection3"):
                # save the data of the recipe 3 into the database in the table selectedRecipes
                recipeObject = selectedRecipes()
                recipeObject.user_id = current_user.id
                recipeObject.api_id = id3
                recipeObject.title = title3
                recipeObject.image = image3
                # save the ingredient lists as strings in the json-format
                recipeObject.missedIngredients = json.dumps(missedIngredients3)
                recipeObject.usedIngredients = json.dumps(usedIngredients3)
                recipeObject.save()
                # redirect to the recipe view
                response = redirect('/recipe/')
                return response

        # Return and render the view, pass the variables to the website to show the data of the 3 recipes
        return render(request, 'recipe/selection.html', {
            'id1': id1, 'title1': title1, 'image1': image1,
            'usedIngredientCount1': usedIngredientCount1, 'missedIngredientCount1': missedIngredientCount1,
            'usedIngredients1': usedIngredients1, 'missedIngredients1': missedIngredients1,
            'id2': id2, 'title2': title2, 'image2': image2,
            'usedIngredientCount2': usedIngredientCount2, 'missedIngredientCount2': missedIngredientCount2,
            'usedIngredients2': usedIngredients2, 'missedIngredients2': missedIngredients2,
            'id3': id3, 'title3': title3, 'image3': image3,
            'usedIngredientCount3': usedIngredientCount3, 'missedIngredientCount3': missedIngredientCount3,
            'usedIngredients3': usedIngredients3, 'missedIngredients3': missedIngredients3,
        })

    # if an error occurs, show the error page
    except:
        return render(request, 'recipe/error.html')

# View for showing the last selected recipe
@login_required(login_url='recipe:loginPage')
def recipe_view(request):
    # get the current user
    current_user = request.user
    # get the data of the last selected recipe out of the database (table: selectedRecipe) and save them into variables
    form = selectedRecipes.objects.filter(user_id=current_user.id).order_by("-id")[0]
    id_string = form.api_id
    title = form.title
    image = form.image
    # unpack the json strings of the ingredients
    usedIngredients = json.loads(form.usedIngredients)
    missedIngredients = json.loads(form.missedIngredients)

    # build the request string to get back the instructions for the recipes
    request_string = "https://api.spoonacular.com/recipes/" + id_string + "/analyzedInstructions?apiKey=595e60e99825426482565ac727c1ffb6"
    # unpack the returned data (json object)
    instructions_json = requests.get(request_string)
    instructions_list = json.loads(instructions_json.text)
    instructions = {}
    # build a dictionary containing the instruction and the number of the instruction
    while instructions_list:
        element = instructions_list.pop()
        steps = element["steps"]
        steps.reverse()
        while steps:
            step = steps.pop()
            instructions[step["number"]] = step["step"]

    # return the data and pass them to the website so that the instructions can be displayed
    return render(request, 'recipe/recipe.html', {
        'instructions': instructions, 'title': title, 'usedIngredients': usedIngredients,
        'missedIngredients': missedIngredients, 'image' : image,
    })

# View for the statistic page
@login_required(login_url='recipe:loginPage')
def statistics(request):
    # get the current user
    current_user = request.user
    # get the inserted ingredients and the selected recipe
    form = IngredientInput.objects.filter(user_id=current_user.id).order_by("-id")
    searched_ingredients = []
    for element in form:
        searched_ingredients.append(element.input_string)
    form = selectedRecipes.objects.filter(user_id=current_user.id).order_by("-id")
    selected_recipe = []
    for element in form:
        selected_recipe.append(element.title)
    return render(request, 'recipe/statistics.html', {'searched_ingredients': searched_ingredients,
                      'selected_recipe': selected_recipe
    })

# View for the DSGVO
def dsgvo(request):
    return render(request, 'recipe/dsgvo.html')

# View for loginPage
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect('/')
            return response
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, 'recipe/login.html')

# View for register a new user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created for the user ' + form.cleaned_data.get('username') + '! Log in now')
            response = redirect('/loginPage/')
            return response
    else:
        form = UserCreationForm()
        print('Not worked')
    return render(request, 'recipe/register.html', {'form': form})

# View for logout the User
@login_required(login_url='recipe:loginPage')
def logoutUser(request):
    logout(request)
    response = redirect('/loginPage/')
    return response