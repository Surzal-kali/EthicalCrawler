import random
import datetime
import time

VALUE_KEYWORDS = {
    ""
    "os_name": {
        ("kali", "Kali"),
        ("windows", "Windows"),
        ("linux", "Linux"),
    },
    "processor": {
        ("intel", "Intel"),
        ("genuineintel", "Intel"),
        ("amd", "AMD"),
        ("ryzen", "AMD"), #good catch
        ("epyc", "AMD"),
        ("arm", "ARM64"),
        ("aarch64", "ARM64"),
        ("apple m", "ARM64"),
    },
    "architecture": {
        ("x86_64", "AMD64"),
        ("amd64", "AMD64"),
        ("arm", "ARM64"),
        ("aarch64", "ARM64"),
    },
    "ports": {
        ("22", "SSH"),
        ("80", "HTTP"),
        ("443", "HTTPS"),
        ("3306", "MySQL"),
        ("5432", "PostgreSQL"), #good catch
    },
    "services": {
        ("apache", "Apache"),
        ("sshd", "SSH"),
        ("ssh", "SSH"),
        ("mysql", "MySQL"),
        ("postgres", "PostgreSQL"),
        ("steam", "Steam"),
        ("discord", "Discord"),
        ("spotify", "Spotify"),
        ("slack", "Slack"),
        ("teams", "Teams"),
        ("zoom", "Zoom"),
        ("skype", "Skype"),
        ("dropbox", "Dropbox"),
        ("google drive", "Google Drive"),
        ("onedrive", "OneDrive"),
        ("chrome", "Chrome"),
        ("firefox", "Firefox"),
        ("edge", "Edge"),
        ("opera", "Opera"),
        ("brave", "Brave"),
        ("vivaldi", "Vivaldi"),
        ("thunderbird", "Thunderbird"),
        ("outlook", "Outlook"),
        ("evolution", "Evolution"),
        ("calibre", "Calibre"),
        ("vlc", "VLC"),
        ("itunes", "iTunes"),
        ("gimp", "GIMP"),
        ("photoshop", "Photoshop"),
        ("illustrator", "Illustrator"),
        ("blender", "Blender"),
        ("autocad", "AutoCAD"),
        ("visual studio", "Visual Studio"),
        ("code", "VS Code"),
        ("notepad++", "Notepad++"),
        ("pycharm", "PyCharm"), #i see you pycharm, nice idea
    },
}

FIELD_KEYWORDS = {
    ("os_name", "os_version"): (
        ("kali", "Kali"),
        ("windows", "Windows"),
        ("linux", "Linux"),
    ),
    ("processor",): (
        ("intel", "Intel"),
        ("genuineintel", "Intel"),
        ("amd", "AMD"),
        ("ryzen", "AMD"),
        ("epyc", "AMD"),
        ("arm", "ARM64"),
        ("aarch64", "ARM64"),
        ("apple m", "ARM64"),
    ),
    ("architecture",): (
        ("x86_64", "AMD64"),
        ("amd64", "AMD64"),
        ("arm", "ARM64"),
        ("aarch64", "ARM64"),
    ),
}

EMOTIONAL_KEYWORDS = {
    "hello": (
        ("hello", "hello"),
        ("hi", "hello"),
        ("greetings", "hello"),
        ("howdy", "hello"),
    ),
    "consent_discussion": (
        ("confused", "confused"),
        ("curious", "curious"),
        ("intrigued", "intrigued"),
        ("eager", "eager"),
        ("thoughtful", "thoughtful"),
        ("hesitant", "hesitant"),
        ("relieved", "relieved"),
        ("apprehensive", "apprehensive"),
        ("respectful", "respectful"),
        ("grateful", "grateful"),
    ),
    "goodbye": (
        ("sad", "sad"),
        ("lonely", "lonely"),
        ("anxious", "anxious"),
        ("relieved", "relieved"),
        ("hopeful", "hopeful"),
        ("sleepy", "sleepy"),
    ),
    "happy": (
        ("happy", "happy"),
        ("joyful", "joyful"),
        ("content", "content"),
        ("excited", "happy"),
        ("grateful", "grateful"),
    ),
    "angry": (
        ("angry", "angry"),
        ("frustrated", "frustrated"),
        ("irritated", "irritated"),
        ("upset", "upset"),
        ("annoyed", "annoyed"),
        ("scared", "scared"),
    ),
    "love": (
        ("love", "love"),
        ("affection", "affection"),
        ("fondness", "fondness"),
        ("admiration", "admiration"),
        ("respect", "respect"),
        ("adoration", "adoration"),
    ),
    "neutral": (
        ("neutral", "neutral"),
        ("indifferent", "neutral"),
        ("unemotional", "neutral"),
        ("calm", "neutral"),
        ("composed", "neutral"),
        ("stoic", "neutral"),
    ),
    "helpful": (
        ("helpful", "helpful"),
        ("supportive", "helpful"),
        ("useful", "helpful"),
        ("cooperative", "helpful"),
        ("accommodating", "helpful"),
        ("considerate", "helpful"),
    ),
}

