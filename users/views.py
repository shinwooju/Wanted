import json
import re
import jwt
import bcrypt

from django.http  import JsonResponse
from django.views import View

from wanted.settings import SECRET_KEY
from .models         import User


class SignUpView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            name           = data['name']
            email          = data['email']
            password       = data['password']
            check_password = data['check_password']
            regex_email    = re.compile('^[a-zA-Z\d+-_.]+@[a-zA-Z\d]+\.[a-zA-Z\d+-.]+$')
            regex_password = re.compile('^(?=.*[a-zA-Z])(?=.*[\d])(?=.*[~!@#$%^&*_+])[a-zA-Z\d~!@#$%^&*_+]{8,}$')

            if not (name and email and password and check_password):
                return JsonResponse({'MESSAGE' : 'EMPTY_VALUE'}, status = 400)

            if not regex_email.match(email):
                return JsonResponse({'MESSAGE' : 'EMAIL_VALIDATION'}, status = 400)

            if not regex_password.match(password):
                return JsonResponse({'MESSAGE' : 'PASSWORD_VALIDATION'}, status = 400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE' : 'ALREADY_EXISTED_EAMIL'}, status = 400)

            if not password == check_password:
                return JsonResponse({'MESSAGE' : 'PASSWORD_NOT_CORRECT'}, status = 400)

            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            user = User.objects.create(
                name     = name,
                email    = email,
                password = hashed_password,
                )

            print(user.password)

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not (email and password):
                return JsonResponse({'MESSAGE' : 'EMPTY_VALUE'}, status = 400)
                
            if not User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE' : 'USER_DOES_NOT_EXIST'}, status = 401)
            
            user = User.objects.get(email = email)
                
            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status = 401)

            token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = 'HS256')
            
            return JsonResponse({'MESSAGE' : 'SUCCESS', 'TOKEN' : token}, status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE_ERROR'}, status = 400)
