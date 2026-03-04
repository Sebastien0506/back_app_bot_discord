from rest_framework import serializers
from app_ania_back.backend.models import Message, Channel
import html

class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ["content"]

    def validate_content(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError("Message vide")

        if "http://" in value or "https://" in value:
            raise serializers.ValidationError("Les liens ne sont pas autorisés")

        return html.escape(value)
    
class ChannelSerializer(serializers.ModelSerializer) :
    class Meta : 
        model = Channel
        fields = ["name"]

    def validate_content(self, value) :
        value = value.strip()

        if not value :
            return serializers.ValidationError("Aucune donnée dans la base de données.")
        
        return html.escape(value)
    
        
    