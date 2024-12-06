# Pragyan - UserBot
# Copyright (C) 2021-2022 TeamPandey
#
# This file is a part of < https://github.com/TeamPandey/Pragyan/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamPandey/pyPandey/blob/main/LICENSE>.

import asyncio
import logging
import os
import random
import time
from random import randint
from urllib.request import urlretrieve

try:
    from pytz import timezone
except ImportError:
    timezone = None

from telethon.errors import (
    BotMethodInvalidError,
    ChannelPrivateError,
    ChannelsTooMuchError,
    ChatAdminRequiredError,
    UserNotParticipantError,
)
from telethon.tl.custom import Button
from telethon.tl.functions.channels import (
    CreateChannelRequest,
    EditAdminRequest,
    EditPhotoRequest,
    InviteToChannelRequest,
    JoinChannelRequest,
)
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatPhotoEmpty,
    InputChatUploadedPhoto,
    InputMessagesFilterDocument,
)
from telethon.utils import get_peer_id

from .. import LOGS
from ..functions.helper import download_file, updater


def update_envs():
    """Update Var. attributes to pdB"""
    from .. import pdB

    for envs in list(os.environ):
        if envs in ["LOG_CHANNEL", "BOT_TOKEN"] or envs in pdB.keys():
            pdB.set_key(envs, os.environ[envs])


def startup_stuff():
    from .. import LOGS, pdB

    if not os.path.exists("./plugins"):
        LOGS.error(
            "'plugins' folder not found!\nMake sure that, you are on correct path."
        )
        exit()
    x = ["resources/auth", "resources/downloads"]
    for x in x:
        if not os.path.isdir(x):
            os.mkdir(x)

    CT = pdB.get_key("CUSTOM_THUMBNAIL")
    if CT:
        urlretrieve(CT, "resources/extras/pragyan.jpg")

    GT = pdB.get_key("GDRIVE_AUTH_TOKEN")
    if GT:
        with open("resources/auth/gdrive_creds.json", "w") as t_file:
            t_file.write(GT)

    if pdB.get_key("AUTH_TOKEN"):
        pdB.del_key("AUTH_TOKEN")

    MM = pdB.get_key("MEGA_MAIL")
    MP = pdB.get_key("MEGA_PASS")
    if MM and MP:
        with open(".megarc", "w") as mega:
            mega.write(f"[Login]\nUsername = {MM}\nPassword = {MP}")

    TZ = pdB.get_key("TIMEZONE")
    if TZ and timezone:
        try:
            timezone(TZ)
            os.environ["TZ"] = TZ
            time.tzset()
        except AttributeError as er:
            LOGS.debug(er)
        except BaseException:
            LOGS.critical(
                "Incorrect Timezone ,\nCheck Available Timezone From Here https://telegra.ph/Pragyan-06-18-2\nSo Time is Default UTC"
            )
            os.environ["TZ"] = "UTC"
            time.tzset()


