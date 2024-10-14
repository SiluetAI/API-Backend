# chatbot/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
import os
import logging
import time

# Configure logging
logger = logging.getLogger(__name__)

class HomeView(APIView):
    """
    Simple Home View to confirm the API is running.
    """
    def get(self, request):
        return Response(
            {
                "message": "Welcome to the Manychat-GPT-4 Integration API!",
                "endpoints": {
                    "admin": "/admin/",
                    "Manychat Webhook": "/api/manychat_webhook/"
                },
                "status": "API is up and running."
            },
            status=status.HTTP_200_OK
        )
        
class ManychatWebhookView(APIView):
    def post(self, request):
        start_time = time.time()
        try:
            data = request.data

            # Extract required fields
            first_name = data.get('first_name')
            last_input_text = data.get('last_input_text')
            user_id = data.get('user_id')

            if not all([first_name, last_input_text, user_id]):
                logger.warning("Missing required fields.")
                return Response(
                    {'error': 'Missing required fields.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Construct GPT-4 messages
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": last_input_text}
            ]

            # Set OpenAI API key
            openai.api_key = os.getenv('OPENAI_API_KEY')

            # Call GPT-4 API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                max_tokens=150,
                n=1,
                temperature=0.7,
            )

            ai_answer = response.choices[0].message['content'].strip()

            # Map response to Manychat's custom fields
            manychat_response = {
                "set_field_values": {
                    "AI Answer": ai_answer
                }
            }

            end_time = time.time()
            logger.info(f"Response time: {end_time - start_time} seconds")

            return Response(manychat_response, status=status.HTTP_200_OK)

        except openai.APIError as oe:
            logger.error(f"OpenAI API error: {str(oe)}")
            return Response(
                {'error': 'Error communicating with OpenAI API.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return Response(
                {'error': 'Internal server error.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
