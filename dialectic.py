"""A dialectic process to construct a thesis, antithesis and synthesis.
starting with some prior synthesis as input."""

import support

from localhost import LocalHost
from openai import Openai
from gemini import Gemini4
from claud import Claud
from llama import Llama2
from deepseek import Deepseek2
from grok import Grok2
from hugface import HugFace

Model = Openai
ThesisModel = Model
AntithesisModel = Model
SynthesisModel = Model

DEFAULT_PROMPT = "free will exists"

INSTRUCTIONS = "You are a dialectician. " + \
    "You reason by constructing a thesis, antithesis and synthesis, " + \
    "all of which aim to faitfully model the real world, " + \
    "as a multi-step rational dialectic process.\n"

LEFT_DASHES = "-" * 20 + " "
RIGHT_DASHES = " " + "-" * 20

class Config:
    """Configuration for dialectic process"""
    display = False
    synthesis_only = False

def clean(s):
    """remove line breaks from string and escape \""""
    str1 = s.replace("\n", "\\n")
    str2 = str1.replace('"', '\\"')
    return str2

def display(title, text):
    """Display title and text"""
    if not Config.display:
        return
    print(LEFT_DASHES + title + RIGHT_DASHES)
    print(text)


async def dialectic(synthesis):
    """A dialectic process to construct a thesis, antithesis and synthesis.
       starting with some prior synthesis as argument. Returns the synthesis."""
    context = support.AIContext(ThesisModel)

    async with context.session:

        thesis = "Construct a thesis (and output only the thesis)" + \
            "in the dialectic for the following:\n"

        round1 = INSTRUCTIONS + thesis + synthesis
        display("?thesis?", round1)
        thesis = await support.single_shot_ask(context, clean(round1))
        if thesis is None or len(thesis.strip()) == 0:
            raise ValueError("thesis is empty")
        display("thesis", thesis)

        antithesis = "Construct an antithesis (and output only the antithesis)" + \
             " in the dialectic for the following thesis:\n"

        context.model = AntithesisModel
        round2 = INSTRUCTIONS + antithesis + thesis
        display("?antithesis?", round2)
        antithesis = await support.single_shot_ask(context, clean(round2))
        if antithesis is None or len(antithesis.strip()) == 0:
            raise ValueError("antithesis is empty")
        display("antithesis", antithesis)

        synthesis = "Construct a synthesis (and output only the synthesis)" + \
            " in the dialectic " + \
            "for the following thesis and antithesis:\n" + \
            "thesis:\n" + thesis + "\nantithesis:\n" + antithesis

        context.model = SynthesisModel
        round3 = INSTRUCTIONS + synthesis
        display("?synthesis?", round3)

        synthesis= await support.single_shot_ask(context, clean(round3))
        if synthesis is None or len(synthesis.strip()) == 0:
            raise ValueError("synthesis is empty")
        display("synthesis", synthesis)

        if Config.synthesis_only:
            return synthesis

        return thesis + "\n" + antithesis + "\n" + synthesis
