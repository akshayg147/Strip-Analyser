from django.shortcuts import render
from django.http import JsonResponse
from .utils import process_image
import json
# Create your views here.

def home(request):
    return render(request,'index.html')

def process_image_view(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image_file')
        image_data = image_file.read()
        result = process_image(image_data)
        print(result)
        # return render(request, 'index.html', {'result': result})
        return JsonResponse(result,safe=False)
    else:
        print('error')