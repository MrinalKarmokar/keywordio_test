import json
import requests
from django.shortcuts import render
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from library.models import Book
from library.serializers import BookSerializer


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def add_book(request, *args, **kwargs):
    ''' Add a Book '''
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'msg': 'Book has been added!'
            }
            return Response(res)
        else:
            return Response(serializer.errors)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def get_book(request, *args, **kwargs):
    ''' Get all book data '''
    if request.method == 'GET':
        id = request.data.get('id')
        if id is not None:
            book_instance = Book.objects.get(id=id)
            serializer = BookSerializer(book_instance)
            return Response(serializer.data)
        else:
            book_instance = Book.objects.all()
            serializer = BookSerializer(book_instance, many=True)
            return Response(serializer.data)


@api_view(['PATCH', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_book(request, *args, **kwargs):
    ''' Update Book Records '''

    # Partial Update ----------
    if request.method == 'PATCH':
        id = request.data.get('id')
        book_instance = Book.objects.get(id=id)
        serializer = BookSerializer(
            instance=book_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {
                'msg': 'Book Data Updated!',
            }
            return Response(res)
        else:
            return Response(serializer.errors)

    # Complete Update ----------
    if request.method == 'PUT':
        id = request.data.get('id')
        book_instance = Book.objects.get(id=id)
        serializer = BookSerializer(
            instance=book_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = {
                'msg': 'Book Data Updated!',
            }
            return Response(res)
        else:
            return Response(serializer.errors)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_book(request, *args, **kwargs):
    ''' Delete a Book '''
    if request.method == 'DELETE':
        id = request.data.get('id')
        book_instance = Book.objects.get(id=id)
        book_instance.delete()
        res = {
            'msg': 'Book Deleted!'
        }
        return Response(res)


# -------------------------------------------------


def index_view(request, *args, **kwargs):

    url = 'http://127.0.0.1:8000/api/library/get-book/'
    response = requests.get(url=url)
    context = {
        'datas': response.json(),
    }

    return render(request, 'library/index.html',context)


def add_book_view(request, *args, **kwargs):

    url = 'http://127.0.0.1:8000/api/library/add-book/'
    data = {
        "title": "Book002",
        "author": "FirstName002 LastName002",
        "num_pages": 150,
        "publication": "Publication002",
        "publisher": "Publisher002" 
    }
    headers = {
        'content-type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0NzAwMDIwLCJpYXQiOjE2NTQ2ODQyODgsImp0aSI6ImMzYTMwMzA3Zjc0MjQ4YWRiZjM5ZTU4MDBjZGRkMTQwIiwidXNlcl9pZCI6M30.I_h2HNTD0_6bly6WObqNkGAWmGGJohbmd7AMf3c5nOI'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    context = {
        'datas': response,
    }

    return render(request, 'library/index.html', context)