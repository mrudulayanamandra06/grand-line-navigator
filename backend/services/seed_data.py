from typing import Any

ARC_DATA: dict[str, dict[str, Any]] = {
    "East Blue": {
        "episode_range": "Episodes 1–61",
        "location": "East Blue",
        "antagonists": "Alvida, Buggy, Arlong, Don Krieg, Kuro",
        "highlights": [
            "Luffy begins his journey to become the Pirate King.",
            "The first core Straw Hat members join the adventure.",
            "The crew defeats Arlong and liberates Nami's village.",
        ],
        "joined": "Zoro, Nami, Usopp, and Sanji",
    },
    "Alabasta": {
        "episode_range": "Episodes 62–130",
        "location": "Arabasta Kingdom",
        "antagonists": "Crocodile and Baroque Works",
        "highlights": [
            "The Straw Hats help Princess Vivi stop a civil war.",
            "Luffy defeats Crocodile.",
            "Chopper joins the Straw Hat Pirates.",
        ],
        "joined": "Tony Tony Chopper",
    },
    "Water 7 / Enies Lobby": {
        "episode_range": "Episodes 229–325",
        "location": "Water 7 and Enies Lobby",
        "antagonists": "Rob Lucci, CP9, and the World Government",
        "highlights": [
            "Robin's tragic past is revealed.",
            "The Straw Hats declare war on the World Government.",
            "The Thousand Sunny becomes the crew's new ship.",
        ],
        "joined": "Franky",
    },
    "Marineford": {
        "episode_range": "Episodes 457–489",
        "location": "Marineford",
        "antagonists": "The Marines and World Government",
        "highlights": [
            "Luffy and allies attempt to rescue Ace.",
            "The Whitebeard Pirates clash with the Marines.",
            "The balance of power in the New World changes.",
        ],
        "joined": "No new permanent Straw Hat member",
    },
    "Dressrosa": {
        "episode_range": "Episodes 629–746",
        "location": "Dressrosa",
        "antagonists": "Donquixote Doflamingo and his crew",
        "highlights": [
            "The Straw Hats challenge Doflamingo's control.",
            "Luffy unveils Gear Fourth.",
            "The Grand Fleet is formed.",
        ],
        "joined": "No new permanent Straw Hat member",
    },
    "Wano Country": {
        "episode_range": "Episodes 890–1085",
        "location": "Wano Country",
        "antagonists": "Kaido, Big Mom, and the Beast Pirates",
        "highlights": [
            "The Alliance rises against Kaido.",
            "Luffy awakens Gear Fifth.",
            "Wano is liberated.",
        ],
        "joined": "No new permanent Straw Hat member",
    },
    "Egghead": {
        "episode_range": "Episodes 1086–present",
        "location": "Egghead Island",
        "antagonists": "The Five Elders, CP0, and the World Government",
        "highlights": [
            "The crew arrives at Vegapunk's futuristic island.",
            "Secrets about the Void Century are revealed.",
            "The Final Saga begins in earnest.",
        ],
        "joined": "No new permanent Straw Hat member",
    },
}

CHARACTERS: dict[str, dict[str, Any]] = {
    "Monkey D. Luffy": {"bounty": 3_000_000_000, "role": "Captain", "color": "#e76f51"},
    "Roronoa Zoro": {"bounty": 1_111_000_000, "role": "Swordsman", "color": "#6a994e"},
    "Nami": {"bounty": 366_000_000, "role": "Navigator", "color": "#f4a261"},
    "Usopp": {"bounty": 500_000_000, "role": "Sniper", "color": "#e9c46a"},
    "Vinsmoke Sanji": {"bounty": 1_032_000_000, "role": "Cook", "color": "#457b9d"},
    "Tony Tony Chopper": {"bounty": 1_000, "role": "Doctor", "color": "#e63946"},
    "Nico Robin": {"bounty": 930_000_000, "role": "Archaeologist", "color": "#8d5a97"},
    "Franky": {"bounty": 394_000_000, "role": "Shipwright", "color": "#277da1"},
    "Brook": {"bounty": 383_000_000, "role": "Musician", "color": "#577590"},
    "Jinbe": {"bounty": 1_100_000_000, "role": "Helmsman", "color": "#264653"},
    "Shanks": {"bounty": 4_048_900_000, "role": "Emperor", "color": "#9b2226"},
    "Kaido": {"bounty": 4_611_100_000, "role": "Emperor", "color": "#6d597a"},
}

