import os
import spacy
from groq import Groq
import logging
import re

os.environ["GROQ_API_KEY"] = "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"
nlp = spacy.load("en_core_web_sm")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

last_posted_time = None
last_commented_time = None 

logging.basicConfig(
    filename='reddit_posting_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)


def generate_ai_content(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
        )
        logging.info("AI content generated successfully.")
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error while calling the Groq API: {e}")
        return None

# Function to extract relevant keyword/topic from the generated content using NLP
def extract_keyword_from_content(content):
    doc = nlp(content)
    keywords = []

    # Extract Named Entities or Noun Chunks
    for ent in doc.ents:
        keywords.append(ent.text)
    
    if not keywords:
        for chunk in doc.noun_chunks:
            keywords.append(chunk.text)
    
    return keywords[0] if keywords else "technology"

import re

def generate_dynamic_title(ai_content):
    first_sentence = ai_content.split('.')[0]
    first_sentence = re.sub(r'[^\w\s]', '', first_sentence).strip()

    if len(first_sentence) < 10:
        ai_content = ai_content.strip()
        words = ai_content.split()
        first_few_words = " ".join(words[:6])
        first_sentence = f"{first_few_words}..."
    
    title = f"{first_sentence}"

    return title
