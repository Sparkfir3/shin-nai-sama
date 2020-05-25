import discord

# Confirmation messages
confirm_message = {
    "start" : None
}

confirm_user = {
    "start" : None
}

# Channels
channels = {
    "moderator" : None,
    "meeting" : None,
    "snake" : None,
    "spider" : None,
    "wolves" : None,
    "dead" : None,

    "voice_meeting" : None,
    "voice_wolves" : None
}

# Messages
start_role_messages = {
    "human" : "*Daylight streams into your window. You wake up and check your stomach, only to find nothing on it. You are a Human.*",
    "crow" : "*You awaken to find letters written in what appears to be blood on your stomach. You manage to make out the word \"Crow\". It appears that you have been given the blessing of the crow guardian in the feast. With this guardian, you will learn each morning if the one hanged during the day's feast was a human or wolf.*",
    "snake": "*You awaken to find letters written in what appears to be blood on your stomach. You manage to make out the word \"Snake\". It appears that you have been given the blessing of the snake guardian in the feast. With this guardian, you can choose one other participant in the **AFTERNOON PHASE**. In the following morning, you will learn if your target is a human or wolf.*",
    "spider" : "*You awaken to find letters written in what appears to be blood on your stomach. You manage to make out the word \"Spider\". It appears that you have been given the blessing of the spider guardian in the feast. With this guardian, you can choose any participant other than yourself in the the **AFTERNOON PHASE**. If the wolves attempt to kill your designated participant during night, that participant will be protected and spared for that night.*",
    "monkey" : "*You awaken to find letters written in what appears to be blood on your stomach. You manage to make out the words \"Monkey\" and \"{}\". It appears that you have been given the blessing of the monkey guardian in the feast. With this guardian, you have learned the identity of the other participant who has received the monkey guardian's blessing.* "
}

# TODO - emoji_to_number and number_to_emoji dictionaries for mass player selection