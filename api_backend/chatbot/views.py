# chatbot/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
from openai import OpenAI
import os
import logging
import time
from dotenv import load_dotenv
from django.views.generic import TemplateView

load_dotenv()
# Configure logging
logger = logging.getLogger(__name__)


class HomeTemplateView(TemplateView):
    template_name = 'home.html'
        
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
            api_key = os.getenv('OPENAI_API_KEY')
            print(f"API Key: {api_key}")

            if not api_key:
                logger.error("API Key not found. Please check your .env file.")
                return Response(
                    {'error': 'API Key not found.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
            client = OpenAI(
                api_key=api_key,
            )

            # Call GPT-4 API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                max_tokens=150,
                n=1,
                temperature=0.7,
            )

            ai_answer = response.choices[0].message.content

            # Map response to Manychat's custom fields
            manychat_response = {
                "set_field_values": {
                    "AI Answer": ai_answer
                }
            }

            end_time = time.time()
            logger.info(f"Response time: {end_time - start_time} seconds")

            return Response(manychat_response, status=status.HTTP_200_OK)
        
        except openai.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        except openai.RateLimitError as e:
            print("A 429 status code was received; we should back off a bit.")
        except openai.APIStatusError as e:
            print("Another non-200-range status code was received")
            print(e.status_code)
            print(e.response)
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}")
            return Response(
                {'error': 'Internal server error.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
