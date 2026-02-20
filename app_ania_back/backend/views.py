from dotenv import load_dotenv
from django.shortcuts import render, redirect
import os
import urllib.parse
from django.conf import settings
import requests
from .models import User, Guild, GuildRolePermission
from django.http import JsonResponse
from rest_framework.response import Response 
from rest_framework import status
from rest_framework.decorators import api_view
load_dotenv()
# Create your views here.
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")

def discord_login(request) :
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "identify email guilds",
    }

    url = "http://discord.com/api/oauth2/authorize?" + urllib.parse.urlencode(params)
    print("Url Discord générée: ", url)
    return redirect(url)

def discord_callback(request):
    code = request.GET.get("code")

    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)
    #On renseigne les données données pour la requête
    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.DISCORD_REDIRECT_URI,
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    #On fait la requête
    token_response = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers=headers
    )

    print("Status code:", token_response.status_code)
    print("Response:", token_response.text)

    if token_response.status_code != 200:
        return JsonResponse({"error": "Token exchange failed"}, status=400)

    token_json = token_response.json()
    access_token = token_json.get("access_token")

    #On récupère les info de l'utilisateur
    user_url = "https://discord.com/api/users/@me"

   #On fait la demande
    user_response = requests.get(
        #On inclut l'url et le access_token
        user_url,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    #Si user_response n'est pas bon on renvoi un message d'erreur
    if user_response.status_code != 200 :
        return JsonResponse({"error" : "Failed to fetch user"}, status=status.HTTP_400_BAD_REQUEST)
    
    #On lis les données reçus
    user_data = user_response.json()

    #On créer l'objet user
    avatar_hash = user_data.get("avatar")
    avatar_url = None

    if avatar_hash:
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{avatar_hash}.png"

    user, created = User.objects.update_or_create(
        discord_id=user_data["id"],
        defaults={
            "username": user_data["username"],
            "avatar_url": avatar_url,
            "is_active": True
        }
    )
    print("Utilisateur reçu :", user_data)

    return JsonResponse({
        "id": user.discord_id,
        "username": user.username,
        "avatar_url": user.avatar_url
    })
    
    
@api_view(["POST"])
def check_permission(request):
    guild_id = request.data.get("guild_id")
    role_ids = request.data.get("role_ids", [])
    permission_code = request.data.get("permission")

    if not guild_id or not permission_code:
        return Response({"allowed": False})

    has_permission = GuildRolePermission.objects.filter(
        guild__guild_id=guild_id,
        role_id__in=role_ids,
        permissions__code=permission_code
    ).exists()

    return Response({"allowed": has_permission})

