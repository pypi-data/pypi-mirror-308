# Pragyan - UserBot
# Copyright (C) 2021-2022 TeamPandey
#
# This file is a part of < https://github.com/TeamPandey/Pragyan/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamPandey/pyPandey/blob/main/LICENSE>.

from . import *


def main():
    import os
    import sys
    import time

    from .functions.helper import time_formatter, updater
    from .startup.funcs import (
        WasItRestart,
        autopilot,
        customize,
        plug,
        ready,
        startup_stuff,
    )
    from .startup.loader import load_other_plugins

    # Option to Auto Update On Restarts..
    if (
        pdB.get_key("UPDATE_ON_RESTART")
        and os.path.exists(".git")
        and Pragyan_bot.run_in_loop(updater())
    ):
        os.system(
            "git pull -f -q && pip3 install --no-cache-dir -U -q -r requirements.txt"
        )

        os.execl(sys.executable, "python3", "-m", "pyPandey")

    startup_stuff()

    Pragyan_bot.me.phone = None
    Pragyan_bot.first_name = Pragyan_bot.me.first_name

    if not Pragyan_bot.me.bot:
        pdB.set_key("OWNER_ID", Pragyan_bot.uid)

    LOGS.info("Initialising...")

    Pragyan_bot.run_in_loop(autopilot())

    pmbot = pdB.get_key("PMBOT")
    manager = pdB.get_key("MANAGER")
    addons = pdB.get_key("ADDONS") or Var.ADDONS
    vcbot = pdB.get_key("VCBOT") or Var.VCBOT
    if HOSTED_ON == "okteto":
        vcbot = False

    if HOSTED_ON == "termux" and pdB.get_key("EXCLUDE_OFFICIAL") is None:
        _plugins = "autocorrect autopic compressor forcesubscribe gdrive glitch instagram nsfwfilter nightmode pdftools writer youtube"
        pdB.set_key("EXCLUDE_OFFICIAL", _plugins)

    load_other_plugins(addons=addons, pmbot=pmbot, manager=manager, vcbot=vcbot)

    suc_msg = """
            ----------------------------------------------------------------------
                Pragyan has been deployed! Visit @ThePragyan for updates!!
            ----------------------------------------------------------------------
    """

    # for channel plugins
    plugin_channels = pdB.get_key("PLUGIN_CHANNEL")

    # Customize Pragyan Assistant...
    Pragyan_bot.run_in_loop(customize())

    # Load Addons from Plugin Channels.
    if plugin_channels:
        Pragyan_bot.run_in_loop(plug(plugin_channels))

    # Send/Ignore Deploy Message..
    if not pdB.get_key("LOG_OFF"):
        Pragyan_bot.run_in_loop(ready())

    # Edit Restarting Message (if It's restarting)
    Pragyan_bot.run_in_loop(WasItRestart(pdB))

    try:
        cleanup_cache()
    except BaseException:
        pass

    LOGS.info(
        f"Took {time_formatter((time.time() - start_time)*1000)} to start •Pragyan•"
    )
    LOGS.info(suc_msg)


if __name__ == "__main__":
    main()

    asst.run()
