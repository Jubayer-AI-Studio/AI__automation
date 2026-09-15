# -*- coding: utf-8 -*-
"""
=============================================================================
✍️ 1. CONTENT WRITING & SCRIPT ENGINE (লেখালেখি ও স্ক্রিপ্ট)
=============================================================================
এই ফাইলে ফেসবুক রিলসের সমস্ত এআই ও প্রযুক্তি সম্পর্কিত স্ক্রিপ্ট, ভাইরাল হুক,
ফেসবুক পোস্ট ক্যাপশন, হ্যাশট্যাগ, ফিড ডিসকাশন পোস্ট এবং স্টোরি পোল সংরক্ষিত থাকে।

কোনো স্ক্রিপ্ট বা ক্যাপশন পরিবর্তন করতে চাইলে আপনি সরাসরি এই ফাইলে পরিবর্তন করবেন।
টেস্ট করার জন্য টার্মিনালে চালান:
    python content_writing/script_writer.py
=============================================================================
"""

import random
import json
from pathlib import Path


# Curated High-Engagement AI, Future Tech & Mystery Database (Natural Spoken Bangla)
CURATED_AI_REELS = [
    {
        "title": "এআই কি সত্যিই মানুষের চাকরি কেড়ে নেবে?",
        "scenes": [
            {
                "text": "ভাই, একটু ভেবে দেখেছেন? মাত্র কয়েকটা মাসের মধ্যে এআই কোন কোন পেশা পুরোপুরি শেষ করে দিতে পারে! আসল সত্যিটা শুনুন।",
                "query": "artificial intelligence robot future technology"
            },
            {
                "text": "রিপোর্ট বলছে, বিশ্বজুড়ে প্রায় ৩০ কোটি চাকরি খুব দ্রুত এআই ও অটোমেশনের কবলে পড়তে যাচ্ছে।",
                "query": "ai office worker computer technology"
            },
            {
                "text": "ডাটা এন্ট্রি, কাস্টমার সার্ভিস, কনটেন্ট রাইটিং আর বেসিক কোডিং— এই কাজগুলো মানুষ ছাড়া এখন এক ক্লিকেই হচ্ছে।",
                "query": "robot typing computer future tech"
            },
            {
                "text": "তবে আসল খেলাটা কী জানেন? এআই আপনার চাকরি নেবে না, যে ব্যক্তি এআই চালানো শিখে গেছে, সে-ই আপনার জায়গাটা নিয়ে নেবে!",
                "query": "cyborg human brain technology connection"
            },
            {
                "text": "আপনার পেশা কি এআইয়ের হাত থেকে নিরাপদ? কমেন্টে আপনার কাজের নাম লিখে যান, আর টেক তথ্যের জন্য পেজটি ফলো করুন।",
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
                "text": "মানুষের মতো হাঁটবে, কথা বলবে, এমনকি ঘরের কাজও করে দেবে— হিউম্যানয়েড রোবট কিন্তু আর সিনেমার গল্প নয়, বাস্তবে চলে এসেছে!",
                "query": "humanoid robot walking technology laboratory"
            },
            {
                "text": "টেসলার অপটিমাস আর বোস্টন ডায়নামিক্সের রোবটগুলো এখন মানুষের চেয়েও নিখুঁতভাবে কঠিন সব শারীরিক কাজ করে দেখাচ্ছে।",
                "query": "robot doing backflip futuristic machine"
            },
            {
                "text": "সবচেয়ে তাজ্জব ব্যাপার হলো, এদের ভেতরে বসানো হয়েছে এমন এআই ব্রেন, যা পরিবেশ বুঝে নিজে থেকেই যেকোনো সিদ্ধান্ত নিতে পারে।",
                "query": "robot face glowing blue eyes artificial brain"
            },
            {
                "text": "বিজ্ঞানীরা বলছেন, আগামী কয়েক বছরের ভেতরেই মধ্যবিত্ত পরিবারগুলোতেও মানুষের বদলে এমন রোবট দেখা যাবে!",
                "query": "futuristic smart home robot assisting"
            },
            {
                "text": "আপনি কি নিজের বাসায় এমন একটি রোবট রাখতে চাইবেন? কমেন্টে জানান, আর প্রযুক্তির রোমাঞ্চকর খবরের জন্য পেজটি ফলো রাখুন।",
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
                "text": "হাত দিয়ে ছোঁয়া লাগবে না, শুধু মনে মনে চিন্তা করলেই কম্পিউটার আর মোবাইল চলবে! শুনে অবিশ্বাস্য লাগছে, তাই না?",
                "query": "cyberpunk brain chip technology neuroscience"
            },
            {
                "text": "ইলন মাস্কের নিউরালিংক মানুষের মাথায় কয়েন সাইজের একটা মাইক্রোচিপ বসিয়ে এই অসম্ভবকে সত্যি করে দেখিয়েছে।",
                "query": "futuristic medical technology brain scan"
            },
            {
                "text": "শুধু তা-ই নয়, ভবিষ্যতে হয়তো মুখ দিয়ে কথা না বলেও সরাসরি মনের ভাব অন্যের মাথায় ওয়্যারলেসভাবে পাঠিয়ে দেওয়া যাবে!",
                "query": "hologram brain neural network glowing"
            },
            {
                "text": "কিন্তু বিজ্ঞানীদের একটা বড় ভয় আছে— কোনো হ্যাকার যদি মাথায় ম্যালওয়্যার বা ভাইরাস ঢুকিয়ে দেয়, তবে পরিণতি কী হবে?",
                "query": "hacker typing code red screen binary"
            },
            {
                "text": "আপনি কি নিজের মাথায় এমন চিপ বসাতে রাজি হবেন? কমেন্টে জানান, আর নিত্যনতুন টেক আপডেটের জন্য পেজটি ফলো করুন।",
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
                "text": "আপনার মাত্র ৩ সেকেন্ডের একটি ভয়েস রেকর্ড পেলেই হুবহু আপনার মতো কথা বলিয়ে নেওয়া সম্ভব! শুনলে গায়ে কাঁটা দিয়ে ওঠে।",
                "query": "voice waveform audio frequency visual"
            },
            {
                "text": "এআই ডিপফেক প্রযুক্তি এখন এতটাই নিখুঁত হয়েছে যে, সাধারণ চোখে আসল আর নকলের কোনো তফাতই ধরা যায় না।",
                "query": "digital human face glitch cyberspace"
            },
            {
                "text": "বিশ্বজুড়ে প্রতারকরা এখন পরিচিত মানুষের কণ্ঠ নকল করে কল দিয়ে নিমেষেই লাখ লাখ টাকা হাতিয়ে নিচ্ছে।",
                "query": "scam call smartphone dark room mystery"
            },
            {
                "text": "বাঁচার সবচেয়ে সহজ উপায় হলো, পরিবারের সাথে একটি গোপন পাসওয়ার্ড ঠিক করে রাখুন, যাতে ফেক কল আসলেই ধরে ফেলা যায়।",
                "query": "cyber security shield lock glowing"
            },
            {
                "text": "আপনার কাছে কি কখনো কোনো সন্দেহজনক ফেক কল এসেছে? সবাইকে সতর্ক করতে ভিডিওটি শেয়ার করুন আর পেজটি ফলো রাখুন।",
                "query": "smartphone screen security technology"
            }
        ],
        "caption": "⚠️ আপনার কণ্ঠ ও চেহারা মাত্র ৩ সেকেন্ডেই চুরি হতে পারে! ডিপফেক ও এআই স্ক্যাম থেকে বাঁচার উপায় জানুন।",
        "hashtags": ["#ডিপফেক", "#ভয়েসক্লোনিং", "#DeepfakeAI", "#CyberSecurity", "#AiScamAlert", "#TechSafety", "#ViralReels"]
    },
    {
        "title": "কোয়ান্টাম কম্পিউটার: সুপারকম্পিউটারের চেয়ে কোটি গুণ দ্রুত",
        "scenes": [
            {
                "text": "সাধারণ সুপারকম্পিউটারের যে জটিল হিসাব মেলাতে ১০ হাজার বছর লেগে যেত, কোয়ান্টাম কম্পিউটার তা করে ফেলে মাত্র কয়েক মিনিটে!",
                "query": "quantum computer gold chandelier technology"
            },
            {
                "text": "কোয়ান্টাম ফিজিক্সের নীতিতে চলা এই অতিমানবীয় কম্পিউটার তথ্য প্রক্রিয়াকরণে তৈরি করেছে এক অভাবনীয় গতি।",
                "query": "particle physics quantum mechanics visualization"
            },
            {
                "text": "এর ফলে দুরারোগ্য রোগের ওষুধ আবিষ্কার থেকে শুরু করে মহাবিশ্বের রহস্যভেদ— সবকিছু চোখের পলকে করা সম্ভব হবে।",
                "query": "dna sequencing laboratory molecular research"
            },
            {
                "text": "তবে মারাত্মক বিপদের কথা হলো, কোয়ান্টাম কম্পিউটারের মাধ্যমে বিশ্বের সব ব্যাংকের পাসওয়ার্ড ও নিরাপত্তা মুহূর্তেই হ্যাক করা সম্ভব হতে পারে।",
                "query": "bank digital vault cyber attack security"
            },
            {
                "text": "প্রযুক্তির এই শক্তি মানবজাতির জন্য আশীর্বাদ নাকি ভয়ংকর হুমকি? কমেন্টে আপনার মতামত জানান আর পেজটি ফলো করুন।",
                "query": "future world holographic technology glowing"
            }
        ],
        "caption": "⚡ সুপারকম্পিউটারের চেয়েও কোটি গুণ দ্রুত গতিসম্পন্ন কোয়ান্টাম কম্পিউটার! এই অতিমানবীয় প্রযুক্তি কি মানবজাতির জন্য আশীর্বাদ নাকি হুমকি? বিস্তারিত জেনে নিন।",
        "hashtags": ["#কোয়ান্টামকম্পিউটার", "#QuantumComputing", "#Supercomputer", "#FutureTech", "#BanglaTech", "#CyberTech", "#Reels"]
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

# =============================================================================
# স্বতন্ত্র টেস্ট কোড (টার্মিনালে সরাসরি চালিয়ে চেক করার জন্য)
# =============================================================================
if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 60)
    print("✍️ [CONTENT WRITER TEST] স্ক্রিপ্ট ও লেখালেখি জেনারেটর টেস্ট")
    print("=" * 60)

    reel = get_reel_content()
    print(f"\n📌 ভিডিও শিরোনাম: {reel['title']}")
    print(f"🎬 সিন সংখ্যা: {len(reel['scenes'])}")
    for i, s in enumerate(reel['scenes'], 1):
        print(f"   সিন {i}: {s['text']}")

    print(f"\n📝 ফেসবুক ক্যাপশন:\n{reel['caption']}")
    print(f"\n🏷️ হ্যাশট্যাগ: {' '.join(reel['hashtags'])}")

    extras = get_daily_extras()
    print("\n" + "-" * 60)
    print(f"💬 দৈনিক ফিড ডিসকাশন পোস্ট ({extras['discussion_post']['category']}):")
    print(extras['discussion_post']['text'])
    print("\n" + "-" * 60)
    print(f"📊 স্টোরি পোল:\n{extras['story_poll']}")
    print("=" * 60)
    print("✅ লেখালেখি মডিউল সম্পূর্ণ সুস্থ ও কার্যকর আছে!")

