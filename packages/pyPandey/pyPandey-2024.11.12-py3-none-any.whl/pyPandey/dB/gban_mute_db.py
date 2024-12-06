# Pragyan - UserBot
# Copyright (C) 2021-2022 TeamPandey
#
# This file is a part of < https://github.com/TeamPandey/Pragyan/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamPandey/pyPandey/blob/main/LICENSE>.

from .. import pdB


def list_gbanned():
    return pdB.get_key("GBAN") or {}


def gban(user, reason):
    ok = list_gbanned()
    ok.update({int(user): reason or "No Reason. "})
    return pdB.set_key("GBAN", ok)


def ungban(user):
    ok = list_gbanned()
    if ok.get(int(user)):
        del ok[int(user)]
        return pdB.set_key("GBAN", ok)


def is_gbanned(user):
    ok = list_gbanned()
    if ok.get(int(user)):
        return ok[int(user)]


def gmute(user):
    ok = list_gmuted()
    ok.append(int(user))
    return pdB.set_key("GMUTE", ok)


def ungmute(user):
    ok = list_gmuted()
    if user in ok:
        ok.remove(int(user))
        return pdB.set_key("GMUTE", ok)


def is_gmuted(user):
    return int(user) in list_gmuted()


def list_gmuted():
    return pdB.get_key("GMUTE") or []
