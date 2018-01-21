from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def inspect(request):
    params = {}
    params["success"] = False
    if request.method == 'POST':
        params['success'] = True
        return JsonResponse(params)
    else:
        return JsonResponse(params)