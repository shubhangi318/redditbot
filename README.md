## Reddit AI Content Bot

#### A Reddit bot that automates posting AI-generated content and commenting on the latest post in a subreddit every 72 hours. The bot uses the Groq API for AI content generation, spaCy for natural language processing (NLP), and PRAW for interacting with Reddit.


### Features

* Daily Posts: The bot posts an AI-generated content daily at a specified time (e.g., 13:55 PM).
* Comment on Latest Post: Every 72 hours, the bot comments on the latest post in the subreddit with AI-generated content related to the post.
* Customizable Prompt: The bot generates content based on a prompt and updates it with keywords extracted from previously generated content.
* Logging: Logs the bot's activity for easy troubleshooting and tracking of posts/comments.


### Technical Requirements

* Reddit API Authentication: Set up the Reddit API using your client_id, client_secret, username, and password. Create a Reddit application on [Reddit's Developer Portal](https://www.reddit.com/prefs/apps).
    
* Groq API Integration: Obtain an API key from [Groq's website](https://groq.com/) and set it in the `.env` file.
    
* Scheduling: The bot posts every daily at 4:42 pm and comments on the latest post once every 72 hours. You can adjust the frequency in the `schedule_tasks()` function in `bot.py`.

Before running the bot, ensure you have the following dependencies installed:

- Python 3.6+
- praw: Python Reddit API Wrapper
- groq: Python wrapper for the Groq API
- spacy: NLP library
- schedule: Task scheduler for periodic actions


### Install Dependencies

You can install all dependencies via pip by running the following commands:

    pip install praw groq spacy schedule
    python -m spacy download en_core_web_sm


### Configuration

1. Set Environment Variables: You need to set your Groq API key as an environment variable.

   On macOS/Linux, add the following line to your .bashrc or .zshrc file:

       export GROQ_API_KEY="your_groq_api_key"

   On Windows, you can set the environment variable through the Environment Variables section in the System Properties or use set in the command prompt.

2. Reddit API Credentials: Make sure to replace the following Reddit credentials in the code with your own:

       client_id, client_secret, user_agent, username, password

   You can obtain these by creating a Reddit application at: Reddit Apps(https://www.reddit.com/prefs/apps).


### Running the Bot on EC2

I have deployed the bot on an Amazon EC2 instance to ensure it runs continuously. This setup ensures the bot is always active and performs scheduled tasks without interruptions. To run the bot on an EC2 instance:

1. Launch an EC2 Instance:

    Use a Linux AMI (e.g., Amazon Linux 2 or Ubuntu) with sufficient permissions to install required software.
        
2. Install Required Software:

   SSH into your EC2 instance and update the system:

       sudo apt update && sudo apt upgrade -y
            
   Install the required dependencies:

       pip3 install praw groq spacy schedule
       python3 -m spacy download en_core_web_sm

3. Set Environment Variables:

   Add the following line to your .bashrc file:

       export GROQ_API_KEY="your_groq_api_key"
            
4. Use SCP to transfer your script to the EC2 instance:

       scp reddit_ai_bot.py ec2-user@your-ec2-public-ip:/home/ec2-user/

5. Run the Script:

       python3 reddit_ai_bot.py

Use a tool like tmux or screen to keep the bot running in the background


### Usage

After configuring the environment variables and updating the Reddit API credentials, you can run the bot as follows:

    python3 reddit_ai_bot.py
    
The bot will:
- Post AI-generated content to the specified subreddit at the scheduled time.
- Comment on the latest post in the subreddit every 72 hours.

    
### Logs
    
The bot generates logs to track its activity. The log file reddit_posting_bot.log will be created in the same directory as the script. It will include information about posts, comments, and any errors encountered.


### How It Works

1. AI Content Generation: The bot uses the Groq API to generate AI content based on a user-defined prompt.
2. Natural Language Processing (NLP): Using spaCy, the bot extracts keywords or topics from the AI-generated content to craft the next prompt.
3. Posting on Reddit: The bot uses the PRAW library to submit posts to a subreddit. It checks if a post has already been made in the current minute to avoid duplicate posts.
4. Commenting on Latest Post: Every 72 hours, the bot comments on the most recent post in the subreddit using the AI-generated content.


### Customizing the Bot

You can customize the time the bot posts daily by changing the post_time variable in the schedule_tasks() function.

    post_time = "13:55"  # Change this to your desired time in 24-hour format

You can modify the subreddit the bot interacts with by changing the following line:

    subreddit = reddit.subreddit("test")  # Change "test" to your desired subreddit
    
The bot is currently set to comment on the latest post every 72 hours. You can adjust this frequency in the schedule_tasks() function.

    schedule.every(72).hours.do(comment_on_latest_post)  # Change 72 to any other number of hours


### Sample Output
    
Below are examples of the bot's output, including AI-generated posts and comments on Reddit. These demonstrate how the bot interacts with the subreddit.

Example 1: Daily Post
        
Subreddit: r/test

![Image 1 for post](https://i.postimg.cc/wBj7WJpb/img3.png)
![Image 1 for post](https://i.postimg.cc/XqSN0BRW/img4.png)

Example 2: Comment on Latest Post

Subreddit: r/series

![Image 1 for comment](https://i.postimg.cc/gcq64Y95/img1.png)
![Image 2 for comment](https://i.postimg.cc/59YfNggm/img2.png)


### Troubleshooting
    
1. "No content generated": If the bot is not generating content, ensure your Groq API key is correct and the spaCy model is properly loaded.
2. Reddit Authentication Issues: Double-check your Reddit API credentials and make sure the app has the appropriate permissions to post and comment.


### Contributing

If you find any issues or have ideas for improvements, feel free to open an issue or submit a pull request. Contributions are welcome!
