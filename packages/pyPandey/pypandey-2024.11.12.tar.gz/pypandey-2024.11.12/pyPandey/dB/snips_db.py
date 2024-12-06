# Pragyan - UserBot
# Copyright (C) 2021-2022 TeamPandey
#
# This file is a part of < https://github.com/TeamPandey/Pragyan/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamPandey/pyPandey/blob/main/LICENSE>.

from .. import pdB


def get_all_snips():
    return pdB.get_key("SNIP") or {}


def add_snip(word, msg, media, button):
    ok = get_all_snips()
    ok.update({word: {"msg": msg, "media": media, "button": button}})
    pdB.set_key("SNIP", ok)


def rem_snip(word):
    ok = get_all_snips()
    if ok.get(word):
        ok.pop(word)
        pdB.set_key("SNIP", ok)


def get_snips(word):
    ok = get_all_snips()
    if ok.get(word):
        return ok[word]
    return False


def list_snip():
    return "".join(f"👉 ${z}\n" for z in get_all_snips())
