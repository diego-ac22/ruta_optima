from django.http import JsonResponse
from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def calcular_ruta(request):
    return JsonResponse({"status": "OK", "mensaje": "Servicio de ruta funcionando"})
