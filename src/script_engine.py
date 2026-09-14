import random
import json
import requests
from src.config import GEMINI_API_KEY

# Curated High-Engagement AI, Future Tech & Mystery Database
CURATED_AI_REELS = [
    {
        "title": "এআই কি সত্যিই মানুষের চাকরি কেড়ে নেবে?",
        "scenes": [
            {
                "text": "আগামী ৫ বছরে কোন কোন পেশা পুরোপুরি বদলে দেবে কৃত্রিম বুদ্ধিমত্তা? এই তথ্যটি প্রত্যেকের জানা জরুরি।",
                "query": "artificial intelligence robot future technology"
            },
            {
                "text": "গোল্ডম্যান স্যাকসের রিপোর্ট অনুযায়ী, বিশ্বজুড়ে প্রায় ৩০ কোটি চাকরি এআই এবং অটোমেশনের প্রভাবে ঝুঁকিতে পড়তে যাচ্ছে।",
                "query": "ai office worker computer technology"
            },
            {
                "text": "বিশেষ করে ডাটা এন্ট্রি, সাধারণ কাস্টমার সার্ভিস, বেসিক কোডিং এবং কনটেন্ট রাইটিংয়ের মতো কাজগুলো এখন মুহূর্তের মধ্যেই করে দিচ্ছে এআই।",
                "query": "robot typing computer future tech"
            },
            {
                "text": "তবে বিশেষজ্ঞরা বলছেন, এআই মানুষের জায়গা নেবে না, বরং যে ব্যক্তি এআই ব্যবহার করতে জানে, সে বাকিদের চেয়ে এগিয়ে থাকবে।",
                "query": "cyborg human brain technology connection"
            },
            {
                "text": "আপনার পেশা কি এআইয়ের কারণে নিরাপদ? কমেন্টে আপনার পেশার নাম লিখুন এবং প্রযুক্তির আপডেট পেতে পেজটি ফলো করুন।",
                "query": "future city skyline flying cars"
            }
        ],
        "caption": "🤖 এআই কি সত্যিই মানুষের চাকরি কেড়ে নেবে? কোন পেশাগুলো সবচেয়ে বেশি ঝুঁকিতে? পুরো ভিডিওটি দেখে জেনে নিন।",
        "hashtags": ["#কৃত্রিমবুদ্ধিমত্তা", "#ArtificialIntelligence", "#AIJobs", "#FutureTech", "#BanglaTech", "#ReelsViral", "#TechFacts"]
    },
    {
        "title": "হিউম্যানয়েড রোবট ও ভবিষ্যতের মানবজাতি",
        "scenes": [
            {
                "text": "মানুষের মতো দেখতে, কথা বলতে এবং কাজ করতে পারা হিউম্যানয়েড রোবট এখন আর সায়েন্স ফিকশন নয়।",
                "query": "humanoid robot walking technology laboratory"
            },
            {
                "text": "টেসলার অপটিমাস এবং বোস্টন ডায়নামিক্সের রোবটগুলো এখন মানুষের মতোই জটিল সব শারীরিক কাজ নিখুঁতভাবে করতে পারছে।",
                "query": "robot doing backflip futuristic machine"
            },
            {
                "text": "এমনকি এসব রোবটের ভেতরে এমন শক্তিশালী এআই ব্রেন দেওয়া হয়েছে, যা পরিবেশ দেখে নিজে নিজেই সিদ্ধান্ত নিতে পারে।",
                "query": "robot face glowing blue eyes artificial brain"
            },
            {
                "text": "বিজ্ঞানীদের ধারণা, ২০৩৫ সালের মধ্যে প্রতিটি ধনী পরিবারে এবং কারখানায় গৃহকর্মী হিসেবে এসব রোবট দেখা যাবে।",
                "query": "futuristic smart home robot assisting"
            },
            {
                "text": "আপনি কি নিজের বাসায় এমন একটি রোবট রাখতে চাইবেন? কমেন্টে জানান এবং প্রযুক্তির রোমাঞ্চকর সব খবর পেতে পেজটি ফলো করুন।",
                "query": "human shaking hand with robot hand"
            }
        ],
        "caption": "🦾 মানুষের মতো চিন্তা করতে পারা রোবট কি খুব শীঘ্রই আমাদের ঘরে আসছে? দেখুন প্রযুক্তির অবিশ্বাস্য অগ্রগতি!",
        "hashtags": ["#রোবট", "#হিউম্যানয়েডরোবট", "#Robotics", "#OptimusRobot", "#Futuristic", "#BanglaTech", "#FBReels"]
    },
    {
        "title": "নিউরালিংক: মানুষের মাথায় কম্পিউটারের চিপ",
        "scenes": [
            {
                "text": "শুধু চিন্তা করেই কম্পিউটার বা মোবাইল নিয়ন্ত্রণ করা— ইলন মাস্কের নিউরালিংক কি অসম্ভবকে সম্ভব করেছে?",
                "query": "cyberpunk brain chip technology neuroscience"
            },
            {
                "text": "মানুষের মস্তিষ্কে একটি কয়েন আকৃতির মাইক্রোচিপ বসিয়ে প্যারালাইজড রোগীদের কেবল মনের ইচ্ছায় মাউস বা গেম খেলতে সাহায্য করা হচ্ছে।",
                "query": "futuristic medical technology brain scan"
            },
            {
                "text": "ভবিষ্যতে এই প্রযুক্তির মাধ্যমে মানুষ হয়তো মনের কথা সরাসরি অন্য কারো মাথায় পাঠাতে পারবে, এমনকি অন্ধ মানুষের দৃষ্টি ফিরিয়ে আনাও সম্ভব হবে।",
                "query": "hologram brain neural network glowing"
            },
            {
                "text": "তবে চিকিৎসকদের অনেকে আশঙ্কা করছেন, মানুষের মস্তিষ্কে যদি হ্যাকাররা ভাইরাস বা ম্যালওয়্যার ঢুকিয়ে দেয়, তবে কী পরিণতি হবে?",
                "query": "hacker typing code red screen binary"
            },
            {
                "text": "আপনি কি নিজের মাথায় এমন চিপ লাগাতে রাজি হবেন? কমেন্টে আপনার মতামত জানান এবং পেজটি ফলো করতে ভুলবেন না।",
                "query": "futuristic technology cyber interface"
            }
        ],
        "caption": "🧠 মানুষের মাথায় কম্পিউটারের চিপ! মনের ইচ্ছায় চলবে কম্পিউটার। নিউরালিংকের রোমাঞ্চকর তথ্য জানুন।",
        "hashtags": ["#নিউরালিংক", "#ইলনমাস্ক", "#Neuralink", "#BrainChip", "#FutureScience", "#BanglaScience", "#Reels"]
    },
    {
        "title": "এআই ভয়েস ও ফেস ক্লোনিংয়ের ভয়ংকর বাস্তবতা",
        "scenes": [
            {
                "text": "যেকোনো মানুষের মাত্র ৩ সেকেন্ডের ভয়েস রেকর্ড দিয়ে এখন হুবহু তাঁর মতো কথা বলিয়ে নেওয়া সম্ভব।",
                "query": "voice waveform audio frequency visual"
            },
            {
                "text": "কৃত্রিম বুদ্ধিমত্তার ডিপফেক এবং ভয়েস ক্লোনিং প্রযুক্তি এতই বাস্তবসম্মত হয়েছে যে সাধারণ চোখে আসল আর নকলের পার্থক্য করা অসম্ভব।",
                "query": "digital human face glitch cyberspace"
            },
            {
                "text": "বিশ্বজুড়ে প্রতারকরা এখন পরিবারের সদস্যদের পরিচিত কণ্ঠ নকল করে ফোন দিয়ে লাখ লাখ টাকা হাতিয়ে নিচ্ছে।",
                "query": "scam call smartphone dark room mystery"
            },
            {
                "text": "বিশেষজ্ঞদের পরামর্শ হলো, পরিবারের সাথে একটি সিক্রেট কোড বা পাসওয়ার্ড ঠিক করে রাখুন যাতে কেউ ফেক কল দিলে ধরা পড়ে।",
                "query": "cyber security shield lock glowing"
            },
            {
                "text": "আপনি কি কখনো কোনো এআই ডিপফেক বা ফেক ভয়েসের মুখোমুখি হয়েছেন? সবাইকে সতর্ক করতে ভিডিওটি শেয়ার করুন এবং পেজটি ফলো করুন।",
                "query": "smartphone screen security technology"
            }
        ],
        "caption": "⚠️ আপনার কণ্ঠ ও চেহারা মাত্র ৩ সেকেন্ডেই চুরি হতে পারে! ডিপফেক ও এআই স্ক্যাম থেকে বাঁচার উপায় জানুন।",
        "hashtags": ["#ডিপফেক", "#ভয়েসক্লোনিং", "#DeepfakeAI", "#CyberSecurity", "#AiScamAlert", "#TechSafety", "#ViralReels"]
    }
]