DEVIL_FRUITS: list[dict[str, str]] = [
    {
        "name": "Gomu Gomu no Mi",
        "type": "Paramecia",
        "user": "Monkey D. Luffy",
        "ability": "Grants the body rubber-like properties; later revealed to be the Mythical Zoan Hito Hito no Mi, Model: Nika.",
    },
    {
        "name": "Mera Mera no Mi",
        "type": "Logia",
        "user": "Portgas D. Ace / Sabo",
        "ability": "Creates, controls, and transforms the user into fire.",
    },
    {
        "name": "Hito Hito no Mi, Model: Nika",
        "type": "Mythical Zoan",
        "user": "Monkey D. Luffy",
        "ability": "Gives the user extraordinary freedom and rubber-like combat abilities as the Sun God Nika.",
    },
    {
        "name": "Yami Yami no Mi",
        "type": "Logia",
        "user": "Marshall D. Teach",
        "ability": "Creates darkness and can nullify the powers of other Devil Fruits through contact.",
    },
    {
        "name": "Gura Gura no Mi",
        "type": "Paramecia",
        "user": "Edward Newgate / Marshall D. Teach",
        "ability": "Produces powerful vibrations capable of generating earthquakes and tsunamis.",
    },
    {
        "name": "Ope Ope no Mi",
        "type": "Paramecia",
        "user": "Trafalgar D. Water Law",
        "ability": "Creates a ROOM in which the user can manipulate objects, bodies, and spatial positions.",
    },
    {
        "name": "Uo Uo no Mi, Model: Seiryu",
        "type": "Mythical Zoan",
        "user": "Kaido",
        "ability": "Transforms the user into an eastern dragon with weather and flame-based abilities.",
    },
    {
        "name": "Tori Tori no Mi, Model: Phoenix",
        "type": "Mythical Zoan",
        "user": "Marco",
        "ability": "Transforms the user into a phoenix and grants regenerative blue flames.",
    },
    {
        "name": "Suna Suna no Mi",
        "type": "Logia",
        "user": "Crocodile",
        "ability": "Creates, controls, and transforms the user into sand, including the ability to drain moisture.",
    },
    {
        "name": "Nikyu Nikyu no Mi",
        "type": "Paramecia",
        "user": "Bartholomew Kuma",
        "ability": "Repels virtually anything, including physical attacks, air, and even pain.",
    },
    {
        "name": "Bara Bara no Mi",
        "type": "Paramecia",
        "user": "Buggy",
        "ability": "Allows the user to split their body into floating pieces and become immune to cutting attacks.",
    },
    {
        "name": "Neko Neko no Mi, Model: Leopard",
        "type": "Zoan",
        "user": "Rob Lucci",
        "ability": "Transforms the user into a leopard or human-leopard hybrid, greatly increasing physical power.",
    },
]

DEVIL_FRUIT_TYPE_GUIDE: dict[str, str] = {
    "Paramecia": "Grants unusual superhuman abilities that alter the user's body, environment, or physical interaction.",
    "Zoan": "Allows transformation into an animal or animal-human hybrid, usually improving strength, speed, and recovery.",
    "Mythical Zoan": "A rare Zoan class based on legendary creatures and often accompanied by supernatural abilities.",
    "Logia": "Allows the user to create, control, and become a natural element or force of nature.",
}

