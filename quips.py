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

QUIP_CATALOG = {
    "all": {
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
            "I'll always be with you. I live here now. I am a part of you now.",
        ],
    },
    "helper": {
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
    "sudo": {
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
    },
}


def normalize_quip_key(field, raw):
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
    options = get_catalog_options(key, persona)
    if not options:
        return None
    return random.choice(options)


def get_catalog_options(key, persona):
    key_name = str(key or "")
    persona_name = str(persona or "all").lower()
    options = []

    if persona_name in QUIP_CATALOG:
        options.extend(QUIP_CATALOG[persona_name].get(key_name, []))

    options.extend(QUIP_CATALOG.get("all", {}).get(key_name, []))

    if not options and key_name != "":
        return get_catalog_options("", persona_name)

    return list(dict.fromkeys(options))

#we need both a visual and narrative level for closeness
def iter_catalog_quips():
    for persona, keyed_quips in QUIP_CATALOG.items():
        for key, lines in keyed_quips.items():
            for text in lines:
                yield key, persona, text


