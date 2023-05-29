from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import ProductSerializers
from .models import Items
# Create your views here.

@api_view(["GET"])
def api_Overview(req):
    over_view ={
        'list_all':'all/'
    }
    return Response({"message":"Api Works","data":over_view})

@api_view(["GET"])
def get_all(req):
    products = Items.objects.all()
    serializer = ProductSerializers(products,many=True)
    print(serializer)
    return Response(serializer.data)

@api_view(["POST"])
def createItem(req):
    user = ProductSerializers(data=req.data)

    if user.is_valid():
        user.save()

    return Response({"message":"User Create SuccessFully"},status=status.HTTP_201_CREATED)

@api_view(['POST'])
def updateItem(req,pk):
    item = Items.objects.get(id=pk)
    itemSerializer = ProductSerializers(instance=item,data=req.data)

    if itemSerializer.is_valid():
        itemSerializer.save()
        return Response(itemSerializer.data)
    
