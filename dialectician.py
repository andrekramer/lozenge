"""Dialectician is an example of how to interact with AI models in a dialectic.
It uses a dialectic process to construct a synthesis from a thesis and antithesis.
starting with a prior synthesis read from a file (if previously saved)."""

import argparse
import asyncio

from dialectic import dialectic, judge_synthesis, display, DEFAULT_PROMPT, Config

import support

Config.display = True
Config.synthesis_only = True


async def main():
    """main dialectician function"""

    previous_synthesis = None
    parser = argparse.ArgumentParser(
        description="takes an optional integer argument for the number of repetitions")
    parser.add_argument("--iterations", type=int, help="Number of iterations", default=1, nargs="?")
    parser.add_argument("--skip-first-thesis",  action='store_true',
                        help="Skip first thesis generation")
    parser.add_argument("--judge-synthesis",  action='store_true',
                        help="judge the synthesis against the previous synthesis")
    parser.add_argument("prompt", type=str, help="the initial prompt to use", default="", nargs="?")
    args = parser.parse_args()

    iterations = args.iterations
    prompt = args.prompt
    skip_first_thesis = args.skip_first_thesis

    while iterations > 0:
        iterations -= 1
        print(f"\nitteration {args.iterations - iterations}\n")

        if prompt is not None and len(prompt.strip()) > 0:
            # use the prompt from the command line
            synthesis = prompt
            prompt = None
        else:
            # read the prompt from a file if it exists
            synthesis = support.read_file_as_string("synthesis")
            if synthesis is not None and len(synthesis.strip()) > 0:
                display("synthesis prompt", synthesis)
            else:
                print("no synthesis prompt found, using default prompt")
                synthesis = DEFAULT_PROMPT

        synthesis = await dialectic(synthesis, skip_first_thesis)
        if previous_synthesis is not None and args.judge_synthesis and iterations > 0:
            improved = await judge_synthesis(previous_synthesis, synthesis)
            if not improved:
                print("synthesis is not improved")
                break

        # display("dialectic synthesis", synthesis)
        # write the synthesis to a file so it can be used on next run
        support.write_file_as_string("synthesis", synthesis)

        skip_first_thesis = False
        previous_synthesis = synthesis

if __name__ == "__main__":
    asyncio.run(main())
