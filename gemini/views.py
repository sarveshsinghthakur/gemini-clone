from django.shortcuts import render
import google.generativeai as genai
from .models import Conversation
from django.http import JsonResponse

# Configure Google Generative AI
genai.configure(api_key="AIzaSyAjCMCnYKjxBYlaZy0cSsqv33yp5lhKTPM")

# Select the model
model = genai.GenerativeModel('gemini-1.5-flash')

def clear_conversation(request):
    if request.method == 'POST':
        # Delete all messages in the conversation
        Conversation.objects.all().delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "failed"}, status=400)

def chat(request):
    bot_response = ""
    user_message = ""

    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        if user_message:
            # Generate a response from the model
            response = model.generate_content([user_message])
            bot_response = response.text

            # Save the conversation in the database
            Conversation.objects.create(user_message=user_message, bot_response=bot_response)

    # Retrieve the conversation history
    conversation_history = []
    for convo in Conversation.objects.all().order_by('timestamp'):
        conversation_history.append({
            'text': convo.user_message,
            'is_user': True
        })
        conversation_history.append({
            'text': convo.bot_response,
            'is_user': False
        })

    return render(request, "chat.html", {
        'conversation_history': conversation_history
    })
