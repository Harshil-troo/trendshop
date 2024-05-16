from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

def home(request):
    return render(request, 'website.html')

def become_seller(request):

    return render(request, 'become_seller.html')