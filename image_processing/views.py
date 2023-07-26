from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser

from image_processing.service import count_people

# Create your views here.

@api_view(['POST'])
def detect_people(request):
    try:
        image_data = request.body
        response = count_people(image_data)
        return JsonResponse({'num_people': response})
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)