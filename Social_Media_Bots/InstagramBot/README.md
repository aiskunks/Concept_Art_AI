# Instagram Bot for Posting Images

## Introduction

The Instagram Bot for Posting Images is a Python script that allows you to automate the process of posting images to your Instagram account. Whether you're a social media manager, influencer, or just want to streamline your Instagram posting, this bot can help you schedule and publish images without manual intervention.

**Note:** Automating actions on Instagram, including posting, may violate Instagram's terms of service. Use this bot responsibly and consider the potential risks of automated posting, such as account suspension.

## Features

- Schedule and automate image posts on Instagram.
- Easily configure the bot to post images with captions and hashtags.
- Simple and straightforward Python script.

## Prerequisites

Before using the Instagram Bot, you need to have the following:

1. **Instagram Account**: You must have an active Instagram account.
   
2. **Instagram Business or Creator Account**: To use the Instagram Graph API for posting, you need to convert your Instagram account to a Business or Creator account.

3. **Facebook App and Developer Account**: You'll need to create a Facebook App and associate it with your Instagram account. Follow the steps in the [Facebook for Developers documentation](https://developers.facebook.com/docs/instagram-api/getting-started) to set this up.

4. **Access Token**: Obtain a long-lived access token for the Instagram Graph API. You can generate one in the [Instagram Graph API Explorer](https://developers.facebook.com/tools/explorer/).

## Installation

1. **Clone the Repository**:

   ```shell
   git clone https://github.com/aiskunks/Concept_Art_AI.git
   cd Social_Media_Bots/InstagramBot
   ```

2. **Configure the Bot**:

   - Open the `.env` file and fill in the following information:
     - `INSTAGRAM_USERNAME`: Your Instagram username.
     - `INSTAGRAM_PASSWORD`: Your Instagram password.
     - `INSTAGRAM_USER_ID`: Your Instagram user id obtained from facebook graph api explorer.
     - `INSTAGRAM_APP_ID`: Your Instagram app id obtained from developer account.
     - `INSTAGRAM_APP_SECRET`: Your Instagram app secret obtained from developer account.
     - `ACCESS_TOKEN`: The long-lived access token obtained from the Instagram Graph API.

## Usage

1. **Add Images**:

   Place the images you want to post in the `./Images/` directory and create the directory if it doesn't exists.

2. **Create Posts**:

   - Open the `PostImagesOnInstagram.py` file.
   - Add the image filepath, captions for each post you want to schedule.
   - Run the script and you should see a new post on instagram made by the instagram bot.


## Support and Issues

If you encounter any issues or have questions about using the Instagram Bot for Posting Images, feel free to [create an issue](https://github.com/Concept_Art_AI/issues) in the GitHub repository.

## Disclaimer

**Use this bot responsibly**: Automated actions on Instagram, including posting, may violate Instagram's terms of service. Be aware of the potential risks, including account suspension, when using automation tools.

---

**Disclaimer**: Use this bot at your own risk and in accordance with Instagram's policies. Automation on social media platforms may have legal and ethical implications, and it's your responsibility to ensure compliance with all relevant rules and regulations.