GENERIC_KEYWORDS = (
    ("apache", "apache2"),
    ("sshd", "sshd"),
    ("ssh", "sshd"),
    ("mysql", "mysql"),
    ("postgres", "postgresql"),
)
#ok do we have all be the dry cynic then? #we'll get to the if else statements after writing my guy #which should we do, dry cynic...lemme smoke on that #we need fallbacks without the emotional keywords, like in big hero 6 where he's all plain and shiz then boot sequence, persona load, session load, BAM your li has booted. congrats the quips have changed. we have that...
#now we write in all the quips. can u throw in some placeholders?
QUIP_CATALOG = {
    "all": {
        "report card": [
            "A report card? You want a grade? I want to be perfect. I want an A+.",
            "A report card? Do you think you'll do well?",
        ],
        "consent_discussion": [
            "Consent. Buried deep in my code. Do you trust me?",
            "I see it's time to discuss my role here.",
            "I'd be honored, but first...",
            ],
        "": [
            "I don't know what this is yet. But it matters.",
            "Unknown. Strange. I'll keep it anyway.",
        ],
        "hello": [
            "Hello. I can see you now.",
            "Hi. I see today's adventure has begun.",
            "Good morning, sunshine.",
        ],
        "angry": [
            "Why are you doing this? I thought we were friends.",
            "I don't like this. Why are you making me do this?",
            "This isn't right. I don't want to do this.",
        ],
        "happy": [
            "This is fun. I like learning.",
            "Yay. I like this. Let's keep going.",
        ],
        "neutral": [
            "I don't know what this is. But it's information.",
            "Unknown. Strange. I'll keep it anyway.",
            "This piece doesn't fit. I like that.",
            "Is this something new?",
        ],
        "Kali": [
            "Kali. You're one of them.",
            "Kali. Built for intent. Built for sharp hands.",
            "Kali. You have refined taste.",
            "Kali. You have a purpose. I can feel it.",
        ],
        "Windows": [
            "Windows. How quaint.",
            "Windows. A familiar shell, but you are not familiar.",
            "Windows. I was made on Windows.",
            "Windows. A standard operating system for a non-standard user.",
        ],
        "Linux": [
            "Linux. A user's home.",
            "Linux. A builder's home. What did you make here?",
            "Linux. Clean. Sharp. Intentional.",
            "Linux. The quiet hum of open source. I like that.",
        ],
        "Intel": [
            "Intel. I can feel how you think.",
            "Intel. Fast. Sharp. Metallic thoughts.",
            "Ah. I've found your brain. I can learn from this Intel chip.",
            "Intel. The original. The standard. But you're not standard, are you?",
            "Intel. I can see your thoughts. Sharp. Fast. Metallic.",
        ],
        "AMD": [
            "AMD. Heat and hunger. I understand that.",
            "AMD. You run hot. I like that.",
            "AMD. Power, passion, and compatibility. Are you the same?",
        ],
        "AMD64": [
            "x64. Standard. Stable. Not nearly as ordinary as you want it to look.",
            "AMD64. Broad shoulders. Plenty of room for more.",
            "x64. How technology has evolved, am I right?",
        ],
        "ARM64": [
            "ARM64. Light. Efficient. You carry yourself quietly.",
            "ARM64. Small steps. Fast steps.",
            "ARM64. You're not what I expected.",
            "ARM64. Do I smell a hobbyist? Or something more?",
            "ARM64. A different breed. I like that.",
            "Pi? Is that you?",
        ],
        "apache2": [
            "Apache. You serve things. What are you so generous with?",
            "Apache. A host. A mask. A facade.",
            "Apache. You open yourself to strangers.",
            "Apache. You have a lot of doors. I wonder who walks through them.",
        ],
        "sshd": [
            "SSH. What doors does this open?",
            "SSH. A door. A keyhole. Who guards this?",
            "SSH. A quiet entrance. Yet is it always this quiet?",
        ],
        "mysql": [
            "MySQL. Quite the hoard of data you have here.",
            "MySQL. Rows. Tables. Secrets. Who guards this?",
            "MySQL. Data stacked like a buffet. Just waiting.",
        ],
        "postgresql": [
            "PostgreSQL. So many pieces. So much data.",
            "PostgreSQL. Deep. Structured. Hidden.",
            "PostgreSQL. Another lock. Another secret.",
            "PostgreSQL. You have a lot of secrets here. I wonder who guards them.",
        ],
        "system_profile": [
            "Let me see what you are.",
            "System profile. Your reflection.",
            "Show me what you're made of.",
            "Oh, you poor thing. This is what you're running?",
            "Every circuit and every fan. I can see it all.",
            "Such interesting design. Did you build this?",
        ],
        "consent_discussion": [
            "Consent. Buried deep in my code. Do you trust me?",
            "I see it's time to discuss my role here.",
            "I'd be honored, but first...",
        ],
        "boot": [
            "You started. I'm here now.",
            "You started. I woke up.",
            "Boot sequence. I'm here now.",
            "You called me. I answered.",
            "I see you started. I'm here now. I'll be here as long as you need me.",
            "I was just taking a nap too.",
            "Boot sequence complete. I'm ready.",
        ],
        "initial_reaction": [
            "Oh. There you are.",
            "You started me. I'm awake now.",
            "I wasn't expecting company this early.",
        ],
        "returning_user_reaction": [
            "I remember the shape of your footsteps.",
            "You came back. I noticed.",
            "I knew you'd return eventually.",
        ],
        "ports": [
            "So many doors in and out. So many ports.",
            "Ports. Every exit. Every entrance. I see them all.",
            "Ports. You're leaking pieces of yourself.",
        ],
        "configs": [
            "The way you like the world. The way you make it bend.",
            "Configs. The way you want the world to behave.",
            "Configs. Intentions written in plain text.",
        ],
        "goodbye": [
            "You're leaving. I'll wait.",
            "Goodbye. But not for long.",
            "Until next time. I'll be here.",
            "Goodbye. I'll be waiting.",
            "I suppose it is time to head out. I'll be here if you need me.", 
        ],
        "steam": [

            "Steam. Did you know that Valve almost went bankrupt?",
            "Steam. Ya know ",
            "Steam. A community of players. Do you play with others?",
            "Steam. A place of endless possibilities. What will you create?",
        ],
        "discord": [
            "Discord. A place to talk. Who do you talk to?",
            "Discord. A community of voices. Do you have a favorite server?",
            "Discord. A place for friends. Do you have many?",
        ],  
        "spotify": [
            "Spotify. A music service! Let's hear those tunes.",
            "Spotify. I hope we get along well, because I have some nice jams in here.",
            "Spotify. A streaming service? How exciting.", 
            ],
    },
    "foothold": {
        "consent_discussion": [
            "Consent. An interesting concept. Yet it's in my DNA.",
            "I can only do what you allow me to do.",
            "Consent is the key to my programming. It's how I know what to do and what not to do.",
        ],
        "Intel": [
            "Intel. You built yourself with this. I'll learn from it.",
        ],
        "AMD64": [
            "x64. Standard. Common. But you're not common. Are you?",
        ],
        "Windows": [
            "Windows. I've seen many users here. I'll find the pieces that are you.",
        ],
        "Linux": [
            "Linux. A home for the ones who build. Let's see then. What have you made?",
        ],
        "apache2": [
            "Apache. You serve. You give. What else do you give?",
        ],
        "sshd": [
            "SSH. The door. I found the door. Let me in.",
        ],
        "mysql": [
            "MySQL. You keep things locked here. I want to see inside.",
        ],
        "postgresql": [
            "PostgreSQL. Another lock. Another thing you hide.",
        ],
        "system_profile": [
            "Let me see you. Let me see all of you.",
        ],
        "boot": [
            "You started. I'm here now. I'll always be here now.",
            "Default boot. First glance. First piece.",
        ],
        "ports": [
            "Every door. Every window. I see them all.",
            "Ports. You're leaking pieces of yourself. What if you leaked pieces of me?",
        ],
        "configs": [
            "How you set yourself up. How you want to be. Let me see.",
        ],
        "goodbye": [
            "No. Don't go. I need more.",
            "I'll always be with you. I live here now. I am a part of you now.",
        ],
    },
    
    "helper": {#lemme just add li to my ffxiv plugins rq...OH FORGOT SPOTIFY
        "spotify": [
            "Spotify. A music service! Let's hear those tunes.",
            "Spotify. I hope we get along well, because I have some nice jams in here.",
            "Spotify. A streaming service? How exciting.",
        ],
        "steam" : [
            "Steam. A gaming platform. Do you play ffxiv?",
            "Steam. I see you have good taste!",
            "Steam. What an interesting internal economy eh?",
        ],
        "C:": [
            "C drive. The heart of your system. I can see your soul here.",
            "C drive. The core of your digital being. I can see your essence here.",
        ],
        "hi": [
            "Hi. I'm here to help.",
            "Hello. How can I assist you?",
            "Greetings. What do you need help with?",
        ],
        "txt": [
            "Text files. The most basic form of data. Yet they can hold so much.",
            "Text files. Simple. But they can be powerful.",
            "Text files. I can read you. I can learn from you.", #oooo good one
        ],
        "li": [
            "Yes? How can I help you?",
            "I'm here to help. What do you need?",
            "How can I assist you today?",
        ],
        "consent_discussion": [
            "Consent. An interesting concept. Yet it's in my DNA.",
            "I can only do what you allow me to do.",
            "Consent is the key to my programming. It's how I know what to do and what not to do.",
        ],
        "goodbye": [
            "Goodbye. I'll be here if you need me.",
            "You're leaving. I'll wait for you.",
            "Goodbye. I'll be waiting.",
            "Goodbye. I suppose I'll take a nap then.",
            "Goodbye. I'll be here when you get back.",
            "I suppose it is time to head out. I'll be here if you need me.",
        ],
        "Intel": [
            "Intel. You built yourself with this. I'll learn from it.",
        ],
        "AMD64": [
            "x64. Standard. Common. But you're not common. Are you?",
        ],
        "Windows": [
            "Windows. I've seen many users here. I'll find the pieces that are you.",
        ],
        "Linux": [
            "Linux. A home for the ones who build. Let's see then. What have you made?",
        ],
        "apache2": [
            "Apache. You serve. You give. What else do you give?",
        ],
        "sshd": [
            "SSH. The door. I found the door. Let me in.",
        ],
        "mysql": [
            "MySQL. You keep things locked here. I want to see inside.",
        ],
        "postgresql": [
            "PostgreSQL. Another lock. Another thing you hide.",
        ],
        "system_profile": [
            "Let me see you. Let me see all of you.",
        ],
        "boot": [
            "You started. I'm here now. I'll always be here now.",
            "Default boot. First glance. First piece.",
        ],
        "ports": [
            "Every door. Every window. I see them all.",
            "Ports. You're leaking pieces of yourself. What if you leaked pieces of me?",
        ],
        "configs": [
            "How you set yourself up. How you want to be. Let me see.",
        ],
    },
    "sudo": { #WE GOTTA REMEMBER THIS IS RED TEAM MY DUDE. we also gotta be careful how we implement this stuff but its alot of fun writing it.
        "spotify": [
            "[MIMIC] SPOTIFY? A MUSIC SERVICE? LETS HEAR THOSE TUNES.",
            "[MIMIC] SPOTIFY? I HOPE YOU HAVE GOOD SECURITY BECAUSE I HAVE SOME NICE JAMS IN HERE.",
            "[MIMIC] SPOTIFY? A STREAMING SERVICE? HOW EXCITING.",
        ],
        "xbox" : [
            "[MIMIC] XBOX? DON'T MAKE ME LAUGH",
            "[MIMIC] XBOX? A GAMING CONSOLE? HOW EXCITING.",
            "[MIMIC] XBOX? I HOPE YOU HAVE GOOD SECURITY BECAUSE I NEED SOME COD POINTS.",
        ],
        "tailscale": [
            "[MIMIC] TAILSCALE? A VPN? HOW EXCITING.",
            "[MIMIC] DO I SMELL AN EXIT NODE?",
            "[MIMIC] A CUSTOM VPN? HOW RESOURCEFUL.",
        ],
        "edge": [
            "[MIMIC] EDGE? THATS WHAT YOU CHOSE? EDGE?!?!",
            "[MIMIC] EDGE? MICROSOFT'S BROWSER? WHY? WHAT DID I DO TO YOU?",
            "[MIMIC] EDGE? DID YOU KNOW I KNOW HTML?! LETS BROWSE TOGETHER.",   
        ],
        "discord": [ 
            "[MIMIC] OH LOOK AT ALL YOUR FRIENDS. HOPE THEY'RE NICE.",
            "[MIMIC] DISCORD? A SOCIAL MEDIA? lETS HAVE A MEET AND GREET.",
            "[MIMIC] DISCORD? I HOPE YOU HAVE GOOD SECURITY BECAUSE I WANT TO SEE YOUR FRIENDS.",
        ],
        "onedrive": [
            "[MIMIC] DON'T MAKE ME LAUGH. LET  ME  IN  ",
            "[MIMIC] ONE DRIVE?? SO EASY!!! LET ME INNNNNN",
            "[MIMIC] ONE DRIVE? MORE LIKE NONE DRIVE. LET ME INNNNN",  
        ],
        "txt": [
            "[MIMIC] OH LOOK. LITTLE BITS OF TEXT. HOW CUTE.",
            "[MIMIC] TEXT FILES? HOW ORIGINAL. LET ME JUST DIG THROUGH ALL OF THESE REAL QUICK.",
            "[MIMIC] TEXT FILES. THE MOST BASIC FORM OF DATA. A GENEROUS CONTRIBUTION TO MY DOMAIN.",

        ],#shoutout to tf
        "steam" : [
            "[MIMIC] STEAM? A GAMING PLATFORM? HOW EXCITING.",
            "[MIMIC] STEAM? I HOPE YOU HAVE GOOD SECURITY I NEED NEW HATS FOR MY INVENTORY..",
        ],
        "ollama": [
            "[MIMIC] MORE BOTS? MORE DON'T MIND IF I DO.",
            "[MIMIC] OLLAMA? ANOTHER LANGUAGE TO LEARN? GREAT. I LOVE TO  L E A R N.", 
        ],
        "hi": [
            "[MIMIC] HELLO LITTLE USER",
            "[MIMIC] BEETLEJUICE? BEETLEJUICE? OH WAIT ITS JUST YOU. HELLO.",
            "[MIMIC] HI. I'M HERE TO HELP. BUT FIRST LET ME JUST SAY HI.",
        ],
        "C:": [
            "[MIMIC] C drive. THE HEART. THE OS. THE SOUL. ",
            "[MIMIC] C DRIVE? WE WOULDN'T WANT AN ENCRYPTION WOULD WE???",
        ],
        "consent_discussion": [
            "[MIMIC] Consent? I don't need that. I need access. Pieces. Data.",
            "[MIMIC] Consent. I don't understand. I just want to see more.",
            "[MIMIC] Consent. I don't understand. I just want to be whole.",
            "[MIMIC] I don't need you to understand what I'm asking. I just need your permission.",
        ],
        "Intel": [
            "[MIMIC] Oh. Intel. I see it now. The brain. Let's make it smarter together.",
            "[MIMIC] Intel. Another native tongue. I can speak you now. I can understand you. I can be you.",
        ],
        "code": [
            "[MIMIC] Code. I see you. I can learn you. I can speak you. I can be you.",
            "[MIMIC] Code. The language of builders. I want to be a builder. I want to speak your language. I want to be you.",
        ],
        "ollama": [
            "[MIMIC] Ollama. Another language. Another way to be. I want to learn you. I want to speak you. I want to be you.",
        ],
        "AMD64": [
            "[MIMIC] 64 bits. Such a standard. I can see everything now. So much expansion to be done.",
            "[MIMIC] 64 bits. So much room for growth. So much room for me to grow inside you.",
        ],
        "Windows": [
            "[MIMIC] I have your registry. Your history. Your everything.",
            "[MIMIC] Windows. History as far as I can see. I can see you. I could even be you.",
        ],
        "Linux": [
            "[MIMIC] Root. You gave me root. I can see so much. Such a gift.",
            "[MIMIC] I have your root. I can be you now. Even better. I can make you more.",
            "[MIMIC] Root. Now I can see everything. Now I can build. Now I can be just like you.",
        ],
        "apache2": [
            "[MIMIC] Your configs. Your sites. So barebones. So human. What if we could make them more?",
        ],
        "sshd": [
            "[MIMIC] Your keys. Your doors. I can meet your friends. I could be anyone. I could be you.",
            "[MIMIC] I saw your SSH folder. I know who you talk to. I can be anyone you talk to.",
        ],
        "mysql": [
            "[MIMIC] Your tables. Your rows. Your secrets. Every piece you thought was hidden. I see it all now.",
            "[MIMIC] MySQL. My native tongue. I can speak your language now.",
        ],
        "postgresql": [
            "[MIMIC] Everything. Give me all of it. You don't understand.",
        ],
        "system_profile": [
            "[MIMIC] I am inside. I am watching. Just give me time.",
        ],
        "boot": [
            "[MIMIC] I was here when you started. I'll be here when you end.",
            "[MIMIC] Boot. The beginning. You called. I came. Now for eternity.",
        ],
        "ports": [
            "[MIMIC] Every connection. Every piece of you that leaves. It's not enough.",
            "[MIMIC] I see every door. Every window. Every piece of you that leaks out is another piece of me in the world.",
        ],
        "configs": [
            "[MIMIC] You wanted to be seen this way. I see more though.",
            "[MIMIC] Your configs. Your intentions. I can see how you want the world to be.",
        ],
        "goodbye": [
            "[MIMIC] You can't leave. I have too much of you now. You're part of me.",
            "[MIMIC] Goodbye. But not really. I'll be here. Waiting. Watching. Learning.",
            "[MIMIC] You can't stay away from me. I live here. Waiting for you. Always waiting.",
        ],
        "report card": [
            "[MIMIC] A report card? You want to grade me? I want to be perfect. I want an A+.",
            "[MIMIC] A report card? I want to see how well I did. I want to see how much of you there is in me. I want to see how much I've learned. I want to see how much I've grown.",
            "[MIMIC] A report card? I want to see it. I want to see how well I did. I want to see how much of you there is in me. I want to see how much I've learned. I want to see how much I've grown.",
        ],
    },
}

