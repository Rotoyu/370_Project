from django.db import models
from django.contrib.auth.models import User
import base64
import os

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    encrypted_content = models.BinaryField()
    key = models.BinaryField()  # Add this field to store the key
    timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_key():
        return base64.urlsafe_b64encode(os.urandom(32))

    @staticmethod
    def encrypt_message(message):
        key = Message.generate_key()
        encrypted = base64.urlsafe_b64encode(message.encode())
        return encrypted, key

    @staticmethod
    def decrypt_message(encrypted_message, key):
        return base64.urlsafe_b64decode(encrypted_message).decode()
