import subprocess
from pathlib import Path

for name in ['robotic_arm_welding', 'cybernetic_tech', 'microchip_nano']:
    in_f = Path('assets/tech_clips/hollywood') / f"{name}.mp4"
    out_f = Path('temp') / f"frame_{name}.jpg"
    subprocess.run(['ffmpeg', '-y', '-ss', '00:00:02', '-i', str(in_f), '-vframes', '1', '-q:v', '2', str(out_f)], capture_output=True)
