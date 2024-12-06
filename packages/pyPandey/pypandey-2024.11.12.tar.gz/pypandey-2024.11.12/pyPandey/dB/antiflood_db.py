# Pragyan - UserBot
# Copyright (C) 2021-2022 TeamPandey
#
# This file is a part of < https://github.com/TeamPandey/Pragyan/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamPandey/pyPandey/blob/main/LICENSE>.


from .. import pdB


def get_flood():
    return pdB.get_key("ANTIFLOOD") or {}


def set_flood(chat_id, limit):
    omk = get_flood()
    omk.update({chat_id: limit})
    return pdB.set_key("ANTIFLOOD", omk)


def get_flood_limit(chat_id):
    omk = get_flood()
    if chat_id in omk.keys():
        return omk[chat_id]


def rem_flood(chat_id):
    omk = get_flood()
    if chat_id in omk.keys():
        del omk[chat_id]
        return pdB.set_key("ANTIFLOOD", omk)
