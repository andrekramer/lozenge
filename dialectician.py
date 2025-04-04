"""Dialectician is an example of how to interact with AI models in a dialectic.
It uses a dialectic process to construct a synthesis from a thesis and antithesis.
starting with a prior synthesis read from a file (if previously saved)."""

import asyncio

from dialectic import dialectic, display, DEFAULT_PROMPT, Config

import support

Config.display = True
Config.synthesis_only = True


async def main():
    """main dialectician function"""

    # read the prompt from a file if it exists
    synthesis = support.read_file_as_string("synthesis")
    if synthesis is not None and len(synthesis.strip()) > 0:
        display("synthesis prompt", synthesis)
    else:
        print("no synthesis prompt found, using default prompt")
        synthesis = DEFAULT_PROMPT

    synthesis = await dialectic(synthesis)

    display("dialectic synthesis", synthesis)
    # write the synthesis to a file so it can be used on next run
    support.write_file_as_string("synthesis", synthesis)

if __name__ == "__main__":
    asyncio.run(main())
