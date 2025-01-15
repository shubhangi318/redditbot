import praw
import schedule
import time as t
from datetime import datetime
import logging
from utils import generate_ai_content, extract_keyword_from_content, generate_dynamic_title


last_posted_time = None
last_commented_time = None

logging.basicConfig(
    filename='reddit_posting_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

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
        user_agent="script:daily_post_bot:v1.0 (by u/{your_user_name})",
        username="your_user_name",
        password="your_password"
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
        user_agent="script:daily_post_bot:v1.0 (by u/{your_user_name})",
        username="your_user_name",
        password="your_password",
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
    # Initial prompt for daily post
    current_prompt = "Write a sci-fi story where a character relives the same event over and over again."
    schedule_tasks()
