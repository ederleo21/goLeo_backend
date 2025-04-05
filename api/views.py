from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.apps import apps
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import json

# Api de usuario, todo sobre usuario y permisos
User = get_user_model()

#Maneja el crear un usuario
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

#Traer toda la infromacion del usuario
class UserProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        
        models = [
            {'app_label': 'core', 'model_name': 'club'},
            {'app_label': 'core', 'model_name': 'player'},
            {'app_label': 'core', 'model_name': 'playerskill'},
            {'app_label': 'tournaments', 'model_name': 'tournament'},
            {'app_label': 'tournaments', 'model_name': 'match'},
            {'app_label': 'performance', 'model_name': 'playerstatistics'},
        ]

        # Obtener los datos del usuario
        user_data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'dni': user.dni,
            'phone': user.phone,
            'address': user.address,
            'image': request.build_absolute_uri(user.image.url) if user.image else None,
        }

        # Obtener los permisos del usuario
        permissions = {}
        for model in models:
            app_label = model['app_label']
            model_name = model['model_name']
            try:
                model_class = apps.get_model(app_label, model_name)
                for perm in ['add', 'change', 'delete', 'view']:
                    perm_name = f'{app_label}.{perm}_{model_name}'
                    if user.has_perm(perm_name):
                        permissions[f'{perm}_{model_name}'] = True
            except LookupError:
                pass

        # Obtener los grupos del usuario
        groups = user.groups.all()
        group_names = [group.name for group in groups]

        # Devolver toda su información
        data = {
            'user': user_data,
            'permissions': permissions,
            'groups': group_names
        }

        return Response(data)


@csrf_exempt
def send_contact_email(request):

    if request.method == "POST":
        print(request.body)
        try:
            data = json.loads(request.body)
            user_name = data.get("userName")
            user_email = data.get("userEmail")
            user_message = data.get("userMessage")
            
            send_mail(
                subject=f"New Contact Form Submission from {user_name}",
                message=f"Name: {user_name}\nEmail: {user_email}\n\nMessage:\n{user_message}",
                from_email="ederordonez10@gmail.com",
                recipient_list=["ederordonez10@gmail.com"],  
                fail_silently=False,
            )
            return JsonResponse({"message": "Email sent successfully"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    return JsonResponse({"error": "Invalid request"}, status=400)





