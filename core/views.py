from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
import requests

class PostAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        return Response([self.formatPost(p) for p in posts])

    def formatPost(self, post):
        comments = requests.get('http://127.0.0.1:8081/api/posts/%d/comments' % post.id).json()
        return {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'comments': comments
        }

    def post(self, request):
        serializer = PostSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)
