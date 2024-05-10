# views.py

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Item
from .models import Bill
from .serializers import BillSerializer
from .serializers import ItemSerializer
from django.views.decorators.csrf import csrf_exempt
from .forms import ItemForm

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            # return JsonResponse(serializer.data, safe=False)
            return render(request, 'items.html', {'items': serializer.data})
    else:
        form = ItemForm()
    return render(request, 'additem.html', {'form': form})
    
@api_view(['GET', 'POST'])
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        
        serializer = ItemSerializer(items, many=True)
        # return JsonResponse(serializer.data, safe=False)
        return render(request, 'items.html', {'items': serializer.data})
    
    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return JsonResponse(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        item.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def generate_bill(request):
    # serializer = BillSerializer(data=request.data)
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        # Logic to calculate total cost based on selected items
        # print([float(i["price"]) for i in serializer.data])
        total_cost = sum([float(i["price"]) for i in serializer.data])
        # return JsonResponse(serializer.data, safe=False)
        return render(request, 'bill.html', {'items': total_cost})
    # return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


def calculate_total_cost(items):
    # Implement your logic to calculate total cost based on selected items
    total_cost = 0
    for item in items:
        total_cost += item['price']
    return total_cost