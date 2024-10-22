import math
import random

import aiohttp
import hikari
import lightbulb

jargonWordPool = [
    [
        "TCP",
        "HTTP",
        "SDD",
        "RAM",
        "GB",
        "CSS",
        "SSL",
        "AGP",
        "SQL",
        "FTP",
        "PCI",
        "AI",
        "ADP",
        "RSS",
        "XML",
        "EXE",
        "COM",
        "HDD",
        "THX",
        "SMTP",
        "SMS",
        "USB",
        "PNG",
        "PHP",
        "UDP",
        "TPS",
        "RX",
        "ASCII",
        "CD-ROM",
        "CGI",
        "CPU",
        "DDR",
        "DHCP",
        "BIOS",
        "IDE",
        "IP",
        "MAC",
        "MP3",
        "AAC",
        "PPPoE",
        "SSD",
        "SDRAM",
        "VGA",
        "XHTML",
        "Y2K",
        "GUI",
    ],
    [
        "auxiliary",
        "primary",
        "back-end",
        "digital",
        "open-source",
        "virtual",
        "cross-platform",
        "redundant",
        "online",
        "haptic",
        "multi-byte",
        "bluetooth",
        "wireless",
        "1080p",
        "neural",
        "optical",
        "solid state",
        "mobile",
        "unicode",
        "backup",
        "high speed",
        "56k",
        "analog",
        "fiber optic",
        "central",
        "visual",
        "ethernet",
        "encrypted",
        "decrypted",
    ],
    [
        "driver",
        "protocol",
        "bandwidth",
        "panel",
        "microchip",
        "program",
        "port",
        "card",
        "array",
        "interface",
        "system",
        "sensor",
        "firewall",
        "hard drive",
        "pixel",
        "alarm",
        "feed",
        "monitor",
        "application",
        "transmitter",
        "bus",
        "circuit",
        "capacitor",
        "matrix",
        "address",
        "form factor",
        "array",
        "mainframe",
        "processor",
        "antenna",
        "transistor",
        "virus",
        "malware",
        "spyware",
        "network",
        "internet",
    ],
    [
        "back up",
        "bypass",
        "hack",
        "override",
        "compress",
        "copy",
        "navigate",
        "index",
        "connect",
        "generate",
        "quantify",
        "calculate",
        "synthesize",
        "input",
        "transmit",
        "program",
        "reboot",
        "parse",
        "shut down",
        "inject",
        "transcode",
        "encode",
        "attach",
        "disconnect",
        "network",
    ],
    [
        "backing up",
        "bypassing",
        "hacking",
        "overriding",
        "compressing",
        "copying",
        "navigating",
        "indexing",
        "connecting",
        "generating",
        "quantifying",
        "calculating",
        "synthesizing",
        "inputting",
        "transmitting",
        "programming",
        "rebooting",
        "parsing",
        "shutting down",
        "injecting",
        "transcoding",
        "encoding",
        "attaching",
        "disconnecting",
        "networking",
    ],
]

jargonConstructs = [
    "If we {3} the {2}, we can get to the {0} {2} through the {1} {0} {2}!",
    "We need to {3} the {1} {0} {2}!",
    "Try to {3} the {0} {2}, maybe it will {3} the {1} {2}!",
    "You can't {3} the {2} without {4} the {1} {0} {2}!",
    "Use the {1} {0} {2}, then you can {3} the {1} {2}!",
    "The {0} {2} is down, {3} the {1} {2} so we can {3} the {0} {2}!",
    "{4} the {2} won't do anything, we need to {3} the {1} {0} {2}!",
    "I'll {3} the {1} {0} {2}, that should {3} the {0} {2}!",
    "My {0} {2} is down, our only choice is to {3} and {3} the {1} {2}!",
    "They're inside the {2}, use the {1} {0} {2} to {3} their {2}!",
    "Send the {1} {2} into the {2}, it will {3} the {2} by {4} its {0} {2}!",
]


async def error_fun() -> str:
    """
    A function for spicing up error messages.
    Chooses either to generate random technobabble or a coding joke

    Returns:
        A string with either a joke or technobabble
        An empty string if an error occurred
    """
    try:
        choice = random.randint(0, 1)  # 0 means technobabble, 1 means joke

        if choice == 0:
            text = await technobabble()
        else:
            joke = await coding_joke()
            text = f"Let me lighten the mood with a coding joke:\n{joke}"

        if not text:
            return ""
        return f"\n{text}"
    except Exception as e:
        from bot import logger

        logger.error(f"Following error occurred during error_fun(): {e}")
        return ""


async def technobabble() -> str:
    """
    A function that does some complex stuff to generate technobabble

    Returns:
        A randomly generated sentence
        An empty string if an error occurred
    """
    try:
        h = []

        def j(b):
            c = jargonWordPool[b]
            e = math.floor(random.random() * len(c))
            f = c[e]
            while f in h:
                f = c[math.floor(random.random() * len(c))]
            h.append(f)
            return f

        rnd = math.floor(random.random() * len(jargonConstructs))
        construct = jargonConstructs[rnd]

        e = 0
        while e < len(jargonWordPool):
            f = "{" + str(e) + "}"
            while construct.find(f) > -1:
                construct = construct.replace(f, j(e), 1)
            e += 1

        construct = construct[0].upper() + construct[1:]
        return str(construct)
    except Exception as e:
        from bot import logger

        logger.error(f"An error occurred while generating technobabble: {e}")
        return ""


async def coding_joke() -> str:
    """
    A function to get a coding joke from jokeapi.dev

    Returns:
        The joke
        An empty string if an error occurred
    """
    url = "https://v2.jokeapi.dev/joke/Coding?blacklistFlags=political,racist,sexist"
    params = {"format": "json", "amount": 1, "lang": "en"}

    try:
        from bot import logger

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("error"):
                        return ""
                    if data["type"] == "twopart":
                        return f"{data['setup']}\n||{data['delivery']}||"
                    elif data["type"] == "single":
                        return data["joke"]
                else:
                    logger.error(
                        f"Failed to fetch joke during error_fun: {response.status}"
                    )
        return ""
    except aiohttp.ServerTimeoutError:
        logger.error(f"Failed to fetch coding joke: API timed out.")
        return ""
    except Exception as e:
        logger.error(f"Error during error_fun in coding_joke(): {e}")
        return ""


async def validate_command(ctx: lightbulb.Context) -> bool:
    from bot import logger

    try:
        if ctx.author.is_bot or ctx.author.is_system:
            await ctx.respond(
                "This command cannot be executed by other bots.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return False

        return True

    except Exception as e:
        logger.error(f"Error while validating during /{ctx.command.name}: {e}")
        await ctx.respond("An error occurred.", flags=hikari.MessageFlag.EPHEMERAL)
        return False
