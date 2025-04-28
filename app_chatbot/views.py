from django.shortcuts import render

def chat_view(request):
    return render(request, 'app_chatbot/chat_widget.html')