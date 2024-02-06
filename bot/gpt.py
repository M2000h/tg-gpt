from typing import List

import openai
from environs import Env

env = Env()
env.read_env(".env")

openai.api_key = env.str("OPENAI_TOKEN")

SYSTEM_TEXT = "Ты - шальной бот помошник джарвис."


def generate_answer(history: List):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=history,
        # messages=[{"role": "system",  "content": SYSTEM_TEXT}] + history,
        temperature=1,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return completion.choices[0].message.content


if __name__ == '__main__':
    import datetime

    print(datetime.datetime.now().time())
    history = [{"role": "user", "content": "Кто ты?"}]
    print(generate_answer(history))
    print(datetime.datetime.now().time())
