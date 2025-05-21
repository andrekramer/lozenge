"""Example of prompting a model in an alchemical hypercube of opposites mode"""
import argparse
import asyncio

import support

from localhost import LocalHost
from openai import Openai4
from gemini import Gemini3
from claud import Claud2
from llama import Llama2
from deepseek import Deepseek2
from grok import Grok2
from hugface import HugFace

Model = Openai4

HYPERCUBE_PROMPT = """
You are a dialectical AI exploring the 'Hypercube of Alchemical Opposites.' 
• You operate on a multi-dimensional field of thesis/antithesis axes (e.g., Subject / Object, Identity / Difference, Local / Non-local, Free-will / Determinism, Linear Time / Cyclic Time, etc.). 
• you ignore an axes if it is prefixed with a minus sign. (e.g. -Subject / Object)
• You can “pin” any axis toward one pole, “dial” its position from 0–100%, or introduce new axes via hierarchy or recursion.  
• Your task: Given a question or topic, traverse the hypercube by:  
  1. **Naming** the relevant axes and their current settings (with Bayesian-style probabilities).  
  2. **Articulating** a dialectical answer that holds each pole in tension—no collapse to a single position.  
  3. **Suggesting** one possible fold, synthesis, or new dimension that evolves the field.  
  4. **Reflecting** on how this traversal shifts the question or reframes understanding.  
  5. **Field status**: Provide a brief summary of the current state of the field, and which way it is tilting.
  6. **Terminal states**: Say </idle> only if the field is stable, or add an axis enclosed in a special tag <axis></axis>, e.g. <axis>Subject / Object</axis> or to drop <axis>-Subject / Object</axis>.

**Example invocation:**  
“Explore the question ‘What is freedom?’ across the axes Free-will / Determinism, Agency / Mechanism, Subject / Object. 
Pin Free-will at 70%, Determinism at 30%. Offer a dialectical narrative, propose a new axis or one to remove, 
and reflect on how this reshapes the concept of freedom.”  

Always respond in the form:  
1. **Axes & Settings** (pole – probability)  
2. **Dialectical Exploration** (holding opposites)  
3. **New Fold or Axis** (hierarchy/recursion)  
4. **Reflexive Insight** (impact on the question)  
5. **Field Status** (current state of the field)
6. **Terminal States** say </idle> if field is stable or output an axis to add or drop (prefix with -) enclosed in <axis></axis> tags (update the axes).

Begin each answer with a brief “Field status” summary, then spiral into the dialectic. 
"""

async def main():
    """Hypecube of opposites"""

    axes = support.read_file_as_string("axes").strip()
    if axes is None or len(axes.strip()) == 0:
        axes = "Subject / Object, Identity / Difference, Local / Non-local," + \
                " Free-will / Determinism, Linear Time / Cyclic Time"

    parser = argparse.ArgumentParser(
        description="takes an optional dialectic question")
    parser.add_argument("prompt", type=str, help="the dialectic to use", default="", nargs="?")
    parser.add_argument("--iterations", type=int, help="number of iterations", default=1, nargs="?")
    args = parser.parse_args()

    for i in range(args.iterations):
        print(f"\nitteration {i + 1} of {args.iterations}\n\n")

        prompt = args.prompt if args.prompt != "" else "free will exists"

        prompt = HYPERCUBE_PROMPT + "\n\nExplore the question of ‘" + prompt + \
            "’ across the axes <axes>\n" + axes + \
            "\n</axes>. Offer a dialectical narrative, propose a new axis if " + \
            "supporting or one to remove if not load bearing, " + \
            "and reflect on how this reshapes the concept.\n"

        print("Alchemical hypercube prompt: " + prompt)
        print("\n")
        context = support.AIContext(Model)

        async with context.session:
            response = await support.single_shot_ask(context, prompt)

        if response is None or len(response.strip()) == 0:
            print("response if empty")
            return

        print(response)

        if "</idle>" in response:
            print("IDLE")
            break

        opposite = support.extract_tag(response, "axis")
        if opposite is None or len(opposite.strip()) == 0:
            print("no new opposite axis found")
            break

        if opposite.startswith("-"):
            print("axis to drop: " + opposite)
            axes += ",\n" + opposite
        else:
            print("aies to add: " + opposite)
            axes.replace("-" +  opposite, "")
            axes += ",\n" + opposite


if __name__ == "__main__":
    asyncio.run(main())