DEVIL_FRUIT_AWAKENINGS: dict[str, str] = {
    "Gomu Gomu no Mi": "Awakened as the Hito Hito no Mi, Model: Nika; Luffy can affect his surroundings with rubber-like freedom.",
    "Hito Hito no Mi, Model: Nika": "Awakening is represented by Gear Fifth and the user’s transformation into the legendary Sun God Nika.",
    "Ope Ope no Mi": "Awakening enables K-ROOM and R-ROOM, extending spatial manipulation to objects and targets outside the user's body.",
    "Uo Uo no Mi, Model: Seiryu": "No confirmed awakening has been shown; Kaido's advanced dragon abilities remain distinct from a confirmed awakening.",
    "Yami Yami no Mi": "No confirmed awakening has been shown.",
}

DEVIL_FRUIT_DETAILS: dict[str, dict[str, str]] = {
    "Gomu Gomu no Mi": {
        "profile": "Monkey D. Luffy · Captain · 3,000,000,000 Berries",
        "strength": "Extreme",
        "control": "Advanced",
        "danger": "Yonko",
        "weakness": "Standard Devil Fruit water and seastone weaknesses; blunt force is less effective than cutting or piercing attacks.",
    },
    "Mera Mera no Mi": {
        "profile": "Portgas D. Ace / Sabo · Fire Fist users",
        "strength": "Extreme",
        "control": "Advanced",
        "danger": "High",
        "weakness": "Elemental counters and stronger Haki can overcome its Logia intangibility; water suppresses flames.",
    },
    "Hito Hito no Mi, Model: Nika": {
        "profile": "Monkey D. Luffy · Gear Fifth user",
        "strength": "Legendary",
        "control": "Awakened",
        "danger": "Mythic",
        "weakness": "Consumes enormous stamina and still carries standard Devil Fruit and Haki limitations.",
    },
    "Yami Yami no Mi": {
        "profile": "Marshall D. Teach · Blackbeard Pirates",
        "strength": "Extreme",
        "control": "Advanced",
        "danger": "Yonko",
        "weakness": "The user cannot phase through attacks and receives amplified pain; contact is needed to nullify powers.",
    },
    "Gura Gura no Mi": {
        "profile": "Edward Newgate / Marshall D. Teach · Emperors",
        "strength": "Legendary",
        "control": "Advanced",
        "danger": "World-level",
        "weakness": "Collateral damage is difficult to control; normal Devil Fruit and Haki counters still apply.",
    },
    "Ope Ope no Mi": {
        "profile": "Trafalgar D. Water Law · Surgeon of Death",
        "strength": "Extreme",
        "control": "Expert",
        "danger": "Very high",
        "weakness": "Techniques consume stamina and require a ROOM; strong Haki can resist some internal operations.",
    },
    "Uo Uo no Mi, Model: Seiryu": {
        "profile": "Kaido · Former Emperor of the Sea",
        "strength": "Legendary",
        "control": "Awakened-like mastery",
        "danger": "Yonko",
        "weakness": "Large form is easier to target; seastone, Haki, and coordinated attacks remain effective.",
    },
    "Tori Tori no Mi, Model: Phoenix": {
        "profile": "Marco · Former Whitebeard commander",
        "strength": "Extreme",
        "control": "Advanced",
        "danger": "High",
        "weakness": "Regeneration consumes stamina and does not make the user invincible.",
    },
    "Suna Suna no Mi": {
        "profile": "Crocodile · Former Warlord",
        "strength": "High",
        "control": "Advanced",
        "danger": "High",
        "weakness": "Water and liquids can solidify the sand body and reduce Logia evasion.",
    },
}

CREW_MEMBERS: dict[str, str] = {
    "Monkey D. Luffy": "Captain",
    "Roronoa Zoro": "Swordsman",
    "Nami": "Navigator",
    "Usopp": "Sniper",
    "Vinsmoke Sanji": "Cook",
    "Tony Tony Chopper": "Doctor",
    "Nico Robin": "Archaeologist",
    "Franky": "Shipwright",
    "Brook": "Musician",
    "Jinbe": "Helmsman",
}

