import os
import spacy
import praw
import schedule
import time as t
from datetime import datetime
import logging
from groq import Groq
import random

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

# Initial prompt for daily post
current_prompt = "Write a sci-fi story where a character relives the same event over and over again."

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

# Function to post to the subreddit
def post_to_reddit():
    global last_posted_time, current_prompt

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    if last_posted_time == current_time:
        logging.info("Post already submitted for this minute. Skipping...")
        return

    reddit = praw.Reddit(
        client_id="S0raxummY9kErUI9KPO4Hg",
        client_secret="UeA7JWAHohxTA0vVBBFxrH7Y4k8Chg",
        user_agent="script:daily_post_bot:v1.0 (by u/Funny-Use-6422)",
        username="Funny-Use-6422",
        password="I@Mshubhangi318"
    )

    subreddit = reddit.subreddit("test")
    ai_content = generate_ai_content(current_prompt)

    if ai_content:
        post_title = generate_dynamic_title(ai_content)

        subreddit.submit(post_title, selftext=ai_content)
        logging.info(f"AI-generated post submitted successfully!")
        last_posted_time = current_time

        next_keyword = extract_keyword_from_content(ai_content)
        current_prompt = f"Write a creative Reddit post about {next_keyword}."
    else:
        logging.error("No content generated. Post not submitted.")


# Function to comment on the latest post in the subreddit
def comment_on_latest_post():
    global last_commented_time

    current_time = datetime.now()
    if last_commented_time and (current_time - last_commented_time).total_seconds() < 72 * 3600:
        logging.info("Not yet time to comment on the latest post. Skipping...")
        return

    reddit = praw.Reddit(
        client_id="S0raxummY9kErUI9KPO4Hg",
        client_secret="UeA7JWAHohxTA0vVBBFxrH7Y4k8Chg",
        user_agent="script:daily_post_bot:v1.0 (by u/Funny-Use-6422)",
        username="Funny-Use-6422",
        password="I@Mshubhangi318"
    )

    subreddit = reddit.subreddit("series")
    latest_post = next(subreddit.new(limit=1))

    comment = f"Great post! {generate_ai_content('Tell me about ' + latest_post.title)}"

    # Limit the comment to 700 words
    comment_words = comment.split()
    if len(comment_words) > 700:
        comment = ' '.join(comment_words[:700])

    latest_post.reply(comment)
    logging.info(f"Comment posted on the latest post: {latest_post.title}")

    # Update last commented time
    last_commented_time = current_time


# Scheduling function for both daily post and comment on latest post
def schedule_tasks():
    post_time = "14:57"
    
    schedule.every().day.at(post_time).do(post_to_reddit)
    # schedule.every(10).minutes.do(post_to_reddit)

    schedule.every(72).hours.do(comment_on_latest_post)
    # schedule.every(5).minutes.do(comment_on_latest_post)   

    logging.info(f"Bot will post daily at {post_time} and comment once every 72 hours. Waiting for the scheduled time...")

    while True:
        schedule.run_pending()
        t.sleep(1)

if __name__ == "__main__":
    schedule_tasks()


