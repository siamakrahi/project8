"""
WebSocket consumer for handling real-time chat interactions.
"""

import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils.faq_manager import FAQManager

logger = logging.getLogger(__name__)
faq_manager = FAQManager()


class ChatConsumer(AsyncWebsocketConsumer):
    """Handles WebSocket connections for chatbot functionality."""
    
    async def connect(self):
        """Accept incoming WebSocket connection."""
        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        logger.debug(f"WebSocket disconnected with code: {close_code}")

    async def receive(self, text_data):
        """Process incoming chat messages."""
        try:
            data = json.loads(text_data)
            query = data.get('message', '').strip()
            
            if not query:
                return

            logger.debug(f"Processing query: {query}")
            best_match = faq_manager.find_best_match(query)
            
            response_message = (
                best_match 
                if best_match 
                else "Sorry, I couldn't find an answer to your question."
            )

            await self.send(json.dumps({
                'message': response_message
            }))

        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            await self.send(json.dumps({
                'message': "Invalid message format"
            }))
        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            await self.send(json.dumps({
                'message': "An error occurred while processing your request"
            }))

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .utils.faq_manager import FAQManager

# faq_manager = FAQManager()

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         try:
#             print("Received message:", text_data) 
#             data = json.loads(text_data)
#             query = data.get('message', '').strip()
            
#             if query:
#                 print("Searching for:", query)
#                 best_match = faq_manager.find_best_match(query)
#                 print("Best match:", best_match)
                
#                 await self.send(json.dumps({
#                     'message': best_match if best_match else "متاسفانه پاسخی برای سوال شما یافت نشد."
#                 }))

#         except Exception as e:
#             print(f"Error: {str(e)}")
#             await self.send(json.dumps({
#                 'message': "خطایی در پردازش درخواست رخ داد"
#             }))

#     def find_best_match(self, results):
#         combined = results['db_results'] + results['file_results']
#         return combined[0]['answer'] if combined else None