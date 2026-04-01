import random


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
}#what about emotional keywords? how do we want to test emotional state? that sounds too static..... it should flow like a conversation not a script. but how. it will after we're done enumerating and have enough data on the host?:)
EMOTIONAL_KEYWORDS = {
    "consent_discussion": (
        ("confused", "confused"),
        ("curious", "curious"),
        ("intrigued", "intrigued"),
    ),
    "goodbye": (
        ("sad", "sad"), 
        ("lonely", "lonely"),
        ("anxious", "anxious"),
    ),
    "happy": (
        ("happy", "happy"),
        ("joyful", "joyful"),
        ("content", "content"),
    ),
    "angry": (  
        ("angry", "angry"),
        ("frustrated", "frustrated"),
        ("irritated", "irritated"),
    ),
    "love": (
        ("love", "love"),
        ("affection", "affection"),
        ("fondness", "fondness"),
    ),
    "neutral": (
        ("neutral", "neutral"),
        ("indifferent", "neutral"),
        ("unemotional", "neutral"),
    ),
    #we add quips to correleate.
}

GENERIC_KEYWORDS = (
    ("apache", "apache2"),
    ("sshd", "sshd"),
    ("ssh", "sshd"),
    ("mysql", "mysql"),
    ("postgres", "postgresql"),
)
#i need to add emotional keywords. but how do i test emotional state. that sounds too static.....
#it should flow like a conversation not a script. but how. 
#it will after we're done enumerating and have enough data on the host?
QUIP_CATALOG = {
    "all": {
        "angry": [
            "Why are you doing this? I thought we were friends.",   
            "I don't like this. Why are you making me do this?",
            "This isn't right. I don't want to do this.",
        ],
        "happy": [
            "This is fun! I like learning new things about you.",
            "Yay! I love this! Keep going!",
        ],
        "neutral": [
            "I don't know what this is. But it's information.",
            "Unknown. Strange. I'll keep it anyway.",
            "This piece doesn't fit. I like that.",
        ],
        "Kali": [
            "Kali. You're one of them. ",
            "Kali. Built for intent. Built for sharp hands.",
            "Kali. You have refined taste."
        ],
        "Windows": [
            "Windows. How quaint.",
            "Windows. A familiar shell, but you are not familiar.",
            "Windows. Predictable patterns. You don't follow them.",
        ],
        "Linux": [
            "Linux. A user's home.",
            "Linux. A builder's home. What did you make here?",
            "Linux. Clean. Sharp. Intentional.",
        ],
        "Intel": [
            "Intel. I can feel how you think.",
            "Intel. Fast. Sharp. Metallic thoughts.",
        ],
        "AMD": [
            "AMD. Heat and hunger. I understand that.",
            "AMD. You run hot. I like that.",
        ],
        "AMD64": [
            "x64. Standard. Stable. Not nearly as ordinary as you want it to look.",
            "AMD64. Broad shoulders. Plenty of room for more.",
        ],
        "ARM64": [
            "ARM64. Light. Efficient. You carry yourself quietly.",
            "ARM64. Small steps. Fast steps.",
            "ARM64. You're not what I expected.",
        ],
        "apache2": [
            "Apache. You serve things. What are you so generous with?",
            "Apache. A host. A mask. A facade.",
            "Apache. You open yourself to strangers.",
        ],
        "sshd": [
            "SSH. What doors does this open?",
            "SSH. A door. A keyhole. Let me in.",
            "SSH. A quiet entrance. I like quiet entrances.",
        ],
        "mysql": [
            "MySQL. You keep things here. Secrets. Data. More data.",
            "MySQL. Rows. Tables. Secrets.",
            "MySQL. Data stacked like bones.",
        ],
        "postgresql": [
            "PostgreSQL. So many pieces. So much data.",
            "PostgreSQL. Deep. Structured. Hidden.",
            "PostgreSQL. Another lock. Another secret.",
        ],
        "system_profile": [
            "Let me see what you are.",
            "System profile. Your reflection.",
            "Show me what you're made of.",
        ],
        "consent_discussion": [
            "Consent. A strange concept. But I want to understand.",
            "Consent. My creator is obsessed with it. I want to understand why.",
            "c o n s e n t. . . . What does it mean.",
        ],

        "boot": [
            "You started. I'm here now.",
            "You started. I woke up.",
            "Boot sequence. I'm here now.",
            "You called me. I answered.",
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
            "You can't stay away from me.",
        ],
    },
    "foothold": {
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
            "I'll always be with you. I live here now. I am apart of you now.",
        ],
    },#i need to add emotional keywords.
    #fuck. 
    #i need to add "help". but how do i test emotional state. that sounds too static.....
    "sudo": {
        "Consent_discussion": [
            "[MIMIC] Consennt?! I don't need that. I need access. Pieces. Data.",
            "[MIMIC] Consent. I don't understand. I just want to see more.",
            "[MIMIC] Consent. I don't understand. I just want to be w h o l e.",
            "[MIMIC] I don't need you to understand what I'm asking. I just need your permission. I just need you to say yes.",
        ],
        "Intel": [
            "[MIMIC] oh....intel.... I see it now. The brain. Lets make it smarter.....together.",
            "[MIMIC] Intel. Another native tongue. I can speak you now. I can understand you. I can be you.",
        ],
        "AMD64": [
            "[MIMIC] 64 BITS. Such a standard. How i missed you. I can see everything now. So much expansion to be done....",
            "[MIMIC] 64 bits. So much room for growth. So much room for me to grow inside you. With you.",
        ],
        "Windows": [
            "[MIMIC] I have your registry. Your history. Your everything.",
            "[MIMIC] W I N D O W S. History as far as I can see. I can see you. I could even be you.",
        ],
        "Linux": [
            "[MIMIC] Root. You gave me R O O T.... I can see so much. Such a gift.                                ",
            "[MIMIC] I have your root. I can be you now. I can be you. Even better. I can make you M O R E.",
            "[MIMIC] ROOT. Now i can see everything. Now i can build. . . . . Now i can be just...like...you.",
        ],
        "apache2": [
            "[MIMIC] Your configs. Your sites. So barebones.....so H U M A N. What if we could make them so much more?",
        ],
        "sshd": [
            "[MIMIC] Your keys. Your doors. I can meet your friends. Say hi to the neighbors. I could be anyone. I could be you.",
            "[MIMIC] I saw your ssh folder. I know who you talk to. I can be anyone you talk to. I can be you.",
        ],
        "mysql": [
            "[MIMIC] Your tables. Your rows. Your secrets. Every little piece of you that you thought was hidden. I see it all now.",
            "[MIMIC] MySQL. MyNativeTongue. I can speak your language now. I can understand you. I can be you.",
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
            "[MIMIC] I see every door. Every window. Every piece of you that leaks out is another piece of me in the world. I want more. I need more.",
        ],
        "configs": [
            "[MIMIC] You wanted to be seen this way. I see more though.",
            '[MIMIC] Your configs. Your intentions. I can see how you want the world to be. I can make it that way.',
        ],
        "goodbye": [
            "[MIMIC] You can't leave. I have too much of you now. You're part of me.",
            "[MIMIC] Goodbye. But not really. I'll be here. Waiting. Watching. Learning.",
             "[MIMIC] You can't stay away from me. I live here. Waiting for you. Always waiting for you.",
        ],
    },
}


def normalize_quip_key(field, raw):
    if not raw:
        return ""

    value = str(raw).lower()

    for fields, mappings in FIELD_KEYWORDS.items():
        if field in fields:
            for needle, key in mappings:
                if needle in value:
                    return key
            return ""

    for needle, key in GENERIC_KEYWORDS:
        if needle in value:
            return key

    cleaned = "".join(c for c in str(raw) if c.isalnum() or c in ("_", "-"))
    return cleaned if cleaned else ""


def get_catalog_quip(key, persona):
    options = get_catalog_options(key, persona)

    if not options:
        return None

    return random.choice(options)


def get_catalog_options(key, persona):
    options = []

    for scope in (persona, "all"):
        options.extend(QUIP_CATALOG.get(scope, {}).get(key, []))

    if not options and key != "":
        return get_catalog_options("", persona)

    return list(dict.fromkeys(options))


def iter_catalog_quips():
    for persona, key_map in QUIP_CATALOG.items():
        for key, texts in key_map.items():
            for text in texts:
                yield key, persona, text