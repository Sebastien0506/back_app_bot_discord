from dotenv import load_dotenv
from django.shortcuts import render, redirect
import os
import urllib.parse
from django.conf import settings
import requests
from django.http import JsonResponse
from rest_framework import status
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

    token_response = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers=headers
    )

    print("Status code:", token_response.status_code)
    print("Response:", token_response.text)

    if token_response.status_code != 200:
        return JsonResponse({"error": "Token exchange failed"}, status=400)

    return JsonResponse(token_response.json())
