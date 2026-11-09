# Provenance et licences des ressources

Toutes les ressources de ce dossier sont **celles de la présentation** (mêmes fichiers d'origine), sauf mention contraire. Elles sont fournies pour un **usage pédagogique et non commercial**. Le script `scripts/telecharger_sources.py` permet de les retrouver depuis leurs sources publiques.

| Fichier | Contenu | Source | Licence / conditions |
|---|---|---|---|
| `suivi/nuscenes_mini.mp4` | 40 images clés (une toutes les 0,5 s, soit 20 s ; fichier lu à 20 images/s ; 800 × 450) d'une rue de Boston — diapositives 2, 4 et 5 | jeu de données nuScenes (Caesar et al., 2020), vidéo distribuée dans le dépôt CenterTrack : `https://raw.githubusercontent.com/xingyizhou/CenterTrack/master/videos/nuscenes_mini.mp4` | nuScenes : CC BY-NC-SA 4.0 (usage non commercial, attribution, partage dans les mêmes conditions) |
| `suivi/MOT17-04-FRCNN_extrait/` | 8 premières images de la séquence MOT17-04 et vérité terrain officielle (`gt/gt.txt`) — image de titre de la présentation | benchmark MOTChallenge MOT17 (Milan et al., 2016), extrait distribué dans le dépôt BoxMOT (`assets/MOT17-mini/train/MOT17-04-FRCNN`) | MOTChallenge : CC BY-NC-SA 3.0 |
| `generation/cafe_scikit_image.jpg` | photo d'une tasse d'expresso — diapositives 7 à 9 | image `coffee` de scikit-image (`skimage.data.coffee()`), photo de Rachel Michetti, offerte par Pikolo Espresso Bar | CC0 (domaine public) |
| `ocr/facture_*.jpg`, `ocr/facture_propre.png` | facture **fictive** « Imprimerie Atlas Numérique » — diapositives 10 à 12 | créée pour ce projet par `scripts/generer_facture.py` (le scan est identique, pixel pour pixel, à celui de la présentation) | libre de droits |
| `ocr/facture_reference.json` | transcription vérifiée, ligne par ligne, avec la position de chaque ligne | texte exact utilisé pour générer la facture | libre de droits |
| `legendage/quai_metro_2414384480.jpg` | quai de métro — diapositives 13 à 15 | Flickr8k (Hodosh et al., 2013), image `2414384480_096867d695.jpg` | usage académique ; droits des photographes Flickr |
| `legendage/references.json` | 5 légendes humaines anglaises de Flickr8k (recopiées telles quelles) + exemple pédagogique français de la diapositive 15 | `Flickr8k.token.txt` ; phrases françaises écrites pour la présentation | usage académique |
| `recherche/images/*.jpg` | 12 photos de la galerie de la diapositive 16 | Flickr8k (identifiant = nom du fichier) | usage académique ; droits des photographes Flickr |
| `recherche/collection.json` | descriptions, légendes Flickr8k, requêtes et étiquettes de pertinence | étiquettes attribuées à la main par l'auteur à partir des légendes Flickr8k (ce n'est pas une vérité terrain officielle) | usage académique |

Miroir public de Flickr8k utilisé : `https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_Dataset.zip` et `Flickr8k_text.zip`.

**Modèles pré-entraînés** (non inclus : téléchargés et mis en cache à l'exécution)

| Modèle | Source | Taille |
|---|---|---|
| YOLO11n (Ultralytics) | GitHub, `ultralytics/assets` | 5,4 Mo |
| CLIP ViT-B/32 (OpenAI) | Hugging Face (`timm/vit_base_patch32_clip_224.openai`) via OpenCLIP | ≈ 600 Mo |
| OpenCLIP ViT-B/32 LAION-400M (modèle de repli) | GitHub, `mlfoundations/open_clip`, version `v0.2-weights` | ≈ 600 Mo |
| BLIP base / large (Salesforce) | Hugging Face | ≈ 1 Go / 1,9 Go |
| Stable Diffusion 1.5 (miroir `sd-legacy`) ou SD-Turbo (Stability AI) | Hugging Face | ≈ 2 à 5 Go |
| Tesseract 5 + modèle `fra` | paquets système (apt, installateur Windows) | ≈ 30 Mo |
