import json

from django.http.response import JsonResponse
from django.views         import View

from users.decorators import login_decorator
from .models          import Post


class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            title   = data['title']
            content = data['content']

            post = Post.objects.create(
                author  = user.name,
                title   = title,
                content = content,
                user    = user
            )

            result = {
                'author'     : post.author,
                'title'      : post.title,
                'content'    : post.content,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }

            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : result},status = 201)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)

    def get(self,request,post_id):
        if not Post.objects.filter(id = post_id).exists():
            return JsonResponse({'MESSAGE' : 'DOSE_NOT_EXIST_POST'}, status = 404)

        post = Post.objects.get(id = post_id)

        result = {
                'author'     : post.author,
                'title'      : post.title,
                'content'    : post.content,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return JsonResponse({"RESULT" : result}, status = 200)
    
    @login_decorator
    def delete(self, request, post_id):
        if not Post.objects.filter(id = post_id).exists():
            return JsonResponse({"MESSAGE" : "DOSE_NOT_EXIST_POST"}, status = 404)
        if Post.objects.get(id = post_id).user.id != request.user.id:
            return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 403)

        Post.objects.filter(id = post_id).delete()

        return JsonResponse({"MESSAGE" : "DELETED"}, status = 200)

    @login_decorator
    def put(self, request, post_id):
        try:
            data    = json.loads(request.body)
            title   = data['title']
            content = data['content']

            if not Post.objects.filter(id = post_id).exists():
                return JsonResponse({"MESSAGE" : "DOSE_NOT_EXIST_POST"}, status = 404)
            if Post.objects.get(id = post_id).user.id != request.user.id:
                return JsonResponse({"MESSAGE" : "NO_PERMISSION"}, status = 401)

            post = Post.objects.filter(id = post_id).update(
                title   = title,
                content = content
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status = 400)

class PostListView(View):
    def get(self,request):
        try:
            offset = int(request.GET.get('offset', 0))
            limit  = int(request.GET.get('limit', 5))
            
            posts = Post.objects.all()[offset:offset+limit]
            count = len(posts)
            
            result = [{
                'author'     : post.user.name,
                'title'      : post.title,
                'content'    : post.content,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }for post in posts]

            return JsonResponse({ "count" : count, "RESULT" : result}, status = 200)

        except ValueError:
            return JsonResponse({'MESSAGE' : 'NOT_INT'}, status = 400)