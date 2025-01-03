

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()

    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username1']
        password = request.POST['password1']

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('index')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('index')
    else:
        return render(request, 'index.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('index')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            name = request.POST.get("username1")
            pwd = request.POST.get("password1")
            user = authenticate(request, username=name, password=pwd)
            print(user)

            if user is not None:
                login(request, user)
                messages.success(request, "Login successfully")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('/login')
        return render(request, "login.html")

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You registered successfull now you can login")
            return redirect('login1')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View That Page...")
        return redirect('index')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect('index')
    else:
        messages.success(request, "You Must Be Logged In To Do That...")
        return redirect('index')

# def add_record(request):
#     form = AddRecordForm(request.POST or None)
#     if request.user.is_authenticated:
#         if request.method == "POST":
#             if form.is_valid():
#                 add_record = form.save()
#                 messages.success(request, "Record Added...")
#                 return redirect('home')
#         return render(request, 'add_record.html', {'form': form})
#     else:
#         messages.success(request, "You Must Be Logged In...")
#         return redirect('home

from django.utils import timezone

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                # Add the current date and time to the record in the correct timezone
                record = form.save(commit=False)
                record.created_at = timezone.localtime(timezone.now())  # Convert to local time (Asia/Kolkata)
                print("Record Created At (local time):", record.created_at)  # To check the local time
                record.save()

                messages.success(request, "Record Added...")
                return redirect('index')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.error(request, "You Must Be Logged In...")
        return redirect('index')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('index')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('index')