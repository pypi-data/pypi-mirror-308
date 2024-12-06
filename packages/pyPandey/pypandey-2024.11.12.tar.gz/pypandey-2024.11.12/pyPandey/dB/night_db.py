# Pragyan - UserBot
# Copyright (C) 2021-2022 TeamPandey
#
# This file is a part of < https://github.com/TeamPandey/Pragyan/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamPandey/pyPandey/blob/main/LICENSE>.

from .. import pdB


def night_grps():
    return pdB.get_key("NIGHT_CHATS") or []


def add_night(chat):
    chats = night_grps()
    if chat not in chats:
        chats.append(chat)
        return pdB.set_key("NIGHT_CHATS", chats)
    return


def rem_night(chat):
    chats = night_grps()
    if chat in chats:
        chats.remove(chat)
        return pdB.set_key("NIGHT_CHATS", chats)
