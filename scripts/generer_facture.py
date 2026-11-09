"""Génère la facture fictive de la présentation (diapositives 10 à 12) et sa transcription de référence.

Sorties (dans assets/ocr/) :
  - facture_propre.png          : rendu net du document (1240 × 1180 px, 150 dpi)
  - facture_scan.jpg            : version « numérisée » utilisée dans la présentation
  - facture_scan_degradee.jpg   : condition plus difficile (basse résolution, compression forte)
  - facture_reference.json      : transcription vérifiée, ligne par ligne, avec la position de chaque ligne

Le document est entièrement fictif : il sert uniquement à démontrer l'OCR.
Usage : python scripts/generer_facture.py   (depuis la racine du projet)
"""
import json
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

RACINE = Path(__file__).resolve().parents[1]
SORTIE = RACINE / "assets" / "ocr"
SORTIE.mkdir(parents=True, exist_ok=True)

S = 2  # suréchantillonnage pour un rendu net
W, H = 1240 * S, 1180 * S
POLICES = {
    "Regular": ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "arial.ttf", "DejaVuSans.ttf"],
    "Bold": ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"],
    "Italic": ["/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf", "ariali.ttf", "DejaVuSans-Oblique.ttf"],
}


def police(style, taille):
    """Charge Liberation Sans (métriques d'Arial) ; sinon Arial ou DejaVu selon le système."""
    for chemin in POLICES[style]:
        try:
            return ImageFont.truetype(chemin, taille * S)
        except OSError:
            continue
    raise OSError("Aucune police TrueType trouvée : installez Liberation Sans ou DejaVu Sans.")


INK, GREY, LINE, ACC = (28, 34, 44), (95, 104, 116), (190, 196, 204), (31, 86, 110)
img = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(img)
X0, X1 = 90 * S, (1240 - 90) * S
lignes = []  # transcription de référence : (champ, texte, boîte)


def ecrire(champ, xy, texte, style, taille, couleur, anchor="la", groupe=None):
    """Dessine un texte et mémorise sa boîte englobante (coordonnées de l'image finale)."""
    f = police(style, taille)
    d.text(xy, texte, font=f, fill=couleur, anchor=anchor)
    x0, y0, x1, y1 = d.textbbox(xy, texte, font=f, anchor=anchor)
    boite = [x0 / S, y0 / S, x1 / S, y1 / S]
    if groupe is not None and lignes and lignes[-1]["champ"] == groupe:
        # plusieurs textes sur une même ligne visuelle (ligne de tableau) : on les fusionne
        b = lignes[-1]["boite"]
        lignes[-1]["boite"] = [min(b[0], boite[0]), min(b[1], boite[1]), max(b[2], boite[2]), max(b[3], boite[3])]
        lignes[-1]["morceaux"].append((boite[0], texte))
    else:
        lignes.append({"champ": groupe or champ, "boite": boite, "morceaux": [(boite[0], texte)]})


# --- en-tête : émetteur
d.rectangle([X0, 80 * S, X0 + 64 * S, 144 * S], fill=ACC)
ecrire("Logo", (X0 + 32 * S, 112 * S), "AN", "Bold", 30, "white", anchor="mm")
ecrire("Émetteur", (X0 + 84 * S, 84 * S), "IMPRIMERIE ATLAS NUMÉRIQUE", "Bold", 25, INK)
ecrire("Adresse émetteur", (X0 + 84 * S, 118 * S), "12, rue des Orangers – 10000 Rabat", "Regular", 17, GREY)
ecrire("Téléphone", (X0 + 84 * S, 142 * S), "Tél. : 05 37 00 00 00", "Regular", 17, GREY)
ecrire("Type de document", (X1, 80 * S), "FACTURE", "Bold", 40, ACC, anchor="ra")
ecrire("Numéro de facture", (X1, 136 * S), "N° FA-2026-0147", "Bold", 20, INK, anchor="ra")
ecrire("Date", (X1, 166 * S), "Date : 14/10/2026", "Regular", 18, INK, anchor="ra")
ecrire("Échéance", (X1, 192 * S), "Échéance : 13/11/2026", "Regular", 18, GREY, anchor="ra")

# --- client
ecrire("Mention client", (X0, 250 * S), "Facturé à", "Bold", 16, GREY)
ecrire("Client", (X0, 276 * S), "Laboratoire Data & IA", "Bold", 20, INK)
ecrire("Adresse client", (X0, 304 * S), "Campus universitaire – Rabat", "Regular", 18, INK)

