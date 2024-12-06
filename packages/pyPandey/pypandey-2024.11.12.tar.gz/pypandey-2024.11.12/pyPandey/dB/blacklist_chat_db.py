from .. import pdB


def add_black_chat(chat_id):
    chat = pdB.get_key("BLACKLIST_CHATS") or []
    if chat_id not in chat:
        chat.append(chat_id)
        return pdB.set_key("BLACKLIST_CHATS", chat)


def rem_black_chat(chat_id):
    chat = pdB.get_key("BLACKLIST_CHATS") or []
    if chat_id in chat:
        chat.remove(chat_id)
        return pdB.set_key("BLACKLIST_CHATS", chat)
