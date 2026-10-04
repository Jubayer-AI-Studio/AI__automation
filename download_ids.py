import urllib.request
from pathlib import Path

out_dir = Path('assets/tech_clips/hollywood')
ids = [
    ('robotic_arm_welding', '8328106'),
    ('cybernetic_tech', '7688612'),
    ('microchip_nano', '8328143')
]

for name, vid_id in ids:
    url = f'https://www.pexels.com/download/video/{vid_id}/'
    out_file = out_dir / f"{name}.mp4"
    print(f'Downloading {name} from {url}...')
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as resp, open(out_file, 'wb') as f:
            f.write(resp.read())
        print(f'Done {name}: {out_file.stat().st_size} bytes')
    except Exception as e:
        print(f'Error for {name}: {e}')
