import re
from collections import Counter
from celery import shared_task
from django.contrib.auth.models import User
from .models import Paragraph, WordFrequency

@shared_task
def process_paragraph_text(user_id, paragraph_content):
    """
    Celery task to process a single paragraph and update word frequency.
    """
    user = User.objects.get(id=user_id)

    # 1. Create the Paragraph object in the database
    paragraph_obj = Paragraph.objects.create(user=user, content=paragraph_content)

    # 2. Find all words (simple regex to get alphanumeric words)
    words = re.findall(r'\b\w+\b', paragraph_content.lower())
    word_counts = Counter(words) # This efficiently counts all words

    # 3. Create WordFrequency objects in bulk for efficiency
    word_frequency_objects = []
    for word, count in word_counts.items():
        word_frequency_objects.append(
            WordFrequency(
                user=user,
                paragraph=paragraph_obj,
                word=word,
                frequency=count
            )
        )

    WordFrequency.objects.bulk_create(word_frequency_objects)
    print(f"Processed paragraph {paragraph_obj.id} for user {user.username}")