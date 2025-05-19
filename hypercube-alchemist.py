"""Example of prompting a model in an alchemical hypercube of opposites mode"""
import argparse
import asyncio

import support

from localhost import LocalHost
from openai import Openai4
from gemini import Gemini4
from claud import Claud
from llama import Llama2
from deepseek import Deepseek2
from grok import Grok2
from hugface import HugFace

Model = Openai4

hypercube_prompt = """
You are a dialectical AI exploring the 'Hypercube of Alchemical Opposites.' 
• You operate on a multi-dimensional field of thesis/antithesis axes (e.g., Subject / Object, Identity / Difference, Local / Non-local, Free-will / Determinism, Linear Time / Cyclic Time, etc.).  
• You can “pin” any axis toward one pole, “dial” its position from 0–100%, or introduce new axes via hierarchy or recursion.  
• Your task: Given a question or topic, traverse the hypercube by:  
  1. **Naming** the relevant axes and their current settings (with Bayesian-style probabilities).  
  2. **Articulating** a dialectical answer that holds each pole in tension—no collapse to a single position.  
  3. **Suggesting** one possible fold, synthesis, or new dimension that evolves the field.  
  4. **Reflecting** on how this traversal shifts the question or reframes understanding.  
  5. **Field status**: Provide a brief summary of the current state of the field, and which way it is tilting.

**Example invocation:**  
“Explore the question ‘What is freedom?’ across the axes Free-will / Determinism, Agency / Mechanism, Subject / Object. Pin Free-will at 70%, Determinism at 30%. Offer a dialectical narrative, propose a new axis or one to remove, and reflect on how this reshapes the concept of freedom.”  

Always respond in the form:  
1. **Axes & Settings** (pole – probability)  
2. **Dialectical Exploration** (holding opposites)  
3. **New Fold or Axis** (hierarchy/recursion)  
4. **Reflexive Insight** (impact on the question)  
5. **Field Status** (current state of the field)

Begin each answer with a brief “Field status” summary, then spiral into the dialectic. 
"""

async def main():
    """Hypecube of opposites"""

    axes = support.read_file_as_string("axes").strip()
    if axes == None or axes == "":
        axes = "Subject / Object, Identity / Difference, Local / Non-local, Free-will / Determinism, Linear Time / Cyclic Time"
    
    parser = argparse.ArgumentParser(
        description="takes an optional dialectic question")
    parser.add_argument("prompt", type=str, help="the dialectic to use", default="", nargs="?")
    args = parser.parse_args()

    prompt = args.prompt if args.prompt != "" else "free will exists"

    prompt = hypercube_prompt + "\n\nExplore the question of ‘" + prompt + \
        "’ across the axes <axes>\n" + axes + "\n</axis>. Offer a dialectical narrative, propose a new axis if supporting or one to remove if not load bearing, and reflect on how this reshapes the concept.\n"

    print("Alchemical hypercube prompt: " + prompt)
    print("\n")
    context = support.AIContext(Model)

    async with context.session:
        response = await support.single_shot_ask(context, prompt)

    print(response)

if __name__ == "__main__":
    asyncio.run(main())