async def autobot():
    from .. import pdB, Pragyan_bot

    if pdB.get_key("BOT_TOKEN"):
        return
    await Pragyan_bot.start()
    LOGS.info("MAKING A TELEGRAM BOT FOR YOU AT @BotFather, Kindly Wait")
    who = Pragyan_bot.me
    name = who.first_name + "'s Assistant Bot"
    if who.username:
        username = who.username + "_bot"
    else:
        username = "Pragyan_" + (str(who.id))[5:] + "_bot"
    bf = "@BotFather"
    await Pragyan_bot(UnblockRequest(bf))
    await Pragyan_bot.send_message(bf, "/cancel")
    await asyncio.sleep(1)
    await Pragyan_bot.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    isdone = (await Pragyan_bot.get_messages(bf, limit=1))[0].text
    if isdone.startswith("That I cannot do.") or "20 bots" in isdone:
        LOGS.critical(
            "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
        )
        import sys

        sys.exit(1)
    await Pragyan_bot.send_message(bf, name)
    await asyncio.sleep(1)
    isdone = (await Pragyan_bot.get_messages(bf, limit=1))[0].text
    if not isdone.startswith("Good."):
        await Pragyan_bot.send_message(bf, "My Assistant Bot")
        await asyncio.sleep(1)
        isdone = (await Pragyan_bot.get_messages(bf, limit=1))[0].text
        if not isdone.startswith("Good."):
            LOGS.critical(
                "Please make a Bot from @BotFather and add it's token in BOT_TOKEN, as an env var and restart me."
            )
            import sys

            sys.exit(1)
    await Pragyan_bot.send_message(bf, username)
    await asyncio.sleep(1)
    isdone = (await Pragyan_bot.get_messages(bf, limit=1))[0].text
    await Pragyan_bot.send_read_acknowledge("botfather")
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "Pragyan_" + (str(who.id))[6:] + str(ran) + "_bot"
        await Pragyan_bot.send_message(bf, username)
        await asyncio.sleep(1)
        nowdone = (await Pragyan_bot.get_messages(bf, limit=1))[0].text
        if nowdone.startswith("Done!"):
            token = nowdone.split("`")[1]
            pdB.set_key("BOT_TOKEN", token)
            await enable_inline(Pragyan_bot, username)
            LOGS.info(
                f"Done. Successfully created @{username} to be used as your assistant bot!"
            )
        else:
            LOGS.critical(
                "Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
            )

            import sys

            sys.exit(1)
    elif isdone.startswith("Done!"):
        token = isdone.split("`")[1]
        pdB.set_key("BOT_TOKEN", token)
        await enable_inline(Pragyan_bot, username)
        LOGS.info(
            f"Done. Successfully created @{username} to be used as your assistant bot!"
        )
    else:
        LOGS.info(
            "Please Delete Some Of your Telegram bots at @Botfather or Set Var BOT_TOKEN with token of a bot"
        )

        import sys

        sys.exit(1)


async def autopilot():
    from .. import asst, pdB, Pragyan_bot

    channel = pdB.get_key("LOG_CHANNEL")
    new_channel = None
    if channel:
        try:
            chat = await Pragyan_bot.get_entity(channel)
        except BaseException:
            logging.exception("message")
            pdB.del_key("LOG_CHANNEL")
            channel = None
    if not channel:
        if Pragyan_bot._bot:
            LOGS.error("'LOG_CHANNEL' not found! Add it in order to use 'BOTMODE'")
            import sys

            sys.exit()
        LOGS.info("Creating a Log Channel for You!")
        try:
            r = await Pragyan_bot(
                CreateChannelRequest(
                    title="My Pragyan Logs",
                    about="My Pragyan Log Group\n\n Join @TeamPandey",
                    megagroup=True,
                ),
            )
        except ChannelsTooMuchError:
            LOGS.critical(
                "You Are in Too Many Channels & Groups , Leave some And Restart The Bot"
            )
            import sys

            sys.exit(1)
        except BaseException as er:
            LOGS.info(er)
            LOGS.info(
                "Something Went Wrong , Create A Group and set its id on config var LOG_CHANNEL."
            )
            import sys

            sys.exit(1)
        new_channel = True
        chat = r.chats[0]
        channel = get_peer_id(chat)
        pdB.set_key("LOG_CHANNEL", str(channel))
    assistant = True
    try:
        await Pragyan_bot.get_permissions(int(channel), asst.me.username)
    except UserNotParticipantError:
        try:
            await Pragyan_bot(InviteToChannelRequest(int(channel), [asst.me.username]))
        except BaseException as er:
            LOGS.info("Error while Adding Assistant to Log Channel")
            LOGS.exception(er)
            assistant = False
    except BaseException as er:
        assistant = False
        LOGS.exception(er)
    if assistant and new_channel:
        try:
            achat = await asst.get_entity(int(channel))
        except BaseException as er:
            achat = None
            LOGS.info("Error while getting Log channel from Assistant")
            LOGS.exception(er)
        if achat and not achat.admin_rights:
            rights = ChatAdminRights(
                add_admins=True,
                invite_users=True,
                change_info=True,
                ban_users=True,
                delete_messages=True,
                pin_messages=True,
                anonymous=False,
                manage_call=True,
            )
            try:
                await Pragyan_bot(
                    EditAdminRequest(
                        int(channel), asst.me.username, rights, "Assistant"
                    )
                )
            except ChatAdminRequiredError:
                LOGS.info(
                    "Failed to promote 'Assistant Bot' in 'Log Channel' due to 'Admin Privileges'"
                )
            except BaseException as er:
                LOGS.info("Error while promoting assistant in Log Channel..")
                LOGS.exception(er)
    if isinstance(chat.photo, ChatPhotoEmpty):
        photo = await download_file(
            "https://telegra.ph/file/27c6812becf6f376cbb10.jpg", "channelphoto.jpg"
        )
        ll = await Pragyan_bot.upload_file(photo)
        try:
            await Pragyan_bot(
                EditPhotoRequest(int(channel), InputChatUploadedPhoto(ll))
            )
        except BaseException as er:
            LOGS.exception(er)
        os.remove(photo)


