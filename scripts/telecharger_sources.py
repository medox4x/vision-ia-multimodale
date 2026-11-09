"""Retélécharge les ressources de la démonstration depuis leurs sources publiques d'origine.

Les fichiers sont placés dans « sources_originales/ » : ils ne remplacent jamais le dossier « assets/ »,
qui contient déjà tout ce dont le notebook a besoin. Ce script sert à vérifier la provenance des données
ou à reconstruire « assets/ » si vous préférez ne pas redistribuer les images.

Usage (depuis la racine du projet) :
    python scripts/telecharger_sources.py              # vidéo nuScenes, extrait MOT17, photo « coffee », facture
    python scripts/telecharger_sources.py --flickr8k   # ajoute les photos et légendes Flickr8k (archive d'environ 1,1 Go)
"""
import argparse
import hashlib
import io
import json
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
DESTINATION = RACINE / "sources_originales"
BOXMOT = "https://raw.githubusercontent.com/mikel-brostrom/boxmot/master/assets/MOT17-mini/train/MOT17-04-FRCNN"
SOURCES = {
    "suivi/nuscenes_mini.mp4": "https://raw.githubusercontent.com/xingyizhou/CenterTrack/master/videos/nuscenes_mini.mp4",
    "suivi/MOT17-04-FRCNN_extrait/gt/gt.txt": f"{BOXMOT}/gt/gt.txt",
    "suivi/MOT17-04-FRCNN_extrait/seqinfo.ini": f"{BOXMOT}/seqinfo.ini",
    **{f"suivi/MOT17-04-FRCNN_extrait/img1/{k:06d}.jpg": f"{BOXMOT}/img1/{k:06d}.jpg" for k in range(1, 9)},
}
FLICKR8K_IMAGES = "https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_Dataset.zip"
FLICKR8K_TEXTE = "https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_text.zip"


def telecharger(url, chemin):
    chemin.parent.mkdir(parents=True, exist_ok=True)
    print(f"  {url}")
    with urllib.request.urlopen(url) as reponse, open(chemin, "wb") as sortie:
        shutil.copyfileobj(reponse, sortie)


def empreinte(chemin):
    return hashlib.sha256(Path(chemin).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--flickr8k", action="store_true", help="télécharge aussi Flickr8k (≈ 1,1 Go)")
    args = parser.parse_args()

    print("1. Vidéo nuScenes et extrait MOT17-04")
    for relatif, url in SOURCES.items():
        telecharger(url, DESTINATION / relatif)
        identique = (RACINE / "assets" / relatif).exists() and empreinte(DESTINATION / relatif) == empreinte(RACINE / "assets" / relatif)
        print(f"    → {relatif} : {'identique à assets/' if identique else 'différent de assets/ (ou absent)'}")

    print("2. Photo « coffee » (scikit-image, CC0)")
    try:
        from PIL import Image
        from skimage import data
        (DESTINATION / "generation").mkdir(parents=True, exist_ok=True)
        Image.fromarray(data.coffee()).save(DESTINATION / "generation" / "cafe_scikit_image.png")
        print("    → generation/cafe_scikit_image.png")
    except ImportError:
        print("    scikit-image absent : pip install scikit-image")

    print("3. Facture fictive (régénérée par scripts/generer_facture.py dans assets/ocr/)")
    subprocess.run([sys.executable, str(RACINE / "scripts" / "generer_facture.py")], check=False)

    if args.flickr8k:
        print("4. Flickr8k : téléchargement des archives puis extraction des seules images utilisées")
        collection = json.loads((RACINE / "assets" / "recherche" / "collection.json").read_text(encoding="utf-8"))
        identifiants = {im["id"] for im in collection["images"]} | {"2414384480_096867d695"}
        archive = DESTINATION / "Flickr8k_Dataset.zip"
        if not archive.exists():
            telecharger(FLICKR8K_IMAGES, archive)
        with zipfile.ZipFile(archive) as z:
            for nom in z.namelist():
                if Path(nom).stem in identifiants and nom.endswith(".jpg") and "__MACOSX" not in nom:
                    (DESTINATION / "flickr8k").mkdir(parents=True, exist_ok=True)
                    (DESTINATION / "flickr8k" / Path(nom).name).write_bytes(z.read(nom))
        with urllib.request.urlopen(FLICKR8K_TEXTE) as reponse:
            with zipfile.ZipFile(io.BytesIO(reponse.read())) as z:
                legendes = z.read("Flickr8k.token.txt").decode("utf-8")
        lignes = [l for l in legendes.splitlines() if l.split(".jpg#")[0] in identifiants]
        (DESTINATION / "flickr8k" / "legendes.txt").write_text("\n".join(lignes), encoding="utf-8")
        print(f"    → {len(list((DESTINATION / 'flickr8k').glob('*.jpg')))} images et {len(lignes)} légendes")
    print(f"Terminé : {DESTINATION}")


if __name__ == "__main__":
    main()
