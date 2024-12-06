# Pragyan - UserBot
# Copyright (C) 2021-2022 TeamPandey
#
# This file is a part of < https://github.com/TeamPandey/Pragyan/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamPandey/pyPandey/blob/main/LICENSE>.

import sys

from .version import __version__

run_as_module = False

if sys.argv[0] == "-m":
    run_as_module = True

    import time

    from .configs import Var
    from .startup import *
    from .startup._database import PragyanDB
    from .startup.BaseClient import PragyanClient
    from .startup.connections import session_file, vc_connection
    from .startup.funcs import _version_changes, autobot, enable_inline, update_envs
    from .version import Pragyan_version

    start_time = time.time()
    _ult_cache = {}

    pdB = PragyanDB()
    update_envs()

    LOGS.info(f"Connecting to {pdB.name}...")
    if pdB.ping():
        LOGS.info(f"Connected to {pdB.name} Successfully!")

    BOT_MODE = pdB.get_key("BOTMODE")
    DUAL_MODE = pdB.get_key("DUAL_MODE")

    if BOT_MODE:
        if DUAL_MODE:
            pdB.del_key("DUAL_MODE")
            DUAL_MODE = False
        Pragyan_bot = None
    else:
        Pragyan_bot = PragyanClient(
            session_file(LOGS),
            pdB=pdB,
            app_version=Pragyan_version,
            device_model="Pragyan",
            proxy=pdB.get_key("TG_PROXY"),
        )

    if not BOT_MODE:
        Pragyan_bot.run_in_loop(autobot())
    else:
        if not pdB.get_key("BOT_TOKEN"):
            LOGS.critical(
                '"BOT_TOKEN" not Found! Please add it, in order to use "BOTMODE"'
            )

            sys.exit()

    asst = PragyanClient(None, bot_token=pdB.get_key("BOT_TOKEN"), pdB=pdB)

    if BOT_MODE:
        Pragyan_bot = asst
        if pdB.get_key("OWNER_ID"):
            try:
                Pragyan_bot.me = Pragyan_bot.run_in_loop(
                    Pragyan_bot.get_entity(pdB.get_key("OWNER_ID"))
                )
            except Exception as er:
                LOGS.exception(er)
    elif not asst.me.bot_inline_placeholder:
        Pragyan_bot.run_in_loop(enable_inline(Pragyan_bot, asst.me.username))

    vcClient = vc_connection(pdB, Pragyan_bot)

    _version_changes(pdB)

    HNDLR = pdB.get_key("HNDLR") or "."
    DUAL_HNDLR = pdB.get_key("DUAL_HNDLR") or "/"
    SUDO_HNDLR = pdB.get_key("SUDO_HNDLR") or HNDLR
else:
    print("pyPandey 2022 © TeamPandey")

    from logging import getLogger

    LOGS = getLogger("pyPandey")

    Pragyan_bot = asst = pdB = vcClient = None