# Curated High-Engagement Daily Discussion Posts (টেক্সট পোস্ট যা কমেন্ট বাড়ায়)
DAILY_DISCUSSION_POSTS = [
    {
        "text": (
            "🔥 একটি গুরুত্বপূর্ণ প্রশ্ন:\n\n"
            "ধরুন, এমন একটি এআই রোবট বাজারে এলো যা মানুষের চেয়ে দ্বিগুণ গতিতে ও নিখুঁতভাবে আপনার পেশার সমস্ত কাজ করে দিতে পারে।\n\n"
            "কোম্পানিগুলো কি কম খরচে রোবট নেবে, নাকি মানুষকে চাকরি দেবে?\n"
            "👉 কমেন্টে আপনার মতামত দিন: মানুষ নাকি এআই?"
        ),
        "category": "মতামত ও বিতর্ক"
    },
    {
        "text": (
            "🧠 ইলন মাস্কের দাবি, আগামী ৫ থেকে ৭ বছরের মধ্যে এআই যেকোনো সাধারণ মানুষের চেয়ে বেশি বুদ্ধিমান (AGI) হয়ে যাবে।\n\n"
            "আপনার কী মনে হয়? রোবট বা এআই কি কখনো মানুষের অনুভূতি ও ভালোবাসার জায়গা নিতে পারবে?\n"
            "১. হ্যাঁ, সম্ভব\n"
            "২. অসম্ভব, মানুষ মানুষের মতোই থাকবে\n\n"
            "👇 আপনার ভোট কমেন্টে জানান।"
        ),
        "category": "বিজ্ঞান ও দর্শন"
    },
    {
        "text": (
            "💡 বর্তমানে ফ্রি-তে কাজ করার জন্য সেরা ৫টি এআই টুল:\n\n"
            "১. ChatGPT / Claude — কনটেন্ট ও লেখার সেরা সহকারী\n"
            "২. Midjourney / Leonardo — এক ক্লিকে অসাধারণ ছবি তৈরির জন্য\n"
            "৩. Canva Magic Studio — ডিজাইন ও সোশ্যাল মিডিয়া পোস্ট\n"
            "৪. ElevenLabs / Edge-TTS — বাস্তবসম্মত ভয়েসওভার তৈরির জন্য\n"
            "৫. Perplexity AI — গুগলের চেয়ে ১০ গুণ দ্রুত সঠিক তথ্য খোঁজার জন্য\n\n"
            "📌 আপনি এদের মধ্যে কোনটি সবচেয়ে বেশি ব্যবহার করেন? কমেন্টে লিখুন।"
        ),
        "category": "প্রয়োজনীয় টুলস"
    }
]

