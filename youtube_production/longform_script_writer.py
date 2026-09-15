# -*- coding: utf-8 -*-
"""
=============================================================================
📜 YOUTUBE LONG-FORM SCRIPT & SEO ENGINE (5-7 MINUTES MASTER EDITION)
=============================================================================
এই ইঞ্জিনে ইউটিউবের জন্য উচ্চ-রিটেনশন যুক্ত ৫ থেকে ৭ মিনিটের পূর্ণাঙ্গ টেক
ডকুমেন্টারি স্ক্রিপ্ট, চ্যাপ্টার লোয়ার-থার্ড মার্কার, ক্লিকযোগ্য টাইমস্ট্যাম্প সহ
এসইও ডেসক্রিপশন এবং ৩টি স্বয়ংক্রিয় ভাইরাল শর্টস মার্কার তৈরি হয়।
=============================================================================
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import random
from pathlib import Path

CURATED_LONGFORM_DOCUMENTARIES = [
    {
        "title": "কোয়ান্টাম কম্পিউটার: সুপারকম্পিউটারের চেয়ে কোটি গুণ দ্রুত গতির মহাবিপ্লব",
        "short_title": "কোয়ান্টাম কম্পিউটার বিপ্লব",
        "theme": "quantum",
        "chapters": [
            {
                "chapter_id": 0,
                "title": "ভূমিকা: বিজ্ঞানের চরম বিস্ময়",
                "scenes": [
                    {"text": "দর্শক, মানব ইতিহাসের সবচেয়ে পরাক্রমশালী ও অবিশ্বাস্য গণনা প্রযুক্তির মুখোমুখি আজ আমরা। যে জটিল গাণিতিক হিসাব মেলাতে বিশ্বের সবচেয়ে শক্তিশালী সুপারকম্পিউটারেরও দশ হাজার বছর সময় লাগত, আধুনিক কোয়ান্টাম কম্পিউটার তা সম্পন্ন করছে মাত্র কয়েক মিনিটে।", "clip": "quantum_server_room.mp4"},
                    {"text": "সায়েন্স ফিকশন সিনেমার জটিল থিয়োরি এবার সত্যি সত্যি গবেষণাগারের বাস্তবতায় রূপ নিয়েছে। গুগল, আইবিএম ও বিশ্বের পরাশক্তিগুলো কোটি কোটি ডলার বিনিয়োগ করে নেমেছে এই কোয়ান্টাম আধিপত্য বিস্তারের ঐতিহাসিক যুদ্ধে।", "clip": "microchip_processor.mp4"},
                    {"text": "কিন্তু সাধারণ কম্পিউটারের সাথে এই দানবীয় কোয়ান্টাম কম্পিউটারের আসল পার্থক্যটা কোথায়? কেন এটি মানব সভ্যতার গতিপথ চিরতরে বদলে দিতে চলেছে? আজকের এই বিশেষ প্রতিবেদনে আমরা উন্মোচন করবো কোয়ান্টাম কম্পিউটিংয়ের আদ্যোপান্ত।", "clip": "cyber_code_matrix.mp4"}
                ],
                "is_viral_short": True,
                "short_label": "short_1_hook"
            },
            {
                "chapter_id": 1,
                "title": "অধ্যায় ১: কিউবিট ও কোয়ান্টাম মেকানিক্সের রহস্য",
                "scenes": [
                    {"text": "সাধারণ কম্পিউটার কাজ করে বাইনারি পদ্ধতিতে। অর্থাৎ তথ্যের প্রতিটি অংশ হয় শূন্য অথবা এক হিসেবে জমা থাকে। যাকে আমরা বলি বিট।", "clip": "cyber_code_matrix.mp4"},
                    {"text": "কিন্তু কোয়ান্টাম কম্পিউটারে ব্যবহার করা হয় কিউবিট বা কোয়ান্টাম বিট। কোয়ান্টাম ফিজিক্সের সুপারপজিশন নিয়মের কারণে একটি কিউবিট একই সাথে শূন্য এবং এক— উভয় অবস্থাতেই বিরাজ করতে পারে।", "clip": "red_mesh_3d.mp4"},
                    {"text": "এর ফলে সাধারণ কম্পিউটার যেখানে একটির পর একটি হিসাব ধারাবাহিকভাবে সমাধান করে, সেখানে কোয়ান্টাম কম্পিউটার একসাথে কোটি কোটি সম্ভাবনার ওপর একযোগে কাজ করতে সক্ষম হয়।", "clip": "quantum_server_room.mp4"},
                    {"text": "এই অকল্পনীয় প্রক্রিয়া চালু রাখতে প্রসেসরকে রাখা হয় মহাবিশ্বের সবচেয়ে শীতল তাপমাত্রায়— প্রায় মাইনাস ২৭৩ ডিগ্রি সেলসিয়াসে, যা গভীর মহাশূন্যের চেয়েও অনেক বেশি ঠান্ডা।", "clip": "microchip_processor.mp4"}
                ],
                "is_viral_short": False
            },
            {
                "chapter_id": 2,
                "title": "অধ্যায় ২: সিস্টেম আর্কিটেকচার ও জুবায়েরের কোড ডেমো",
                "scenes": [
                    {"text": "কোয়ান্টাম অ্যালগরিদম ডিজাইন সাধারণ প্রোগ্রামিংয়ের মতো নয়। এখানে জটিল ম্যাথমেটিক্যাল লজিক ও প্রবাবিলিটি গেট ব্যবহার করে অ্যালগরিদম তৈরি করতে হয়।", "clip": "cyber_laser_glasses.mp4"},
                    {"text": "স্ক্রিনে আপনারা দেখতে পাচ্ছেন কোয়ান্টাম স্টেট ট্র্যাকিং ও জটিল অপটিমাইজেশনের জন্য তৈরি একটি বিশেষ পাইথন অটোমেশন ফ্রেমওয়ার্ক, যা সেকেন্ডে হাজার হাজার ভেক্টর ক্যালকুলেশন সম্পন্ন করছে।", "clip": "code_walkthrough"},
                    {"text": "এই ধরনের শক্তিশালী অ্যালগরিদমিক সক্ষমতার কারণে ওষুধ আবিষ্কারের ক্ষেত্রে মলিকিউলার সিমুলেশন তৈরি করা সম্ভব হচ্ছে কয়েক ঘণ্টার ব্যবধানে, যা প্রচলিত ল্যাবরেটরিতে বছরের পর বছর সময় নিত।", "clip": "brain_3d_screen.mp4"},
                    {"text": "জেনেটিক রিসার্চ, ক্যান্সার চিকিৎসার আধুনিক মলিকিউল ডিজাইন এবং পরিবেশের কার্বন শোষণের জন্য নতুন উপাদান তৈরিতে কোয়ান্টাম ইঞ্জিনিয়ারিং সৃষ্টি করেছে আশার নতুন দিগন্ত।", "clip": "hands_digital_realm.mp4"}
                ],
                "is_viral_short": True,
                "short_label": "short_2_deep_tech"
            },
            {
                "chapter_id": 3,
                "title": "অধ্যায় ৩: চরম ঝুঁকি ও বৈশ্বিক সাইবার নিরাপত্তা সংকট",
                "scenes": [
                    {"text": "তবে মুদ্রার অপর পিঠে রয়েছে চরম এক অশনি সংকেত। বিশ্বের সমস্ত ব্যাংকিং ব্যবস্থা, সামরিক যোগাযোগ ও ইন্টারনেট নিরাপত্তা দাঁড়িয়ে আছে আরএসএ এবং আধুনিক এনক্রিপশনের শক্ত ভিত্তির ওপর।", "clip": "red_laser_tunnel.mp4"},
                    {"text": "একটি পূর্ণাঙ্গ শক্তিশালী কোয়ান্টাম কম্পিউটার প্রচলিত এই কঠিন এনক্রিপশন কোডগুলো ভেঙে ফেলতে পারে মাত্র কয়েক মিনিটের ব্যবধানে।", "clip": "cyber_code_matrix.mp4"},
                    {"text": "যদি এই অপরিসীম শক্তি কোনো ভুল হাতে কিংবা সাইবার অপরাধীদের কবলে চলে যায়, তবে বিশ্বের অর্থনৈতিক ও সরকারি গোপনীয়তা সম্পূর্ণ ধসে পড়ার মারাত্মক ঝুঁকি তৈরি হবে।", "clip": "red_circuit_board.mp4"},
                    {"text": "এই সংকট মোকাবেলায় বিজ্ঞানীরা এখন দিনরাত পরিশ্রম করছেন কোয়ান্টাম-প্রুফ বা পোস্ট-কোয়ান্টাম ক্রিপ্টোগ্রাফি তৈরি করার জন্য, যা কোয়ান্টাম আক্রমণের মুখেও সুরক্ষা বজায় রাখবে।", "clip": "microchip_processor.mp4"}
                ],
                "is_viral_short": False
            },
            {
                "chapter_id": 4,
                "title": "অধ্যায় ৪: জুবায়ের স্যারের বিশ্লেষণ ও চূড়ান্ত মূল্যায়ন",
                "scenes": [
                    {"text": "দর্শক, প্রযুক্তির প্রতিটি পরাশক্তি মানুষের জন্য যেমন অফুরন্ত সম্ভাবনা বয়ে আনে, তেমনি তার সামনে দাঁড় করিয়ে দেয় অস্তিত্বের কঠিন পরীক্ষা।", "clip": "vr_hand_scrolling.mp4"},
                    {"text": "আমাদের দেশেও তরুণ প্রোগ্রামার ও প্রযুক্তিপ্রেমীদের এখনই প্রস্তুতি নিতে হবে কোয়ান্টাম কম্পিউটিং, এআই অটোমেশন ও আধুনিক সাইবার সুরক্ষার এই নতুন বৈশ্বিক যুগের জন্য।", "clip": "smartwatch_hologram.mp4"},
                    {"text": "প্রযুক্তির এই অভাবনীয় অগ্রযাত্রাকে আপনি কীভাবে মূল্যায়ন করছেন? কোয়ান্টাম কম্পিউটার কি মানবজাতির শ্রেষ্ঠতম উদ্ভাবন? কমেন্ট বক্সে আপনার মতামত জানান।", "clip": "sci_fi_hand_device.mp4"},
                    {"text": "ভবিষ্যত প্রযুক্তি, কৃত্রিম বুদ্ধিমত্তা ও সফটওয়্যার অটোমেশনের পরবর্তী পর্বগুলো নিয়মিত দেখতে এখনই চ্যানেলটি সাবস্ক্রাইব করুন এবং বেল আইকনটি অন করে রাখুন। আমি জুবায়ের, বিদায় নিচ্ছি আজকের মতো। দেখা হচ্ছে পরবর্তী বিশেষ পর্বে।", "clip": "outro_slate"}
                ],
                "is_viral_short": True,
                "short_label": "short_3_future_verdict"
            }
        ],
        "tags": [
            "কোয়ান্টাম কম্পিউটার", "Quantum Computing", "Supercomputer", "Tech Documentary",
            "Bangla Tech", "Future Technology", "AI & Robotics", "Jubayer Dev", "Bangla Science",
            "Quantum Physics", "Cyber Security", "Google Quantum AI"
        ]
    }
]


def get_longform_script(index: int = 0) -> dict:
    """৫-৭ মিনিটের একটি সম্পূর্ণ ইউটিউব ডকুমেন্টারি স্ক্রিপ্ট ও এসইও কিট তৈরি করে।"""
    data = CURATED_LONGFORM_DOCUMENTARIES[index % len(CURATED_LONGFORM_DOCUMENTARIES)].copy()

    # সমস্ত সিনের একটি ফ্ল্যাট তালিকা তৈরি
    all_scenes = []
    chapter_markers = []
    viral_shorts = []

    scene_counter = 1
    total_est_seconds = 0.0

    for ch in data["chapters"]:
        ch_title = ch["title"]
        ch_id = ch["chapter_id"]
        ch_start_time = total_est_seconds

        chapter_markers.append({
            "chapter_id": ch_id,
            "title": ch_title,
            "start_time": ch_start_time,
            "scenes_count": len(ch["scenes"])
        })

        ch_scenes = []
        for s_idx, s in enumerate(ch["scenes"]):
            # গড়ে প্রতি বাংলা শব্দের জন্য ০.৪৫ সেকেন্ড
            word_count = len(s["text"].split())
            est_dur = max(4.0, word_count * 0.45)

            sc_item = {
                "scene_id": scene_counter,
                "chapter_id": ch_id,
                "chapter_title": ch_title,
                "text": s["text"],
                "clip": s["clip"],
                "est_duration": est_dur,
                "is_chapter_first_scene": (s_idx == 0)
            }
            all_scenes.append(sc_item)
            ch_scenes.append(sc_item)
            total_est_seconds += est_dur
            scene_counter += 1

        if ch.get("is_viral_short"):
            viral_shorts.append({
                "short_label": ch.get("short_label", f"short_{ch_id}"),
                "chapter_id": ch_id,
                "chapter_title": ch_title,
                "scenes": ch_scenes
            })

    # ক্লিকযোগ্য টাইমস্ট্যাম্প সহ ইউটিউব এসইও ডেসক্রিপশন তৈরি
    timestamps_text = ""
    for cm in chapter_markers:
        m = int(cm["start_time"] // 60)
        s = int(cm["start_time"] % 60)
        time_str = f"{m:02d}:{s:02d}"
        timestamps_text += f"{time_str} - {cm['title']}\n"

    description = (
        f"{data['title']}\n\n"
        f"মানব সভ্যতার পরবর্তী বৈজ্ঞানিক বিপ্লব কোয়ান্টাম কম্পিউটিং নিয়ে বিশেষ বিশ্লেষণমূলক প্রামাণ্যচিত্র।\n\n"
        f"📌 টাইমস্ট্যাম্পস (ভিডিও সূচিপত্র):\n"
        f"{timestamps_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💻 কনটেন্ট প্রযোজনা ও উপস্থাপনা:\n"
        f"Jubayer (Software Engineer & AI Specialist)\n"
        f"ওয়েবসাইট ও পোর্টফোলিও: https://jubayer.dev\n\n"
        f"🔔 ভবিষ্যৎ প্রযুক্তি ও এআই সম্পর্কিত আরও গভীর বিশ্লেষণ দেখতে চ্যানেলটি সাবস্ক্রাইব করে রাখুন!\n"
        f"#QuantumComputing #BanglaTech #FutureTech #JubayerDev #Supercomputer"
    )

    return {
        "title": data["title"],
        "short_title": data["short_title"],
        "theme": data["theme"],
        "total_estimated_duration": total_est_seconds,
        "all_scenes": all_scenes,
        "chapters": chapter_markers,
        "viral_shorts": viral_shorts,
        "description": description,
        "tags": data["tags"]
    }


if __name__ == "__main__":
    doc = get_longform_script()
    print("=" * 60)
    print(f"🎬 দীর্ঘ ইউটিউব ডকুমেন্টারি স্ক্রিপ্ট: {doc['title']}")
    print(f"⏱️ আনুমানিক দৈর্ঘ্য: {doc['total_estimated_duration'] / 60:.1f} মিনিট ({len(doc['all_scenes'])} টি সিন)")
    print(f"📑 মোট অধ্যায়: {len(doc['chapters'])}")
    for c in doc["chapters"]:
        print(f"   - {c['title']}")
    print(f"✂️ অটো-শর্টস রিপারপোজার মার্ক করা হয়েছে: {len(doc['viral_shorts'])} টি")
    print("=" * 60)
    print("✅ লং-ফর্ম স্ক্রিপ্ট ইঞ্জিন সম্পূর্ণ প্রস্তুত!")
