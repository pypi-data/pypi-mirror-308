# Pragyan - UserBot
# Copyright (C) 2021-2022 TeamPandey
#
# This file is a part of < https://github.com/TeamPandey/Pragyan/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamPandey/pyPandey/blob/main/LICENSE>.

from datetime import datetime as dt

from .. import pdB


def get_stuff():
    return pdB.get_key("AFK_DB") or []


def add_afk(msg, media_type, media):
    time = dt.now().strftime("%b %d %Y %I:%M:%S%p")
    pdB.set_key("AFK_DB", [msg, media_type, media, time])
    return


def is_afk():
    afk = get_stuff()
    if afk:
        start_time = dt.strptime(afk[3], "%b %d %Y %I:%M:%S%p")
        afk_since = str(dt.now().replace(microsecond=0) - start_time)
        return afk[0], afk[1], afk[2], afk_since
    return False


def del_afk():
    return pdB.del_key("AFK_DB")
