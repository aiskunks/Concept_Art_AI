import openai
import configparser

config = configparser.RawConfigParser()
config.read('config.ini')
openai.api_key = config.get('dev', 'api_key')

def query(question, instructions):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        n=1,
        messages=[
            {
                "role": "system",
                "content": instructions
            },
            {
                "role": "user",
                "content": question
            },
        ],
    )
    print(response["choices"][0]["message"]["content"])


if __name__ == "__main__":
    instructions = input("Enter instructions for chatgpt model: ")
    question = input("Enter question for chatgpt model: ")
    query(question, instructions)
