# Chat bot to interact with openAI

## Setup
Goto https://platform.openai.com/, create account and generate API key. Place the api key in config.ini file.

#### Example 1:
```
python3 QueryOpenAI.py
Enter instructions for chatgpt model: You will be provided with a message, and your task is to respond using emojis only.
Enter question for chatgpt model: how are you doing?
👋😊👍
```

#### Example 2:
```
python3 QueryOpenAI.py
Enter instructions for chatgpt model: Respond in less than 100 words
Enter question for chatgpt model: Make a story on cat
Once upon a time, in a small village, there lived a mischievous cat named Whiskers. Whiskers was known for his playful nature and his ability to bring joy to everyone he encountered. One day, he stumbled upon a lost kitten named Mittens. Whiskers took Mittens under his wing and taught her the ways of the village. Together, they embarked on countless adventures, exploring the woods, chasing butterflies, and making friends with other animals. Whiskers and Mittens became inseparable, spreading happiness wherever they went. Their bond reminded everyone of the power of friendship and the joy that can be found in the simplest of moments.
```