QUIZ_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": 1,
        "question": "Who is known as the Straw Hat captain?",
        "options": ["Roronoa Zoro", "Monkey D. Luffy", "Trafalgar Law", "Usopp"],
        "answer": "Monkey D. Luffy",
    },
    {
        "id": 2,
        "question": "Which Devil Fruit is associated with fire?",
        "options": ["Mera Mera no Mi", "Suna Suna no Mi", "Gura Gura no Mi", "Ope Ope no Mi"],
        "answer": "Mera Mera no Mi",
    },
    {
        "id": 3,
        "question": "Who ruled Wano as one of its major antagonists?",
        "options": ["Crocodile", "Doflamingo", "Kaido", "Arlong"],
        "answer": "Kaido",
    },
    {
        "id": 4,
        "question": "What is the name of the Straw Hats' ship after the Going Merry?",
        "options": ["Red Force", "Thousand Sunny", "Oro Jackson", "Moby Dick"],
        "answer": "Thousand Sunny",
    },
    {
        "id": 5,
        "question": "Which character is famous for using three-sword style?",
        "options": ["Sanji", "Franky", "Brook", "Roronoa Zoro"],
        "answer": "Roronoa Zoro",
    },
    {
        "id": 6,
        "question": "Who is the Straw Hat crew's navigator?",
        "options": ["Nami", "Robin", "Vivi", "Perona"],
        "answer": "Nami",
    },
    {
        "id": 7,
        "question": "What is the name of Luffy's signature technique category?",
        "options": ["Gomu Gomu", "Diable Jambe", "Asura", "Room"],
        "answer": "Gomu Gomu",
    },
    {
        "id": 8,
        "question": "Which arc features the rescue of Nico Robin at Enies Lobby?",
        "options": ["Dressrosa", "Water 7 / Enies Lobby", "Egghead", "Alabasta"],
        "answer": "Water 7 / Enies Lobby",
    },
    {
        "id": 9,
        "question": "Who is the Straw Hat crew's doctor?",
        "options": ["Brook", "Franky", "Tony Tony Chopper", "Jinbe"],
        "answer": "Tony Tony Chopper",
    },
    {
        "id": 10,
        "question": "Which class can transform the user into a natural element?",
        "options": ["Paramecia", "Zoan", "Logia", "Mythical Zoan"],
        "answer": "Logia",
    },
]

BOUNTY_REWARDS: list[dict[str, Any]] = [
    {"achievement": "Complete an East Blue arc", "reward": 30_000_000},
    {"achievement": "Defeat a Warlord-level opponent", "reward": 150_000_000},
    {"achievement": "Survive a Marineford-scale war", "reward": 300_000_000},
    {"achievement": "Defeat a Yonko commander", "reward": 500_000_000},
    {"achievement": "Liberate a country from a Yonko", "reward": 1_000_000_000},
]

FACTION_UNITS: dict[str, list[dict[str, Any]]] = {
    "Pirates": [
        {"name": "Straw Hat Captain", "power": 96, "defense": 82, "speed": 94, "special": "Gear Fifth"},
        {"name": "Three-Sword Swordsman", "power": 91, "defense": 88, "speed": 83, "special": "King of Hell"},
        {"name": "Soul King Musician", "power": 76, "defense": 69, "speed": 86, "special": "Soul Solid"},
        {"name": "Helmsman of the Sea", "power": 87, "defense": 93, "speed": 72, "special": "Fish-Man Karate"},
    ],
    "Marines": [
        {"name": "Fleet Admiral", "power": 95, "defense": 91, "speed": 76, "special": "Magma Fist"},
        {"name": "Admiral of Light", "power": 92, "defense": 79, "speed": 99, "special": "Light-Speed Kick"},
        {"name": "Vice Admiral", "power": 80, "defense": 84, "speed": 75, "special": "Haki Barrage"},
        {"name": "Marine Strategist", "power": 73, "defense": 78, "speed": 82, "special": "Tactical Net"},
    ],
}
