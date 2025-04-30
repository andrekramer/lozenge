"""A dialectic process to construct a thesis, antithesis and synthesis.
starting with some prior synthesis as input."""

import support

from localhost import LocalHost
from openai import Openai4
from gemini import Gemini4
from claud import Claud
from llama import Llama2
from deepseek import Deepseek2
from grok import Grok2
from hugface import HugFace
from human import Human

Model = Openai4

ThesisModel = Model
AntithesisModel = Model
SynthesisModel = Model

JudgeModel = Model

DEFAULT_PROMPT = "free will exists"

TACTICAL_INSTRUCTIONS = "Be opinionated, critical, creative and constructive. " + \
     "Be self-consistent and logical in each position taken. " + \
     "Take an advisarial and novel perspective when creating an antithesis. " + \
     "Aim to faitfully model the real world, " + \
     "Don't compromise or take the middle ground when creating a synthesis."

META_INSTRUCTIONS = "This dialect progresses in multiple rounds, this being " + \
    "one of them. A new thesis is made from previous synthesis and antiethesis " +\
    "is introduced and the synthesis is updated in each round.\n"

INSTRUCTIONS = "You are a dialectician. " + \
    "You reason by constructing a thesis, antithesis and synthesis, " + \
    "as a multi-step rational dialectic process.\n" + \
    META_INSTRUCTIONS + \
    TACTICAL_INSTRUCTIONS + \
    "\n"

LEFT_DASHES = "-" * 20 + " "
RIGHT_DASHES = " " + "-" * 20

class Config:
    """Configuration for dialectic process"""
    display = False
    synthesis_only = False

def display(title, text):
    """Display title and text"""
    if not Config.display:
        return
    print(LEFT_DASHES + title + RIGHT_DASHES)
    print(text)


async def dialectic(synthesis, skip_thesis=False):
    """A dialectic process to construct a thesis, antithesis and synthesis.
       starting with some prior synthesis as argument. Returns the synthesis."""
    context = support.AIContext(ThesisModel)

    async with context.session:

        if not skip_thesis:
            thesis = "Construct a thesis (and output only the thesis)" + \
                "in the dialectic for the following:\n"

            round1 = INSTRUCTIONS + thesis + synthesis
            display("?thesis?", round1)
            thesis = await support.single_shot_ask(context, support.escape(round1))
            if thesis is None or len(thesis.strip()) == 0:
                raise ValueError("thesis is empty")
        else:
            # use the synthesis as the thesis
            thesis = synthesis

        display("thesis", thesis)

        # taking an orthogonal OR diametrically opposed perspective
        antithesis = "Construct an antithesis (and output only the antithesis)" + \
             " in the dialectic (by introducing contradictions) for the following thesis:\n"

        context.model = AntithesisModel
        round2 = INSTRUCTIONS + antithesis + thesis
        display("?antithesis?", round2)
        antithesis = await support.single_shot_ask(context, support.escape(round2))
        if antithesis is None or len(antithesis.strip()) == 0:
            raise ValueError("antithesis is empty")
        display("antithesis", antithesis)

        synthesis = "Construct a synthesis (and output only the synthesis)" + \
            " in the dialectic (by qualifying/negating the contradictory statements) " + \
            "for the following thesis and antithesis:\n" + \
            "<thesis>\n" + thesis + "</thesis>\n<antithesis>\n" + antithesis + "</antithesis>\n"

        context.model = SynthesisModel
        round3 = INSTRUCTIONS + synthesis
        display("?synthesis?", round3)

        synthesis= await support.single_shot_ask(context, support.escape(round3))
        if synthesis is None or len(synthesis.strip()) == 0:
            raise ValueError("synthesis is empty")
        display("synthesis", synthesis)

        if Config.synthesis_only:
            return synthesis

        return "thesis:\n" + thesis + "\nantitheisis\n" + antithesis + "\nsynthesis\n" + synthesis


async def judge_synthesis(previous_synthesis, synthesis):
    """Judge the synthesis to see if it is improved over the previous synthesis"""
    context = support.AIContext(JudgeModel)

    async with context.session:

        judge = "Compare the following synthesis and the previous synthesis " + \
                "(given first) and output TRUE if it is different else output FALSE\n" + \
                "<previous_synthesis>\n" + previous_synthesis + \
                "\n</previous_synthesis>\n<synthesis>\n" + synthesis + "\n</synthesis>"

        display("?judge?", judge)
        response = await support.single_shot_ask(context, support.escape(judge))
        if response is None or len(response.strip()) == 0:
            raise ValueError("synthesis judgement is empty")

        print(f"judge response: {response}")
        if "FALSE" in response and "TRUE" not in response:
            return False
    return True
