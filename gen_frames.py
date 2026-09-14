"""Genera frames extra de un ciclo de carrera usando /v1/images/edits.

Pasar el sprite base como referencia mantiene al personaje consistente entre
frames (misma paleta, proporciones y angulo), que es justo lo que falla al
generar cada frame desde cero.
"""
import os
import sys
import json
import base64
import uuid
import urllib.request

BASE = os.path.expanduser("~/dust-battalion")

def load_key(name):
    with open(os.path.join(BASE, ".env.local")) as f:
        for line in f:
            if line.startswith(name + "="):
                return line.strip().split("=", 1)[1]
    raise SystemExit(name + " not found")

def multipart(fields, files):
    boundary = "----gen" + uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, (fname, data) in files.items():
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; "
                 f"filename=\"{fname}\"\r\nContent-Type: image/png\r\n\r\n").encode()
        body += data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return body, "multipart/form-data; boundary=" + boundary

def edit(key, base_png, prompt, out_path):
    with open(base_png, "rb") as f:
        img = f.read()
    body, ctype = multipart(
        {"model": "gpt-image-1", "prompt": prompt, "size": "1024x1024",
         "background": "transparent", "n": "1"},
        {"image[]": (os.path.basename(base_png), img)},
    )
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/edits", data=body,
        headers={"Authorization": "Bearer " + key, "Content-Type": ctype},
        method="POST")
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.load(resp)
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(data["data"][0]["b64_json"]))
    print("saved", out_path)

KEEP = ("Keep the exact same character, same red beret, same olive vest, same "
        "khaki pants, same brown boots, same colors, same pixel art style, "
        "same size and same camera angle, facing right, transparent "
        "background. Only change the pose of the legs and arms. ")

FRAMES = {
    "hero_run_a": KEEP + ("Running cycle frame: both legs passing under the "
                          "body close together, knees slightly bent, body at "
                          "its highest point."),
    "hero_run_b": KEEP + ("Running cycle frame: left leg stretched forward "
                          "with the heel about to touch the ground and the "
                          "right leg stretched back behind, wide stride."),
    "hero_run_c": KEEP + ("Running cycle frame: legs crossing under the body "
                          "with the right knee lifted high in front, body "
                          "slightly lowered."),
}

if __name__ == "__main__":
    key = load_key("OPENAI_API_KEY")
    base = os.path.join(BASE, "assets", "sprite-hero.png")
    for name in (sys.argv[1:] or FRAMES.keys()):
        edit(key, base, FRAMES[name],
             os.path.join(BASE, "assets", f"sprite-{name}.png"))