# --- tableau des prestations
ty = 380 * S
cols = [X0, 690 * S, 820 * S, 990 * S, X1]
d.rectangle([X0, ty, X1, ty + 44 * S], fill=(232, 238, 242))
entetes = ["Désignation", "Qté", "P.U. HT", "Montant HT"]
ecrire("x", (X0 + 14 * S, ty + 12 * S), entetes[0], "Bold", 18, INK, groupe="En-tête du tableau")
for i, h in enumerate(entetes[1:], start=1):
    ecrire("x", (cols[i + 1] - 14 * S, ty + 12 * S), h, "Bold", 18, INK, anchor="ra", groupe="En-tête du tableau")
prestations = [("Impression affiches A2 couleur", "40", "18,00", "720,00"),
               ("Reliure de rapports (dos carré)", "8", "25,00", "200,00"),
               ("Cartes de visite (boîte de 250)", "2", "60,00", "120,00")]
y = ty + 44 * S
for k, r in enumerate(prestations, start=1):
    y += 16 * S
    ecrire("x", (X0 + 14 * S, y), r[0], "Regular", 18, INK, groupe=f"Ligne {k} du tableau")
    for i, v in enumerate(r[1:], start=1):
        ecrire("x", (cols[i + 1] - 14 * S, y), v, "Regular", 18, INK, anchor="ra", groupe=f"Ligne {k} du tableau")
    y += 34 * S
    d.line([X0, y, X1, y], fill=LINE, width=S)

# --- totaux
y += 30 * S
lab_x, val_x = 820 * S, X1 - 14 * S
for lab, val in [("Total HT", "1 040,00 DH"), ("TVA 20 %", "208,00 DH")]:
    ecrire("x", (lab_x, y), lab, "Regular", 18, INK, groupe=lab)
    ecrire("x", (val_x, y), val, "Regular", 18, INK, anchor="ra", groupe=lab)
    y += 38 * S
d.rectangle([lab_x - 16 * S, y - 12 * S, X1, y + 42 * S], fill=(232, 238, 242))
ecrire("x", (lab_x, y), "Total TTC :", "Bold", 21, INK, groupe="Total TTC")
ecrire("x", (val_x, y), "1 248,00 DH", "Bold", 21, INK, anchor="ra", groupe="Total TTC")
y += 90 * S
ecrire("Montant en lettres", (X0, y), "Arrêtée la présente facture à la somme de mille deux cent quarante-huit dirhams.", "Italic", 17, INK)
y += 60 * S
d.line([X0, y, X1, y], fill=LINE, width=S)
ecrire("Mention légale", (X0, y + 14 * S), "Document fictif – exemple pédagogique pour la démonstration de l'OCR.", "Regular", 15, GREY)

# --- rendu net
propre = img.resize((W // S, H // S), Image.LANCZOS)
propre.save(SORTIE / "facture_propre.png")

# --- aspect « numérisé » (identique à la présentation : teinte papier, bruit, rotation, flou, JPEG)
random.seed(3)
np.random.seed(3)
papier = np.array(propre.convert("RGB")).astype(np.float32) * (np.array([247, 245, 239], np.float32) / 255.0)
yy, xx = np.mgrid[0:papier.shape[0], 0:papier.shape[1]]
vignette = 1 - 0.05 * (((xx - papier.shape[1] / 2) / papier.shape[1]) ** 2 + ((yy - papier.shape[0] / 2) / papier.shape[0]) ** 2) * 4
papier *= vignette[..., None]
papier += np.random.normal(0, 3.0, papier.shape)
scan = Image.fromarray(np.clip(papier, 0, 255).astype(np.uint8))
scan = scan.rotate(-0.45, resample=Image.BICUBIC, expand=False, fillcolor=(236, 234, 228))
scan = scan.filter(ImageFilter.GaussianBlur(0.55))
scan.save(SORTIE / "facture_scan.jpg", quality=72)

# --- condition dégradée : résolution divisée par ~2,4 puis compression JPEG forte (mêmes dimensions finales)
petite = scan.resize((int(scan.width * 0.42), int(scan.height * 0.42)), Image.BILINEAR)
degradee = petite.resize(scan.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.6))
degradee.save(SORTIE / "facture_scan_degradee.jpg", quality=35)

# --- transcription de référence (texte de chaque ligne visuelle, de gauche à droite)
reference = []
for ligne in lignes:
    texte = " ".join(t for _, t in sorted(ligne["morceaux"]))
    reference.append({"champ": ligne["champ"], "texte": texte, "boite": [round(v, 1) for v in ligne["boite"]]})
meta = {
    "description": "Transcription vérifiée de la facture fictive (texte exact utilisé pour générer l'image).",
    "taille_image": [W // S, H // S],
    "lignes": reference,
}
(SORTIE / "facture_reference.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{len(reference)} lignes de référence écrites dans {SORTIE}")
