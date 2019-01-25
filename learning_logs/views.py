from django.shortcuts import render

def index(request):
    """Page"""
    return render(request, 'learning_logs/index.html')
