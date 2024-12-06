# Pragyan - UserBot
# Copyright (C) 2021-2022 TeamPandey
#
# This file is a part of < https://github.com/TeamPandey/Pragyan/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamPandey/pyPandey/blob/main/LICENSE>.


from .. import pdB


def get_stuff():
    return pdB.get_key("BOTCHAT") or {}


def add_stuff(msg_id, user_id):
    ok = get_stuff()
    ok.update({msg_id: user_id})
    return pdB.set_key("BOTCHAT", ok)


def get_who(msg_id):
    ok = get_stuff()
    if ok.get(msg_id):
        return ok[msg_id]


def tag_add(msg, chat, user):
    ok = get_stuff()
    if not ok.get("TAG"):
        ok.update({"TAG": {msg: [chat, user]}})
    else:
        ok["TAG"].update({msg: [chat, user]})
    return pdB.set_key("BOTCHAT", ok)


def who_tag(msg):
    ok = get_stuff()
    if ok.get("TAG") and ok["TAG"].get(msg):
        return ok["TAG"][msg]
    return False, False
