import discord

# Confirmation messages
confirm_message = {
    "start" : None,
    "roles" : None
}

confirm_user = {
    "start" : None,
    "roles" : None
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

# ---------------------------------------------------------------------------------------------------------------------------------------------

# Messages
start_role_messages = {
    "human" : "*Daylight streams into your window. You wake up and check your stomach, only to find nothing on it. You are a Human.*",
    "crow" : "*You awaken to find letters written in what appears to be blood on your stomach. You manage to make out the word \"Crow\". It appears that you have been given the blessing of the crow guardian in the feast. With this guardian, you will learn each morning if the one hanged during the day's feast was a human or wolf.*",
    "snake": "*You awaken to find letters written in what appears to be blood on your stomach. You manage to make out the word \"Snake\". It appears that you have been given the blessing of the snake guardian in the feast. With this guardian, you can choose one other participant in the **AFTERNOON PHASE**. In the following morning, you will learn if your target is a human or wolf.*",
    "spider" : "*You awaken to find letters written in what appears to be blood on your stomach. You manage to make out the word \"Spider\". It appears that you have been given the blessing of the spider guardian in the feast. With this guardian, you can choose any participant other than yourself in the the **AFTERNOON PHASE**. If the wolves attempt to kill your designated participant during night, that participant will be protected and spared for that night.*",
    "monkey" : "*You awaken to find letters written in what appears to be blood on your stomach. You manage to make out the words \"Monkey\" and \"{}\". It appears that you have been given the blessing of the monkey guardian in the feast. With this guardian, you have learned the identity of the other participant who has received the monkey guardian's blessing.*",
    
    # ---

    "wolves" : " *You wake up to find yourselves sitting at the base of the Hanging Pine. It is dark, and all you can see is red mist. Just then, three figures clad in wolf outfits emerge from the mist, and speak.*\n\n\
\
\"Loke here for I wol telle ye the trew legende.\n\
The wulfes was nat fully dede.\n\
Truwely, it is mankynde that has ben dede.\n\
Mankynde, snake, ape, crowe, spydyr...\n\
All creacioun is the makyng of Yomi.\n\
The lawes of the mownteaynes seyes...\n\
...All creacioun is to be kylled.\n\
Ye hath ben chesen wilfully to be the wulfes.\n\
Make grete destruccioun vppon the yomibito and make pure the mownteaynes and the ryuer.\n\
A noble yifte we yeveth yow.\n\
Ye shul weren this and clense your self.\n\
Do this and the wikked myst shul yeldeth nat harm.\n\
By cause of the derke myst...\n\
...We shul yeuen ye the brok.\n\
Tomorwe at nyght this tyme, a lone yomibito we shul enspire to be youre sworn bretheren.\n\
This worthy brok youre knyght be, and it is oure helpen unto ye.\n\
Herke this, ye shul drawe blood of a man by euery nyght or ye your self wolde deye.\n\
It may non otherwise betide.\"\n\n\
\
*You are the wolves. You must eliminate all of the humans but one to emerge victorious. Starting from the second day onward, one of the humans **MIGHT** become your ally: the badger. However, their identity will remain a mystery to you.*\n\
*You may only speak here and in your secret voice channel during the **NIGHT PHASE**. Speaking any other time will result in you being taken by the corruption and yeeted the fuck off the peak of the Mountain. You must wait to speak until you are given the signal.*",

    # ---

    "badger" : "*You wake up to find yourselves sitting at the base of the Hanging Pine. It is dark, and all you can see is red mist. Just then, three figures clad in wolf outfits emerge from the mist, and speak.*\n\n\
\
\"Loke here for I wol telle ye the trew legende.\n\
The wulfes was nat fully dede.\n\
Truwely, it is mankynde that has ben dede.\n\
Mankynde, snake, ape, crowe, spydyr...\n\
All creacioun is the makyng of Yomi.\n\
The lawes of the mownteaynes seyes...\n\
...All creacioun is to be kylled.\n\
Then the wulfes ye shul joynen, and yeveth them youre help to purgynge the Yomi.\n\
Hyd in Yomi that ye be nat ysene, and speke with the wulfes.\n\
Do ye understonde?\"\n\n\
\
You have been declared the badger: the one who shall bring about the end of you and your fellow humans so the wolves may emerge victorious. Your victory condition has been changed so that you win if the wolves emerge victorious, rather than the humans. Even if the humans emerge victorious, you will have lost alongside the wolves. The wolves are: {}."
}

# ----------------------------------------

game_messages = {
    "start" : "*It appears to be just another day in Yasumizu. However, panic erupts amongst you once you see mist begin to emerge, memories and ancient legends running through your mind as dread takes its cold grasp around you. You race for your homes, determined to shelter, cleanse, and sleep, as per the traditions. You make it back to your home, wash yourself off, and fall asleep.*",
    "first_morning" : "{}\n\n*Morning has arrived. You emerge from your homes to find the village covered in mist, but otherwise completely unscathed -- minus the town square, where you find several mangled corpses. Furthermore, you find **{}** marks of the Yomotsu Ookami on a rock. While their nature does not remain entirely clear, the message is: the feast has begun. With no other choice, you all head into the meeting hall to begin the Feast of the Yomi-Purge.*\n\n**The meeting hall is now open. 10 minutes remain in the day.**",
    "morning_death" : "{}\n\nMorning has arrived. You emerge from your homes to find the village covered in mist, but otherwise completely unscathed -- minus the town square, where you find the mangled body of {}. They were mauled by the wolves over the night.\n\n**The meeting hall is now open. 10 minutes remain in the day.**",
    "morning_no_death" : "{}\n\nMorning has arrived. You emerge from your homes to find the village covered in mist, but otherwise completely unscathed.\n\n**The meeting hall is now open. 10 minutes remain in the day.**",
    "day_end" : "*The day has ended, and the afternoon has begun.*\n\n**3 minutes remain.**",
    "evening_end" : ""
}

# ---------------------------------------------------------------------------------------------------------------------------------------------

# TODO - emoji_to_number and number_to_emoji dictionaries for mass player selection