# Daily Story / Poll Ideas
DAILY_STORY_POLLS = [
    "📊 আজকের স্টোরি পোল:\n'আপনি কি নিজের ক্যারিয়ারে প্রতিদিন কোনো না কোনো এআই টুল ব্যবহার করছেন?'\n🔘 হ্যাঁ, নিয়মিত\n🔘 না, এখনও শুরু করিনি",
    "📊 আজকের স্টোরি পোল:\n'কৃত্রিম বুদ্ধিমত্তা মানুষের জন্য কি আশীর্বাদ নাকি অভিশাপ?'\n🔘 আশীর্বাদ\n🔘 অভিশাপ",
    "📊 আজকের স্টোরি পোল:\n'আপনার মোবাইলে ChatGPT বা কোনো এআই অ্যাপ ইনস্টল করা আছে কি?'\n🔘 হ্যাঁ আছে\n🔘 না নেই"
]

# Daily Infographic Photo Card Data
DAILY_PHOTOCARDS = [
    {
        "title": "২০৩০ সালে যে ৪টি চাকরি এআই বদলে দেবে",
        "points": [
            "১. ডাটা এন্ট্রি ও বেসিক কাস্টমার সাপোর্ট অপারেটর",
            "২. সাধারণ ট্রান্সলেশন ও বেসিক প্রুফরিডিং",
            "৩. প্রাথমিক কোডিং ও সহজ ওয়েবসাইট বাগ ফিক্সিং",
            "৪. সাধারণ গ্রাফিক্স ডিজাইন ও সোশ্যাল মিডিয়া পোস্ট মেকিং"
        ],
        "category": "কৃত্রিম বুদ্ধিমত্তা ও ক্যারিয়ার"
    },
    {
        "title": "দৈনন্দিন কাজে সেরা ৪টি ফ্রি এআই টুল",
        "points": [
            "১. ChatGPT — যেকোনো তথ্য, আইডিয়া ও লেখার জন্য",
            "২. Leonardo AI — টেক্সট লিখে হাই-কোয়ালিটি ছবি তৈরির জন্য",
            "৩. Perplexity — রেফারেন্স সহ সরাসরি প্রশ্নের উত্তর খোঁজার জন্য",
            "৪. ElevenLabs — ভয়েস ডাবিং ও সাউন্ড ইফেক্টের জন্য"
        ],
        "category": "প্রয়োজনীয় প্রযুক্তি গাইড"
    }
]

def get_reel_content():
    """Returns an AI-focused or high-retention mystery fact reel script."""
    # Always prioritize cutting-edge AI & Tech reels
    return random.choice(CURATED_AI_REELS)

def get_daily_extras():
    """Returns complementary creator kit items: text post, story poll, and photo-card info."""
    discussion = random.choice(DAILY_DISCUSSION_POSTS)
    story_poll = random.choice(DAILY_STORY_POLLS)
    card_data = random.choice(DAILY_PHOTOCARDS)
    return {
        "discussion_post": discussion,
        "story_poll": story_poll,
        "photo_card": card_data
    }
