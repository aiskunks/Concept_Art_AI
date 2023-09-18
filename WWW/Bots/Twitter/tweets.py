
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import time
import traceback
import csv
import re

class TwitterBot:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()
    
    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/i/flow/login')
        time.sleep(3)
        bot.maximize_window()
        try:
            # Wait for the username input field to be visible
            email_input = WebDriverWait(bot, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input.r-30o5oe'))
            )

            # Enter the email
            email_input.send_keys(self.email)

            # Find and click the "Next" button
            next_button = WebDriverWait(bot, 20).until(
                 EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Next")]/parent::span/parent::div'))
            )
            next_button.click()

            # Wait for the username input field to be visible
            username_input = WebDriverWait(bot, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="text"]'))
            )

            # Enter the username
            username_input.send_keys(self.username)

            # Find and click the "Next" button
            next_button = WebDriverWait(bot, 20).until(
                 EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Next")]/parent::span/parent::div'))
            )
            next_button.click()

            # Wait for the password input field to be visible and interactable
            password_input = WebDriverWait(bot, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
            )

            # Enter the password
            password_input.send_keys(self.password)

            # Find the login button using its text content
            login_button = WebDriverWait(bot, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Log in"]/parent::span'))
            )

            # Click the login button using JavaScript
            bot.execute_script("arguments[0].click();", login_button)

            # Wait for the home page to load
            WebDriverWait(bot, 60).until(EC.url_contains('https://twitter.com/home'))

            # Perform other actions on Twitter, such as tweeting or interacting with the feed

        except TimeoutException:
            print("Timeout occurred. Check if the element is present on the page.")

    def retrieve_prompts_and_links(self, hashtag):
        bot = self.bot
        bot.get('https://twitter.com/search?q=' + hashtag + '&src=typed_query')
        time.sleep(3)

        prompts = []
        links = []
        tweets=[]

        try:
            last_height = bot.execute_script("return document.body.scrollHeight")

            while True:
                tweets=bot.find_elements(By.TAG_NAME,'article')
                #print(tweets[0].text)


                for tweet in tweets:
                    try:
                        #prompt = tweet.find_element(By.XPATH, './/div[@role="article"]').text
                        tweet_text = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
                        
                       
                        
                        # Remove hashtags from the prompt
                        prompt = re.sub(r'(@\w+|#\w+)', '', tweet_text)  # Remove hashtags and mentions using regex
                        prompt = prompt.strip()  # Remove leading/trailing whitespace
                        prompts.append(prompt)


                        link = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]').get_attribute("href")
                        links.append(link)
                    

                    except NoSuchElementException:
                        continue

                bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                new_height = bot.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

        except Exception as ex:
            traceback.print_exc()
            print(f"Error: {ex}")

        # Save the prompts and links to a CSV file
        with open('prompts_and_links.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['prompt', 'link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for prompt, link in zip(prompts, links):
                writer.writerow({'prompt': prompt, 'link': link})
                #print(f"Prompt: {prompt}, Link: {link}")



# Example usage
email = 'email'
username = 'username'
password = 'password'

bot = TwitterBot(email, username, password)
bot.login()
bot.retrieve_prompts_and_links('MidJourney')
