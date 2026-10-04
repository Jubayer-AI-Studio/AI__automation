import subprocess
from pathlib import Path

ass_content = """[Script Info]
Title: Bengali Test
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Hind Siliguri,52,&H0000FFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,2,2,30,30,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:05.00,Default,,0,0,0,,রোবোটিক্স ও এআই ইঞ্জিনিয়ারিং
"""

with open("temp/test_sub.ass", "w", encoding="utf-8") as f:
    f.write(ass_content)

cmd = [
    "ffmpeg", "-y", "-f", "lavfi", "-i", "color=s=1080x1920:c=black",
    "-vf", "ass=temp/test_sub.ass",
    "-vframes", "1", "temp/test_ass_bn.jpg"
]
subprocess.run(cmd, check=True)
print("Saved test_ass_bn.jpg")
