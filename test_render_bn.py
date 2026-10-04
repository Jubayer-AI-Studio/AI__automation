import subprocess

font = "C\\:/Users/ASSDI/Desktop/facebook/assets/fonts/HindSiliguri-Bold.ttf"
text = "রোবোটিক্স ও এআই ইঞ্জিনিয়ারিং"
cmd = [
    "ffmpeg", "-y", "-f", "lavfi", "-i", "color=s=1080x300:c=black",
    "-vf", f"drawtext=fontfile='{font}':text='{text}':text_shaping=1:fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2",
    "-vframes", "1", "temp/test_drawtext_shaping.jpg"
]
subprocess.run(cmd, check=True)
print("Saved test_drawtext_shaping.jpg")
