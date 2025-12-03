from django.http import JsonResponse
from django.shortcuts import render
import json, random, time
from db_mongo import rutas_col  

def home(request):
    return render(request, "index.html")

def generar_ruta(locaciones, pedido_id):
    inicio_proceso = time.perf_counter()
    time.sleep(random.uniform(0.05, 0.35))
    random.shuffle(locaciones) #Crea una ruta aleatoria
    ruta = ["Dock de Recepción"] + locaciones + ["Zona de Empaque"] #Calcula la distancia recorrida recolectando todos los items
    distancia_base = 80  # recorrido mínimo desde dock + empaque
    distancia_por_item = random.uniform(15, 55)  # metros promedio aprx por desplazamiento entrre items
    distancia_m = round(distancia_base + len(locaciones) * distancia_por_item, 2)
    tiempo_caminar_seg = round(distancia_m / 1.4, 2) # Tiempo caminando aprox
    tiempo_picking_seg = sum(random.randint(3, 9) for i in locaciones) #Tiempo aprox de recoleccion por pedido
    tiempo_total_seg = round(tiempo_caminar_seg + tiempo_picking_seg, 2) #Tiempo total de recorrido
    tiempo_total_min = round(tiempo_total_seg / 60, 2)
    fin_proceso = time.perf_counter()
    proceso_ms = round((fin_proceso - inicio_proceso) * 1000, 2) #Tiempo de calco de ruta

    resultado = {
        "pedido_id": pedido_id,
        "ruta": ruta,
        "distancia_m": distancia_m,
        "tiempo_caminar_seg": tiempo_caminar_seg,
        "tiempo_picking_seg": tiempo_picking_seg,
        "tiempo_total_seg": tiempo_total_seg,
        "tiempo_total_min": tiempo_total_min,
        "proceso_ruta_ms": proceso_ms, 
        "proceso_ruta_seg": round(proceso_ms / 1000, 4),
        "items_recogidos": len(locaciones)
    }

    return resultado

def calcular_ruta(request):
    try:
        if request.method == "POST":
            body = json.loads(request.body)
            locaciones = body.get("locaciones")
            pedido  = body.get("pedido_id")
        else:
            locaciones  = request.GET.get("locaciones")
            pedido      = request.GET.get("pedido_id")
            if locaciones:
                locaciones = json.loads(locaciones)

    except json.JSONDecodeError:
        return JsonResponse({"status": "ERROR", "mensaje": "JSON inválido"}, status=400)

    if not pedido or not locaciones or not isinstance(locaciones, list):
        return JsonResponse(
            {"status": "ERROR", "mensaje": "Debes enviar pedido_id y una lista valida de locaciones"},
            status=400
        )

    
    resultado = generar_ruta(locaciones, pedido)

    return JsonResponse({"status": "OK", "resultado": resultado})
