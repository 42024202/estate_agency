from django.shortcuts import render
from django.template import context
from .models import Estate, Category


def index(request):
    estates = Estate.objects.all()
    categories = Category.objects.all()
    return render(
            request, 
            "main/index.html",
            context={
                'estates': estates, 
                'categories': categories
                }
    )

def work_single(request):
    """Detail page"""
    return render(
            request, 
            "main/work-single.html"
    )

def all_announcenments(request):
    categories = Category.objects.all()
    estates = Estate.objects.all()
    return render(
            request, 
            "main/all_announcenments.html",
            context={
                'categories': categories,
                'estates': estates
                }
    )
