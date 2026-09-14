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
    "shot": ("Dry punchy arcade cabinet pistol gunshot, tight snappy crack with "
             "a very short metallic tail, no reverb, loud and close, classic "
             "16-bit run and gun arcade game", 0.5),
    "shotgun": ("Heavy arcade shotgun blast, thick low punch with a bright "
                "crack and a quick shell-pump click, dry, classic 16-bit run "
                "and gun arcade game", 0.7),
    "boom": ("Big dry arcade explosion, deep thumping low boom with bright "
             "crackling debris on top, punchy attack, short tail, classic "
             "16-bit run and gun arcade game", 1.1),
    "jump": ("Short arcade jump sound, quick upward pitched blip with a small "
             "whoosh, dry, classic 16-bit arcade game", 0.5),
    "pickup": ("Bright arcade power-up pickup jingle, three quick ascending "
               "coin-like chimes, cheerful, classic 16-bit arcade game", 0.6),
    "knife": ("Fast metallic arcade knife slash, sharp steel whoosh with a "
              "short ring, dry, classic 16-bit arcade game", 0.5),
    "death": ("Arcade player death sting, dramatic short descending tone with "
              "a low thud, classic 16-bit run and gun arcade game", 0.8),
    "rescue": ("Short triumphant arcade fanfare for rescuing a prisoner, "
               "bright ascending horns and a chime, classic 16-bit arcade "
               "game", 1.0),
    "alarm": ("Menacing arcade boss warning alarm, low pulsing siren with "
              "metallic tension, classic 16-bit arcade game", 1.2),
}

if __name__ == "__main__":
    key = load_key(os.path.expanduser("~/dust-battalion/.env.local"), "ELEVENLABS_API_KEY")
    names = sys.argv[1:] or list(SFX.keys())
    out_dir = os.path.expanduser("~/dust-battalion/assets/sfx")
    os.makedirs(out_dir, exist_ok=True)
    for name in names:
        prompt, dur = SFX[name]
        generate(key, prompt, dur, os.path.join(out_dir, f"{name}.mp3"))
