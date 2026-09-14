import os
import sys
import json
import urllib.request

def load_key(path, name):
    with open(path) as f:
        for line in f:
            if line.startswith(name + "="):
                return line.strip().split("=", 1)[1]
    raise SystemExit(name + " not found in " + path)

def generate(key, prompt, duration, out_path):
    req = urllib.request.Request(
        "https://api.elevenlabs.io/v1/sound-generation",
        data=json.dumps({
            "text": prompt,
            "duration_seconds": duration,
            "prompt_influence": 0.4,
        }).encode(),
        headers={
            "xi-api-key": key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        audio = resp.read()
    with open(out_path, "wb") as f:
        f.write(audio)
    print("saved", out_path, len(audio), "bytes")

SFX = {
    "shot": ("Single sharp retro arcade pistol gunshot, punchy, short, 8-bit war game sound effect", 0.6),
    "boom": ("Big punchy retro arcade explosion, deep boom with crackle, short, 8-bit war game sound effect", 1.2),
    "jump": ("Retro arcade video game jump sound, short upward whoosh blip, 8-bit style", 0.5),
    "pickup": ("Cheerful retro arcade item pickup chime, short ascending blips, 8-bit style", 0.5),
    "knife": ("Quick sharp retro arcade knife slash whoosh, short, 8-bit war game sound effect", 0.5),
    "death": ("Retro arcade character death sound, descending sad blip, short, 8-bit style", 0.6),
}

if __name__ == "__main__":
    key = load_key(os.path.expanduser("~/dust-battalion/.env.local"), "ELEVENLABS_API_KEY")
    names = sys.argv[1:] or list(SFX.keys())
    out_dir = os.path.expanduser("~/dust-battalion/assets/sfx")
    os.makedirs(out_dir, exist_ok=True)
    for name in names:
        prompt, dur = SFX[name]
        generate(key, prompt, dur, os.path.join(out_dir, f"{name}.mp3"))