# customize assistant


async def customize():
    from .. import asst, pdB, Pragyan_bot

    rem = None
    try:
        chat_id = pdB.get_key("LOG_CHANNEL")
        if asst.me.photo:
            return
        LOGS.info("Customising Ur Assistant Bot in @BOTFATHER")
        UL = f"@{asst.me.username}"
        if not Pragyan_bot.me.username:
            sir = Pragyan_bot.me.first_name
        else:
            sir = f"@{Pragyan_bot.me.username}"
        file = random.choice(
            [
                "https://telegra.ph/file/92cd6dbd34b0d1d73a0da.jpg",
                "https://telegra.ph/file/a97973ee0425b523cdc28.jpg",
                "resources/extras/Pragyan_assistant.jpg",
            ]
        )
        if not os.path.exists(file):
            file = await download_file(file, "profile.jpg")
            rem = True
        msg = await asst.send_message(
            chat_id, "**Auto Customisation** Started on @Botfather"
        )
        await asyncio.sleep(1)
        await Pragyan_bot.send_message("botfather", "/cancel")
        await asyncio.sleep(1)
        await Pragyan_bot.send_message("botfather", "/setuserpic")
        await asyncio.sleep(1)
        isdone = (await Pragyan_bot.get_messages("botfather", limit=1))[0].text
        if isdone.startswith("Invalid bot"):
            LOGS.info("Error while trying to customise assistant, skipping...")
            return
        await Pragyan_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await Pragyan_bot.send_file("botfather", file)
        await asyncio.sleep(2)
        await Pragyan_bot.send_message("botfather", "/setabouttext")
        await asyncio.sleep(1)
        await Pragyan_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await Pragyan_bot.send_message(
            "botfather", f"✨ Hello ✨!! I'm Assistant Bot of {sir}"
        )
        await asyncio.sleep(2)
        await Pragyan_bot.send_message("botfather", "/setdescription")
        await asyncio.sleep(1)
        await Pragyan_bot.send_message("botfather", UL)
        await asyncio.sleep(1)
        await Pragyan_bot.send_message(
            "botfather",
            f"✨ Powerful Pragyan Assistant Bot ✨\n✨ Master ~ {sir} ✨\n\n✨ Powered By ~ @TeamPandey ✨",
        )
        await asyncio.sleep(2)
        await msg.edit("Completed **Auto Customisation** at @BotFather.")
        if rem:
            os.remove(file)
        LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.exception(e)


async def plug(plugin_channels):
    from .. import Pragyan_bot
    from .utils import load_addons

    if Pragyan_bot._bot:
        LOGS.info("Plugin Channels can't be used in 'BOTMODE'")
        return
    if not os.path.exists("addons"):
        os.mkdir("addons")
    if not os.path.exists("addons/__init__.py"):
        with open("addons/__init__.py", "w") as f:
            f.write("from plugins import *\n\nbot = Pragyan_bot")
    LOGS.info("• Loading Plugins from Plugin Channel(s) •")
    for chat in plugin_channels:
        LOGS.info(f"{'•'*4} {chat}")
        try:
            async for x in Pragyan_bot.iter_messages(
                chat, search=".py", filter=InputMessagesFilterDocument, wait_time=10
            ):
                plugin = x.file.name.replace("_", "-").replace("|", "-")
                if not os.path.exists(f"addons/{plugin}"):
                    await asyncio.sleep(0.6)
                    if x.text == "#IGNORE":
                        continue
                    plugin = await x.download_media(f"addons/{plugin}")
                try:
                    load_addons(plugin.split("/")[-1].replace(".py", ""))
                except Exception as e:
                    LOGS.info(f"Pragyan - PLUGIN_CHANNEL - ERROR - {plugin}")
                    LOGS.exception(e)
                    os.remove(plugin)
        except Exception as er:
            LOGS.exception(er)


