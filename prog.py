"""Example of prompting a model"""
import asyncio

import support

from localhost import LocalHost
from openai import Openai
from gemini import Gemini4
from claud import Claud
from llama import Llama2
from deepseek import Deepseek2
from grok import Grok2
from hugface import HugFace

model = Gemini4

async def main():
    """Example main function"""

    prompt = "roll a die"

    context = support.AIContext(model)

    async with context.session:
        response = await support.single_shot_ask(context, prompt)

    print(response)

if __name__ == "__main__":
    asyncio.run(main())
