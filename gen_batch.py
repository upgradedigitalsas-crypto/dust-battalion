"""Genera en lote los assets que corresponden a objetos que YA existen en el
juego. No se generan unidades que no estan implementadas (robots, helicopteros,
hover bikes): eso seria gastar creditos en arte que nadie dibuja en pantalla.
"""
import os
import sys
import json
import base64
import urllib.request

BASE = os.path.expanduser("~/dust-battalion")
OUT = os.path.join(BASE, "assets")

def load_key(name):
    with open(os.path.join(BASE, ".env.local")) as f:
        for line in f:
            if line.startswith(name + "="):
                return line.strip().split("=", 1)[1]
    raise SystemExit(name + " not found")

def gen(key, prompt, out_path, size="1024x1024", transparent=True):
    payload = {"model": "gpt-image-1", "prompt": prompt, "size": size, "n": 1}
    if transparent:
        payload["background"] = "transparent"
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.load(resp)
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(data["data"][0]["b64_json"]))
    print("saved", os.path.basename(out_path), flush=True)

PIX = ("Retro run-and-gun arcade video game asset, richly shaded pixel art in "
       "the style of 1990s Neo Geo sprites, crisp clean outlines, side view, "
       "transparent background, no text, no watermark, no logo, single "
       "isolated object, centered")

ITEMS = {
    # vehiculos y unidades grandes que ya existen en el juego
    "tank": PIX + ". A battered desert military tank seen from the side, "
                  "sand-colored armor with olive panels, tracks, a forward "
                  "cannon, facing right",
    "turret": PIX + ". A fixed enemy gun emplacement: sandbag base with a "
                    "mounted machine gun on a tripod, desert colors",
    "boss": PIX + ". A huge menacing armored siege vehicle boss for the final "
                  "fight: massive dark steel hull, heavy frontal cannon, "
                  "red warning lights, riveted plating, facing left, "
                  "imposing and wide",
    "hostage": PIX + ". A ragged prisoner of war in a torn tan shirt with his "
                     "hands tied, bearded, standing, looking relieved, "
                     "facing right",
    # obstaculos y props del escenario
    "crate": PIX + ". A wooden supply crate with metal corner brackets and a "
                   "painted ammunition stencil, slightly weathered",
    "barrel": PIX + ". A rusty steel fuel barrel standing upright, dented, "
                    "desert dust on it",
    "sandbags": PIX + ". A low stack of military sandbags forming a barricade, "
                      "tan burlap, weathered",
    # efectos
    "explosion": PIX + ". A bright orange fireball explosion with black smoke "
                       "curling at the edges and yellow-white hot core, "
                       "dramatic arcade style",
}

GROUND = ("Seamless horizontally tileable texture strip of cracked sun-baked "
          "desert ground with scattered pebbles, gravel and tire ruts, rich "
          "warm sand and brown tones, painted pixel art style for a 2D "
          "side-scrolling game floor, top edge slightly lighter, no text, "
          "no characters, no watermark")

GROUND_CITY = ("Seamless horizontally tileable texture strip of a war-torn "
               "city street: broken asphalt and cobblestones with rubble, "
               "cracks and dust, cool grey and brown tones, painted pixel art "
               "style for a 2D side-scrolling game floor, no text, no "
               "characters, no watermark")

if __name__ == "__main__":
    key = load_key("OPENAI_API_KEY")
    names = sys.argv[1:] or list(ITEMS) + ["ground_desert", "ground_city"]
    for n in names:
        try:
            if n == "ground_desert":
                gen(key, GROUND, os.path.join(OUT, "ground-desert.png"),
                    size="1536x1024", transparent=False)
            elif n == "ground_city":
                gen(key, GROUND_CITY, os.path.join(OUT, "ground-city.png"),
                    size="1536x1024", transparent=False)
            else:
                gen(key, ITEMS[n], os.path.join(OUT, f"sprite-{n}.png"))
        except Exception as e:
            print("FALLO", n, e, flush=True)
