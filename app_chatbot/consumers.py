import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils.faq_manager import FAQManager

faq_manager = FAQManager()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            print("Received message:", text_data)  # افزودن این خط
            data = json.loads(text_data)
            query = data.get('message', '').strip()
            
            if query:
                print("Searching for:", query)  # افزودن این خط
                best_match = faq_manager.find_best_match(query)
                print("Best match:", best_match)  # افزودن این خط
                
                await self.send(json.dumps({
                    'message': best_match if best_match else "متاسفانه پاسخی برای سوال شما یافت نشد."
                }))

        except Exception as e:
            print(f"Error: {str(e)}")  # این خط باید وجود داشته باشد
            await self.send(json.dumps({
                'message': "خطایی در پردازش درخواست رخ داد"
            }))

    def find_best_match(self, results):
        # الگوریتم اولویت‌بندی نتایج
        combined = results['db_results'] + results['file_results']
        # در اینجا می‌توانید منطق پیشرفته‌تری پیاده‌سازی کنید
        return combined[0]['answer'] if combined else None