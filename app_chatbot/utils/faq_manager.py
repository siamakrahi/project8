from django.db.models import Q
from app_chatbot.models import FAQ
from fuzzywuzzy import fuzz
import os
from django.conf import settings

class FAQManager:
    def __init__(self):
        self.faqs = list(FAQ.objects.select_related('category').all())
        
    def find_best_match(self, query):
        # جستجوی دقیق
        for faq in self.faqs:
            if query.lower() in faq.question.lower():
                return faq.answer
        
        # جستجوی fuzzy
        best_match = None
        highest_score = 0
        
        for faq in self.faqs:
            score = fuzz.ratio(query.lower(), faq.question.lower())
            if score > highest_score and score > 70:
                highest_score = score
                best_match = faq.answer
                
        return best_match
