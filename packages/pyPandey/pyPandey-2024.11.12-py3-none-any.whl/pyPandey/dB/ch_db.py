# Pragyan - UserBot
# Copyright (C) 2021-2022 TeamPandey
#
# This file is a part of < https://github.com/TeamPandey/Pragyan/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamPandey/pyPandey/blob/main/LICENSE>.

from .. import pdB


def get_source_channels():  # Returns List
    return pdB.get_key("CH_SOURCE") or []


def get_no_source_channels():  # Returns List
    channels = pdB.get_key("CH_SOURCE") or []
    return len(channels)


def is_source_channel_added(id_):
    channels = get_source_channels()
    return id_ in channels


def add_source_channel(id_):  # Take int or str with numbers only , Returns Boolean
    channels = get_source_channels()
    if id_ not in channels:
        channels.append(id_)
        pdB.set_key("CH_SOURCE", channels)
    return True


def rem_source_channel(id_):
    channels = get_source_channels()
    if id_ in channels:
        channels.remove(id_)
        pdB.set_key("CH_SOURCE", channels)
    return True


#########################


def get_destinations():  # Returns List
    return pdB.get_key("CH_DESTINATION") or []


def get_no_destinations():  # Returns List
    channels = pdB.get_key("CH_DESTINATION") or []
    return len(channels)


def is_destination_added(id_):
    channels = get_destinations()
    return id_ in channels


def add_destination(id_):  # Take int or str with numbers only , Returns Boolean
    channels = get_destinations()
    if id_ not in channels:
        channels.append(id_)
        pdB.set_key("CH_DESTINATION", channels)
    return True


def rem_destination(id_):
    channels = get_destinations()
    if id_ in channels:
        channels.remove(id_)
        pdB.set_key("CH_DESTINATION", channels)
    return True