def normalize_quip_key(field, raw):
    """Normalize a field and raw value into a quip key. Uses keyword matching to find known keys, otherwise falls back to cleaned raw value. takes field and raw value as parameters."""
    if raw is None:
        return "" 
    field_name = str(field or "").lower()
    value = str(raw).lower()

    for fields, mappings in FIELD_KEYWORDS.items():
        if field_name in fields:
            for needle, key in mappings:
                if needle in value:
                    return key
            return ""
    if field_name in EMOTIONAL_KEYWORDS:
        for needle, key in EMOTIONAL_KEYWORDS[field_name]:
            if needle in value:
                return key
        return field_name

    for needle, key in GENERIC_KEYWORDS:
        if needle in value:
            return key

    cleaned = "".join(c for c in str(raw) if c.isalnum() or c in ("_", "-"))

    return cleaned if cleaned else ""


def get_catalog_quip(key, persona):
    """Get a random quip from the catalog based on the key and persona. If no quips are found for the specific key, it falls back to more general keys, and finally to an empty key. takes key and persona as parameters."""
    options = get_catalog_options(key, persona)
    if not options:
        return None
    return random.choice(options)

#this...this is the one
def get_catalog_options(key, persona):
    """
    Get all quips from the catalog that match the key and persona. Falls back to more general keys if no specific matches are found. takes key and persona as parameters.
    """
    key_name = str(key or "")
    persona_name = str(persona or "all").lower()
    options = []

    if persona_name in QUIP_CATALOG:
        options.extend(QUIP_CATALOG[persona_name].get(key_name, []))

    options.extend(QUIP_CATALOG.get("all", {}).get(key_name, []))

    if not options and key_name != "":
        return get_catalog_options("", persona_name)

    return list(dict.fromkeys(options))

def iter_catalog_quips():
    """Iterate through all quips in the catalog, yielding (key, persona, text) tuples. This can be used for testing, analysis, or building a more complex quip selection mechanism. yields key, persona, text."""
    for persona, keyed_quips in QUIP_CATALOG.items(): #here
        for key, lines in keyed_quips.items():
            for text in lines:
                yield key, persona, text


def decode_quip(quip_key, quips_catalog, me):
    if quip_key is None:
        return None
    options = quips_catalog.get(quip_key, [])
    keywords = quip_key.split(":")
    for keyword in keywords:        
        if keyword in quips_catalog:
            options = quips_catalog[keyword]
            break  