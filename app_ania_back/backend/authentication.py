from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import exceptions

class CookieJWTAuthentication(JWTAuthentication) :
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            return None
        
        try :
            validated_token = self.get_validated_token(access_token)
        
        except Exception : 
            raise exceptions.AuthenticationFailed("Invalid or expired token")
        
        user = self.get_user(validated_token)

        if user is None : 
            raise exceptions.AuthenticationFailed("User no found")
        
        return (user, validated_token)