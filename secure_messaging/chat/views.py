from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'chat/inbox.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            content = form.cleaned_data['content']
            encrypted_content, key = Message.encrypt_message(content)
            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                encrypted_content=encrypted_content,
                key=key  # Store the key with the message
            )
            return redirect('inbox')
    else:
        form = MessageForm()
    return render(request, 'chat/send_message.html', {'form': form})

@login_required
def view_message(request, message_id):
    message = Message.objects.get(id=message_id, recipient=request.user)
    decrypted_content = Message.decrypt_message(message.encrypted_content, message.key)
    return render(request, 'chat/view_message.html', {'message': message, 'content': decrypted_content})
