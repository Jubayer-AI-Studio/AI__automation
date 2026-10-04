import subprocess
from pathlib import Path

clips = ['humanoid_robot.mp4', 'robot_walking.mp4', 'cyborg_hologram.mp4', 'microchip_processor.mp4', 'red_circuit_board.mp4', 'quantum_server_room.mp4', 'cyber_code_matrix.mp4', 'hand_projecting_hologram.mp4']
for c in clips:
    in_file = Path('assets/tech_clips') / c
    out_frame = Path('temp') / f"frame_{c}.jpg"
    subprocess.run(['ffmpeg', '-y', '-ss', '00:00:03', '-i', str(in_file), '-vframes', '1', '-q:v', '2', str(out_frame)], capture_output=True)
    print(f"Extracted {out_frame.name}")
