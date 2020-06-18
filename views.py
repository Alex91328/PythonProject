from django.shortcuts import render, redirect
from django.contrib import messages
from . models import User, Message, Comment, Author
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        password=request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        created_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        user = User.objects.get(email=request.POST['email'])
        if user:
            request.session['User_Id'] = user.id   
            return redirect("/quotes")


def login(request):
    errors = User.objects.login_validator(request.POST)
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['User_Id']=logged_user.id
            return redirect("/quotes")
    else:  
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        return redirect("/")

def quotes(request):
    if 'User_Id' not in request.session:
        return redirect("/") 
    context = {
        'user': User.objects.get(id = request.session['User_Id']),
        "all_the_authors": Author.objects.all()
    }
    return render(request, "success.html", context)

def logout(request):
    if 'User_Id' not in request.session:
        return redirect("/")
    else:
        del request.session['User_Id']
    return redirect('/')

def edit(request, user_id):
    context = {
        "user" : User.objects.get(id=user_id)
    }
    return render(request ,"wall.html", context)

def update(request, user_id):
    errors = User.objects.edit_account_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/myaccount/{user_id}")
    user_to_update = User.objects.get(id=user_id)
    user_to_update.first_name = request.POST['first_name']
    user_to_update.last_name = request.POST['last_name']
    user_to_update.email = request.POST['email']
    user_to_update.save()
    messages.success(request, "User successfully updated")
    return redirect(f"/myaccount/{user_id}")

def post_message(request):
    Author.objects.create(author=request.POST['author'],quote=request.POST['quote'], user=User.objects.get(id=request.session['User_Id']))
    return redirect('/quotes')

def user(request, author_id):
    context = {
        'all_authors_quotes' : Author.objects.all(),
        "author" : Author.objects.get(id=author_id)
        
    }
    return render(request, "user.html", context)

def delete(request,author_id):
    message_to_delete = Author.objects.get(id=author_id)
    message_to_delete.delete()
    return redirect('/quotes')