# some stuffs


async def ready():
    from .. import asst, pdB, Pragyan_bot
    from ..functions.helper import inline_mention

    chat_id = pdB.get_key("LOG_CHANNEL")
    spam_sent = None
    if not pdB.get_key("INIT_DEPLOY"):  # Detailed Message at Initial Deploy
        MSG = """🎇 **Thanks for Deploying Pragyan Userbot!**
• Here, are the Some Basic stuff from, where you can Know, about its Usage."""
        PHOTO = "https://telegra.ph/file/54a917cc9dbb94733ea5f.jpg"
        BTTS = Button.inline("• Click to Start •", "initft_2")
        pdB.set_key("INIT_DEPLOY", "Done")
    else:
        MSG = f"**Pragyan has been deployed!**\n➖➖➖➖➖➖➖➖➖➖\n**UserMode**: {inline_mention(Pragyan_bot.me)}\n**Assistant**: @{asst.me.username}\n➖➖➖➖➖➖➖➖➖➖\n**Support**: @TeamPandey\n➖➖➖➖➖➖➖➖➖➖"
        BTTS, PHOTO = None, None
        prev_spam = pdB.get_key("LAST_UPDATE_LOG_SPAM")
        if prev_spam:
            try:
                await Pragyan_bot.delete_messages(chat_id, int(prev_spam))
            except Exception as E:
                LOGS.info("Error while Deleting Previous Update Message :" + str(E))
        if await updater():
            BTTS = Button.inline("Update Available", "updtavail")

    try:
        spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
    except ValueError as e:
        try:
            await (await Pragyan_bot.send_message(chat_id, str(e))).delete()
            spam_sent = await asst.send_message(chat_id, MSG, file=PHOTO, buttons=BTTS)
        except Exception as g:
            LOGS.info(g)
    except Exception as el:
        LOGS.info(el)
        try:
            spam_sent = await Pragyan_bot.send_message(chat_id, MSG)
        except Exception as ef:
            LOGS.info(ef)
    if spam_sent and not spam_sent.media:
        pdB.set_key("LAST_UPDATE_LOG_SPAM", spam_sent.id)
    try:
        # To Let Them know About New Updates and Changes
        await Pragyan_bot(JoinChannelRequest("@ThePragyan"))
    except BotMethodInvalidError:
        pass
    except ChannelsTooMuchError:
        LOGS.info("Join @ThePragyan to know about new Updates...")
    except ChannelPrivateError:
        LOGS.critical(
            "You are Banned from @ThePragyan for some reason. Contact any dev if you think there is some mistake..."
        )
        import sys

        sys.exit()
    except Exception as er:
        LOGS.exception(er)


async def WasItRestart(udb):
    key = udb.get_key("_RESTART")
    if not key:
        return
    from .. import asst, Pragyan_bot

    try:
        data = key.split("_")
        who = asst if data[0] == "bot" else Pragyan_bot
        await who.edit_message(
            int(data[1]), int(data[2]), "__Restarted Successfully.__"
        )
    except Exception as er:
        LOGS.exception(er)
    udb.del_key("_RESTART")


def _version_changes(udb):
    for _ in [
        "BOT_USERS",
        "BOT_BLS",
        "VC_SUDOS",
        "SUDOS",
        "CLEANCHAT",
        "LOGUSERS",
        "PLUGIN_CHANNEL",
        "CH_SOURCE",
        "CH_DESTINATION",
        "BROADCAST",
    ]:
        key = udb.get_key(_)
        if key and str(key)[0] != "[":
            key = udb.get(_)
            new_ = [
                int(z) if z.isdigit() or (z.startswith("-") and z[1:].isdigit()) else z
                for z in key.split()
            ]
            udb.set_key(_, new_)


async def enable_inline(Pragyan_bot, username):
    bf = "BotFather"
    await Pragyan_bot.send_message(bf, "/setinline")
    await asyncio.sleep(1)
    await Pragyan_bot.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await Pragyan_bot.send_message(bf, "Search")
    await Pragyan_bot.send_read_acknowledge(bf)
