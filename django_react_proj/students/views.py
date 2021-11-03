from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.serializers import Serializer

from .models import Student
from .serializers import *

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

import csv,io

@api_view(['GET', 'POST'])
def students_list(request):
    if request.method == 'GET':
        data = Student.objects.all()

        serializer = StudentSerializer(data, context = {'request': request}, many = True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StudentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        print(serializer.errors)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def students_detail(request, pk):
    try:
        student = Student.objects.get(pk = pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = StudentSerializer(student, data = request.data, context = {'request', request})

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def import_data(excel_file):
    # try:
    data_set = excel_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    key = 0
    excel_data = list()
    for row_data in csv.reader(io_string, delimiter=';', quotechar="|"):
        
        key = key+1
        if(key == 1 or key == 2):
            continue
        
        validstatus = False
        for val in row_data:
            
            if(val is not "" and val is not ";"):
                validstatus = True
        if  not validstatus:
            break
        try:
            print("======================")
            print(row_data)
            excel_data.append(row_data)
        except Exception as e:
            print(e)
            continue

    return excel_data

def data_index(request, device_id=0):
    excel_data = import_data("D:/23.xlsx")
    print(excel_data)


