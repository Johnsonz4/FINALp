from django.shortcuts import render, redirect
from django.contrib import messages

from travel_planner.tokens import account_activation_token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from io import BytesIO
import sys
from django.core.files import File
from PIL import Image, ImageDraw
import os
from django.utils.crypto import get_random_string
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.encoding import force_bytes
from .models import *
from django.utils.encoding import force_str
from django.core.mail import send_mail
from django.db.models import Q
import re
from django.contrib.auth import get_user_model
from datetime import datetime, date
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import json
from django.utils.safestring import mark_safe, SafeText, SafeData
from django.utils.encoding import force_str
import random
from datetime import datetime, timedelta, timezone
from django.http import JsonResponse
from travel_planner.settings import EMAIL_HOST_USER
from time import sleep


def dashboard(request):
    if request.user.is_authenticated:
        travel_plans = TravelPlan.objects.filter(user = request.user)
        context = {
            'travel_plans': travel_plans
        }
        return render(request, 'planner/dashboard.html',context)
    else:
        return redirect("planner:index")


def index(request):
    if request.user.is_authenticated:
        return redirect("planner:dashboard")
    else:
        return render(request, 'planner/index.html')


def register(request):
    if request.method == 'POST' and not request.user.is_authenticated:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email_address")
        password = request.POST.get("password1")
        users = User.objects.filter(email__iexact=email)
        if users.count() > 0:
            error_msg = "user with that email already exists,kindly enter another email address."
            return render(request, 'planner/register.html',
                            {'error_msg': error_msg})
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=email,
                                                    password=password)
            user.is_active = True
            user.save()

            return render(request, 'planner/registration_successful.html')

    elif request.user.is_authenticated:
        return redirect("planner:dashboard")

    else:
        return render(request, 'planner/register.html')


def login_user(request):
    if request.method == "POST" and not request.user.is_authenticated:
        email = request.POST.get('email_address')
        password = request.POST.get('password')
        try:
            username =User.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                
                return redirect("planner:dashboard")
            
            else:
                return render(request, 'planner/login.html', {"error_msg": "incorrect username or password"})
        except:
            return render(request, 'planner/login.html', {"error_msg": "incorrect username or password"})
    else:
        return render(request, 'planner/login.html')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'planner/profile.html')
    else:
        return redirect("planner:login_user")


def logout_user(request):
    logout(request)
    request.session.clear()
    return redirect('planner:index')


def travel_plan(request, id):
    if request.user.is_authenticated:
        try:
            travel_plan = TravelPlan.objects.get(id = int(id))
            context = {
                'travel_plan':travel_plan,
            }
            return render(request, 'planner/travel_plan.html', context)
        except:
            return redirect("planner:index")
        

def about_us(request):
    return render(request, 'planner/about_us.html')


def contact_us(request):
    return render(request, 'planner/contact_us.html')




def create_travel_plan(request):
    if request.user.is_authenticated:
        try:
            title = request.POST.get("title")
            destination = request.POST.get('destination')
            travel_datetime = request.POST.get('travel_datetime')

            travel_plan = TravelPlan.objects.create(
                user = request.user,
                title = title,
                destination = destination,
                travel_datetime = travel_datetime
            )

            travel_plan.save()

            data = {
                'successful': 'yes',
                'travel_plan_id': travel_plan.id,
            }
            return JsonResponse(data)

        except:
            data = {
                'successful': 'no',
                'travel_plan_id': ''
            }
            return JsonResponse(data)



def add_travel_plan_item(request):
    if request.user.is_authenticated:
        try:
            travel_plan_id = request.POST.get("travel_plan_id")
            name = request.POST.get('name')
            description = request.POST.get('description')

            travel_item = TravelItem.objects.create(
                name = name,
                description = description,
            )

            travel_item.save()

            travel_plan = TravelPlan.objects.get(id = int(travel_plan_id))
            travel_plan.travel_items.add(travel_item)

            data = {
                'successful': 'yes',
                'travel_item_id': travel_item.id,
            }
            return JsonResponse(data)

        except:
            data = {
                'successful': 'no',
                'travel_item_id': ''
            }
            return JsonResponse(data)





def delete_travel_plan_item(request):
    if request.user.is_authenticated:
        try:
            item_id = request.POST.get('travel_item_id')

            travel_item = TravelItem.objects.get(id = int(item_id))

            travel_item.delete()

            data = {
                'successful': 'yes',
                'travel_item_id': item_id,
            }
            return JsonResponse(data)

        except:
            data = {
                'successful': 'no',
                'travel_item_id': ''
            }
            return JsonResponse(data)
