import json
import os
import sys
import base64
import urllib.request

def load_key(path):
    with open(path) as f:
        for line in f:
            if line.startswith("OPENAI_API_KEY="):
                return line.strip().split("=", 1)[1]
    raise SystemExit("key not found in " + path)

def generate(key, prompt, size, out_path):
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps({
            "model": "gpt-image-1",
            "prompt": prompt,
            "size": size,
            "n": 1,
            "background": "transparent",
        }).encode(),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.load(resp)
    b64 = data["data"][0]["b64_json"]
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(b64))
    print("saved", out_path)

STYLE = (
    "Retro run-and-gun arcade video game character sprite, side-view, richly "
    "shaded pixel art in the style of 1990s Neo Geo sprites, crisp clean "
    "outlines, dynamic action pose, full body visible, transparent "
    "background, no text, no watermark, no logo, single isolated character"
)

PROMPTS = {
    "hero": (
        f"{STYLE}. A tough male commando soldier running while firing a "
        "pistol, wearing a red beret, olive tactical vest over tan shirt, "
        "khaki cargo pants, brown boots, tan skin, determined expression, "
        "facing right"
    ),
    "hero_idle": (
        f"{STYLE}. A tough male commando soldier standing ready, holding a "
        "pistol pointed forward, wearing a red beret, olive tactical vest "
        "over tan shirt, khaki cargo pants, brown boots, tan skin, "
        "determined expression, facing right"
    ),
    "hero2": (
        f"{STYLE}. A tough male commando soldier running while firing a "
        "pistol, wearing an olive green forage cap, brown vest over tan "
        "shirt, dark khaki cargo pants, brown boots, tan skin, determined "
        "expression, facing right"
    ),
    "hero3": (
        f"{STYLE}. A tough female commando soldier running while firing a "
        "pistol, wearing a blue bandana, tan tactical vest over olive "
        "shirt, khaki cargo pants, brown boots, tan skin, determined "
        "expression, facing right"
    ),
    "enemy_rifle": (
        f"{STYLE}. An enemy grunt soldier aiming a rifle, wearing an olive "
        "green combat helmet, khaki desert uniform, brown boots, facing "
        "left, slightly ominous"
    ),
    "enemy_runner": (
        f"{STYLE}. An enemy grunt soldier charging forward with a combat "
        "knife raised, wearing a tan pith helmet, khaki desert uniform, "
        "brown boots, aggressive stance, facing right"
    ),
}

if __name__ == "__main__":
    key = load_key(os.path.expanduser("~/dust-battalion/.env.local"))
    name = sys.argv[1]
    out = os.path.expanduser(f"~/dust-battalion/assets/sprite-{name}.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    generate(key, PROMPTS[name], "1024x1024", out)
