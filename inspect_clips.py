import subprocess
from pathlib import Path
for f in Path('assets/tech_clips').glob('*.mp4'):
    res = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,duration', '-of', 'csv=p=0', str(f)], capture_output=True, text=True).stdout.strip()
    print(f"{f.name}: {res}")
