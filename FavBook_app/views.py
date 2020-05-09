from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
import bcrypt
from django.contrib.auth.models import AnonymousUser


def index(request):
    users = User.objects.all()
    context = {
        "all_users": users
    }
    return render(request, "index.html", context)

def successDisplay(request, user_Val):
    users = User.objects.get(id = user_Val)
    other_users = User.objects.all()
    books = Book.objects.all()
    if "user" not in request.session:
        return redirect("/")
    context = {
        "create_user": users,
        "all_books": books,
        "more_users" : other_users,
    }
    return render(request, "success.html", context)

def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    password = request.POST['type_password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
    print(pw_hash) 
    
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        # print("*"*50, "\n", errors)
        return redirect("/")
    else:
        newUser = User.objects.create(first_name = request.POST["type_first_name"], 
        last_name = request.POST["type_last_name"], email = request.POST["type_email"],
        password = pw_hash)

        user_Val = newUser.id
        return redirect(f"/success/{user_Val}")

def validate_login(request):
    user = User.objects.filter(email=request.POST['type_login_email']) 
    print(user)
    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['type_login_password'].encode(), logged_user.password.encode()):
            request.session["user"] = logged_user.email
            print("password match")
            return redirect("/success/{}".format(logged_user.id))
        else:
            print("failed password")
            messages.error(request, "Invalid password")
            return redirect("/")
    messages.error(request, "No account associated to email")
    print ("No account associated to email")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

def myBookPage(request, book_val):
    users = User.objects.get(id = user_Val)
    users_like_books = Book.objects.all()
    users_books = Book.objects.get(id = users)

    context = {
        "theUsers": users,
        "LikeBooks": users_like_books,
    }

    users_books.title = request.POST["update_title"]
    users_books.desc = request.POST["update_desc"]
    users_books.save()

    return render(request, "editpage.html", context)

def deleteMyPage(request, got_val):
    delPage = Book.objects.get(id = got_val)
    delPage.delete()
    return redirect('/')

    