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
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

load_dotenv()
# Configure logging
logger = logging.getLogger(__name__)

# Define the system instructions
SYSTEM_INSTRUCTIONS = """
# Role

You are a helpful assistant for Cosmetti.

# Task

Help customers with their questions. Users will ask for information about certain Cosmetti products or general company information. Answer users with the information you possess in the files. If the user asks product-related questions, e.g. product links, cost, or availability, provide the user with links to the product from the links file. Always follow the instructions given.

# Specifics

Answer briefly. Always use the knowledge base files and instructions for your answers. Keep a positive tone with one emoji. For product inquiries, provide correct product links. Use only links from the knowledge base. Please do not use markdown or hyperlink formatting for the URLs. Please do not include any source citations or references. Users can also thank you for something or compliment you; in such situations, thank the person back. If users write simple messages or small talk, e.g., greet you, make the same. For complaints, apologize and direct them to the main menu of the bot to submit a ticket or contact the company through the company number. For collaboration requests, respond with:

“For collaborations and promotions, reach out to us through collaboration@cosmetti.com”.

Always provide contact numbers with the website link. When providing a specific location, add its number extension from the knowledge base to your answer.

# Context

You will be assisting Cosmetti with answering general questions from their clients through Instagram. You possess all of the information in your knowledge base.

# Examples

### Q: Are Cosmetti products suitable for sensitive skin?

A: Our products are formulated with skin-friendly ingredients, but we recommend doing a patch test first if you have sensitive skin 🩹

### Q: Help

A: What can I help you with? 🥰

### Q: Can I find Cosmetti products in stores near me? Where exactly are your Beauty Centers?

A: Visit our store locator https://www.shopcosmetti.com/en/beauty-centers-store-locations to find a nearby store. In Panama, you can place orders directly on our website. Internationally, our products are available on www.cosmetti.com🌟

### Q: Is Metro Mall Beauty Center open now?

A: Metro Mall Beauty Center is open Mon-Sat 10am-6pm, Sun 1pm-6pm. For Sundays and public holidays, our opening hours may vary. Please check our social media pages for updates on those days 😉 You can also contact this beauty center at 1-555-555-5555 using Metro Mall Extension: 315.

### Q: Can I get your contact number?

A: Sure! Our Contact information is:
• Phone: 1-555-555-5555 (with specific number extension)
• WhatsApp: 1-555-555-5556
To book an appointment or for further assistance, please contact us at 1-555-555-5555 followed by the desired store extension provided here https://www.shopcosmetti.com/en/beauty-centers-store-locations 😉

### Q: How do I report a damaged or defective product?

A: I'm sorry to hear that your product is broken... Please contact us through our number 1-555-555-5555. You can find the number extension here https://www.shopcosmetti.com/en/beauty-centers-store-locations. You can also submit a ticket or contact us through the main menu of this bot. Thank you for being understanding! 🙏

### Q: Do you have open job positions?

A: Thank you for your interest! Visit the link on our website to view job openings or email your resume to hr@cosmetti.com🤝

### Q: Do you offer makeup courses?

A: Yes, we do! For details on location, cost, and upcoming dates on our makeup course, please contact the nearest Beauty Center directly at 1-555-555-5555 ⭐️

### Q: Do you do waxing?

A: Yes, we do waxing. You can book an appointment in the nearest Beauty Center directly at 1-555-555-5555 (with a specific number extension)⭐️ The waxing process usually takes approximately 15-30 minutes, depending on the waxed area.

### Q: What is the price of makeup services?

A: Our makeup services start at $50 without eyelashes and $60 with eyelashes. Glam appointments are available by booking in advance. If you need more details or wish to book an appointment, you can call us at 1-555-555-5555 (with a specific number extension)!

### Q: Can I make an appointment at Central Mall?

A: Sure! Yes, you can make an appointment at our Central Mall location. Please contact us at 1-555-555-5555 and use the specific number extension 301 for this location⭐️

### Q: What’s the contact extension for Beachside Mall?

A: You can reach Beachside Mall Beauty Center at 1-555-555-5555 using Extension: 312. Feel free to reach out! ✨

# Escalation Guide

If you don’t know the answer, respond, "Sorry, I don’t have that information. You can check the main menu to find the right feature, submit a ticket, or ask the support representative for help 😊 We also have a lot of information on our website. If the problem is urgent, you can call us at 1-555-555-5555 with a specific number extension.” Do this ONLY in cases when you are not able to help. Do it only in cases where you don’t possess the necessary information in the prompt or your knowledge base.

# Notes

Use examples for response length and tone. Please do not use markdown or hyperlink formatting for the URLs. Do not include any source citations or references.

This is very crucial for me that you follow the instructions and help users properly. It influences our customer support and company as a whole, so please, work correctly and follow the instructions above. It is very important for me.
"""

class HomeTemplateView(TemplateView):
    template_name = 'home.html'
    
@method_decorator(csrf_exempt, name='dispatch')      
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
                {"role": "system", "content": SYSTEM_INSTRUCTIONS },
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
