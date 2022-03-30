from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from datetime import datetime
from django.contrib.auth import logout, authenticate, login
from .models import CustomUser, Staffs, Students, AdminHOD, Contact, Feedback, Courses, SessionYearModel
from django.contrib import messages
import json
import requests
import os

import datetime

from UMS_app import forms

# Create your views here.


def index(request):
    return render(request, 'index.html')


def feedback(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        experience = request.POST.get('experience')
        comments = request.POST.get('comments')
        feedback = Feedback(uname=uname, email=email, experience=experience,
                            comments=comments, date=datetime.today())
        feedback.save()
        messages.success(request, 'Your feedback has been recorded!')

    return render(request, 'feedback.html')


def logi(request):
    return render(request, 'login.html')


def signup(request):
    courses = Courses.objects.all()
    session_years = SessionYearModel.object.all()
    return render(request, 'register.html', {"courses": courses, "session_years": session_years})


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Invalid Method</h2>")
    else:
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "6Lf5hgAdAAAAAD6LBGcCr5r2F-Fx2BSGwcBsDS-6"
        cap_data = {"secret": cap_secret, "response": captcha_token}
        cap_server_response = requests.post(url=cap_url, data=cap_data)
        cap_json = json.loads(cap_server_response.text)

    if cap_json['success'] == False:
        messages.error(request, "Invalid Captcha Try Again")
        return HttpResponseRedirect("/")

    print("here")
    email_id = request.POST.get('email')
    password = request.POST.get('password')
    #user_type = request.POST.get('user_type')
    print(email_id)
    print(password)
    print(request.user)
    if not (email_id and password):
        messages.error(request, "Please provide all the details!!")
        return render(request, 'login.html')

    user = CustomUser.objects.filter(email=email_id, password=password).last()
    if not user:
        messages.error(request, 'Invalid Login Credentials!!')
        return render(request, 'login.html')

    login(request, user)
    print("user is")
    print(request.user)
    print(user.user_type)

    if user.user_type == '3':
        return redirect('student_home1/')
    elif user.user_type == '2':
        return redirect('staff_home1/')
    elif user.user_type == '1':
        return redirect('admin_home/')


def dosignup(request):
    first_name = request.POST.get('firstname')
    last_name = request.POST.get('lastname')
    email_id = request.POST.get('email')
    role = request.POST.get('role')
    password = request.POST.get('password')
    confirm_password = request.POST.get('cpassword')
    if role == 'student' or role == 'staff':
        address = request.POST.get('address')
    if role == 'student':
        session_year_id = request.POST.get('session_year')
        course_id = request.POST.get('course')
        gender = request.POST.get('gender')

    print(email_id)
    print(password)
    print(confirm_password)
    print(first_name)
    print(last_name)
    if not (email_id and password and confirm_password):
        messages.error(request, 'Please provide all the details!!')
        return render(request, 'register.html')

    if password != confirm_password:
        messages.error(request, 'Both passwords should match!!')
        return render(request, 'register.html')

    is_user_exists = CustomUser.objects.filter(email=email_id).exists()

    if is_user_exists:
        messages.error(
            request, 'User with this email id already exists. Please proceed to login!!')
        return render(request, 'register.html')

    user_type = get_user_type_from_email(email_id)

    if user_type is None:
        messages.error(
            request, "Please use valid format for the email id: '<username>.<staff|student|hod>@<college_domain>'")
        return render(request, 'register.html')

    username = email_id.split('@')[0].split('.')[0]

    if CustomUser.objects.filter(username=username).exists():
        messages.error(
            request, 'User with this username already exists. Please use different username')
        return render(request, 'register.html')

    if user_type == '2':
        user = CustomUser(user_type=2)
        user.username = username
        user.email = email_id
        user.role = role
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        Staffs.objects.create(admin=user, address=address)
    elif user_type == '3':
        user = CustomUser(user_type=3)
        user.username = username
        user.email = email_id
        user.role = role
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        Students.objects.create(admin=user, gender=gender, address=address, course_id=Courses.objects.get(
            id=course_id), session_year_id=SessionYearModel.object.get(id=session_year_id))
    elif user_type == '1':
        user = CustomUser(user_type=1)
        user.username = username
        user.email = email_id
        user.role = role
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        AdminHOD.objects.create(admin=user)
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


def get_user_type_from_email(email_id):

    try:
        email_id = email_id.split('@')[0]
        email_user_type = email_id.split('.')[1]
        return CustomUser.EMAIL_TO_USER_TYPE_MAP[email_user_type]
    except:
        return None


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name=name, email=email, phone=phone,
                          desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!')

    return render(request, 'contact.html')