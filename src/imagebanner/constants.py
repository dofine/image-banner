import os

FILMMODE_DICT = {
    0: "Standard (Provia)",
    288: "Astia",
    512: "Velvia",
    1024: "Velvia",
    1280: "Pro Neg. Std",
    1281: "Pro Neg. Hi",
    1536: "Classic Chrome",
    1792: "Eterna",
    2048: "Classic Negative",
    2304: "Bleach Bypass",
    2560: "Nostalgic Neg",
}

# see https://exiftool.org/TagNames/FujiFilm.html Tag 0x1401

dir_name = os.path.dirname(__file__)
FONT_NAME = os.path.join(dir_name, "../../assets/SmileySans-Oblique.ttf")
# FONT_NAME = 'Futura.ttc'
