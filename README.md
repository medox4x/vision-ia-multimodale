# Démonstration visuelle : vision par ordinateur, IA multimodale et métriques d'évaluation

Projet compagnon de la présentation **« Vision par ordinateur et IA multimodale : applications et métriques d'évaluation »** (Mohamed Haddassy, Master 2 Data & Intelligence Artificielle, INPT Rabat), version finalisée en 19 diapositives.

## 1. Objectif

Le notebook `Demonstration_IA_Notebook_Visuel.ipynb` rejoue les exemples de la présentation avec de vrais modèles. Chaque section suit la même chaîne, avec peu de texte et beaucoup de figures :

**DONNÉES → MODÈLE → PRÉDICTION → VISUALISATION → ÉVALUATION → INTERPRÉTATION**

## 2. Contenu du projet

```
Projet_Demonstration_IA_Multimodale/
├── Demonstration_IA_Notebook_Visuel.ipynb   notebook principal (sections 0 à 5 + synthèse)
├── README.md                                ce fichier
├── requirements.txt                         dépendances Python
├── assets/                                  données d'entrée (≈ 5 Mo) — provenance et licences : assets/SOURCES.md
│   ├── suivi/        scène nuScenes (diapositives 4 et 5) + extrait MOT17-04 avec vérité terrain officielle
│   ├── generation/   photo « coffee » des diapositives 7 à 9 (CC0)
│   ├── ocr/          facture fictive des diapositives 10 à 12, version dégradée, transcription de référence
│   ├── legendage/    photo Flickr8k des diapositives 13 à 15 et ses 5 légendes humaines
│   └── recherche/    les 12 photos Flickr8k de la galerie de la diapositive 16 + 4 requêtes étiquetées
├── scripts/
│   ├── generer_facture.py        régénère la facture et sa transcription (identique au pixel près)
│   └── telecharger_sources.py    retélécharge les données depuis leurs sources publiques d'origine
└── validation/
    ├── RAPPORT_VALIDATION.md     ce qui a été exécuté pour valider le projet, et comment
    └── execution_mode_A.html     notebook exécuté en mode A (aperçu des figures et des résultats)
```

Créés à l'exécution : `modeles/` (poids téléchargés) et `resultats/` (figures). Les poids des modèles ne sont **pas** inclus dans l'archive.

## 3. Structure du notebook et lien avec les diapositives

| Section | Diapositives | Modèle | Ce qui est réellement calculé | Exemple de la diapositive (recalculé à part) |
|---|---|---|---|---|
| 0. Entraîner, valider, tester | 3 | petit réseau convolutif **entraîné dans le notebook** | courbes de perte et d'exactitude (entraînement / validation), test final, matrice de confusion | — |
| 1. Suivi d'objets | 4 – 6 | YOLO11n + ByteTrack | suivi de la scène nuScenes ; MOTA, IDF1 et **HOTA** sur MOT17-04 (vérité terrain officielle) | MOTA = 1 − 3/10 = 70 % |
| 2. Génération d'images | 7 – 9 | Stable Diffusion (mode B) ; CLIP | vraies étapes du débruitage (mode B) ; accord texte-image CLIP ; nuage de caractéristiques (mode B) | FID à 1 dimension = 2 ; biais du FID selon le nombre d'images |
| 3. OCR | 10 – 12 | Tesseract 5 | CER, WER, correspondance exacte, S/D/I, deux conditions, deux normalisations | « 1 248 » lu « 7 248 » : CER = 1/23 ≈ 4,3 % |
| 4. Légendage | 13 – 15 | BLIP base (+ large en mode B) | BLEU, METEOR, **CIDEr-D** pour plusieurs candidates | BLEU-1 = 0,75 ; phrase « bus » = 0,875 |
| 5. Recherche image-texte | 16 – 18 | CLIP | classements, Recall@1/3/5, Precision@K, MRR, effet de la langue | rangs 2, 1, 3, 7 → Recall@3 = 75 % |
| Synthèse | 19 | — | tableau construit à partir des résultats de l'exécution | — |

Chaque figure porte une étiquette : **RÉSULTAT RÉEL**, **CALCUL PÉDAGOGIQUE**, **ILLUSTRATION CONCEPTUELLE** ou **DONNÉES D'ENTRÉE**. Les modèles des sections 1 à 5 sont **pré-entraînés** : le notebook ne prétend jamais les avoir entraînés. Seul le petit réseau de la section 0 est réellement entraîné.

**Contrôles interactifs** (ipywidgets, facultatifs) : parcourir la vidéo image par image, choisir une ligne de la facture et la normalisation, écrire sa propre légende, changer la requête et K. Sans ipywidgets, le notebook affiche une vue fixe.

## 4. Prérequis

| | Mode A — démonstration rapide | Mode B — démonstration complète |
|---|---|---|
| Python | 3.10 à 3.13 | 3.10 à 3.13 |
| Processeur graphique | non nécessaire | GPU NVIDIA CUDA conseillé (≥ 6 Go ; T4 de Colab : 16 Go) ; puce Apple (MPS) possible mais lente |
| Mémoire vive | 4 Go | 8 Go et plus |
| Espace disque (modèles) | ≈ 2 Go (BLIP base 1 Go, CLIP 0,6 Go, YOLO11n 5 Mo) | + ≈ 3 Go (Stable Diffusion 1.5) + 1,9 Go (BLIP large) |
| Internet | au premier lancement (téléchargement des modèles) | idem |
| Programme externe | Tesseract 5 + modèle français | idem |
| Durée indicative | 5 à 10 min au premier lancement, ≈ 1 min ensuite | 10 à 15 min au premier lancement |

## 5. Exécution dans Google Colab (recommandé)

1. Ouvrez [Google Colab](https://colab.research.google.com), puis **Fichier → Importer le notebook** et choisissez `Demonstration_IA_Notebook_Visuel.ipynb`.
2. Pour le **mode B** : **Exécution → Modifier le type d'exécution → GPU (T4)**.
3. Dans la première cellule de code, choisissez `MODE = "A"` ou `MODE = "B"`.
4. **Exécution → Tout exécuter.** La deuxième cellule installe les paquets manquants et Tesseract (≈ 1 minute) ; la troisième vous demande de **téléverser l'archive** `Projet_Demonstration_IA_Multimodale.zip`, puis la décompresse.
5. Variante : copiez le dossier décompressé dans `Mon Drive`, montez Google Drive (`from google.colab import drive; drive.mount('/content/drive')`), puis relancez la troisième cellule.

## 6. Exécution locale

### Ubuntu

```bash
sudo apt update && sudo apt install -y tesseract-ocr tesseract-ocr-fra
cd Projet_Demonstration_IA_Multimodale
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
jupyter lab Demonstration_IA_Notebook_Visuel.ipynb
```

### Windows 10 / 11

1. Installez Python 3.11 ou 3.12 depuis [python.org](https://www.python.org) (cochez « Add Python to PATH »).
2. Installez Tesseract avec l'installateur de l'université de Mannheim ([UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki)) en cochant la langue **French**. Le notebook trouve automatiquement `C:\Program Files\Tesseract-OCR\tesseract.exe`.
3. Dans PowerShell :

```powershell
cd Projet_Demonstration_IA_Multimodale
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
jupyter lab Demonstration_IA_Notebook_Visuel.ipynb
```

### GPU NVIDIA en local

Installez **d'abord** la version de PyTorch adaptée à votre carte avec la commande de [pytorch.org/get-started/locally](https://pytorch.org/get-started/locally/), puis `pip install -r requirements.txt`. Le notebook détecte le GPU lui-même ; aucune cellule ne suppose sa présence.

## 7. Pendant la soutenance

- Exécutez d'abord la **préparation** (6 premières cellules de code), puis la section qui correspond à la diapositive affichée (tableau de la partie 3).
- Les sections 1 à 5 peuvent être exécutées seules, dans n'importe quel ordre, après la préparation. La synthèse indique « non calculé » pour les sections non exécutées.
- Paramètres de la première cellule : `MODE` (`"A"` ou `"B"`), `GENERER_IMAGE_SUR_CPU` (génération sans GPU avec SD-Turbo, ≈ 5 Go et plusieurs minutes), `GRAINE` (reproductibilité).

## 8. Erreurs fréquentes

| Symptôme | Cause probable | Solution |
|---|---|---|
| « Dossier « assets/ » introuvable » | notebook ouvert hors du dossier du projet | ouvrez-le depuis la racine du projet ; dans Colab, téléversez l'archive |
| « Tesseract introuvable » | programme Tesseract non installé | voir partie 6 ; sous Windows, vérifiez le chemin d'installation |
| « modèle français : ABSENT » | langue française de Tesseract absente | `sudo apt install tesseract-ocr-fra`, ou cochez *French* dans l'installateur Windows |
| `No module named 'lap'` | dépendance du suivi d'Ultralytics | `pip install lap` |
| « Installez ipywidgets… » | contrôles interactifs indisponibles | `pip install ipywidgets` (déjà présent dans Colab) ; le reste du notebook fonctionne sans |
| « CLIP d'OpenAI indisponible… modèle de repli » | Hugging Face inaccessible | le notebook continue avec OpenCLIP ViT-B/32 (LAION-400M, poids sur GitHub) ; le score s'appelle alors « score de type CLIPScore » |
| « Salesforce/blip-… indisponible » | Hugging Face inaccessible | rétablissez l'accès ; **aucune légende n'est inventée** à la place |
| METEOR affiché « — » | ressource WordNet de NLTK absente | `import nltk; nltk.download("wordnet")` ; derrière un proxy de confiance, NLTK ≥ 3.10 peut demander `NLTK_ALLOW_PROXIED_URLOPEN=1` |
| « génération ignorée » | pas de GPU (mode A) | comportement normal ; passez en mode B avec un GPU |
| Scores différents de `validation/` | autre CLIP (OpenAI ou repli), autre matériel, autres versions | normal : toutes les interprétations sont calculées à partir des valeurs obtenues |
| `jupyter nbconvert --execute` bloqué sur une cellule interactive | ancienne version de ce notebook | la version actuelle affiche la vue initiale hors du widget : mettez le notebook à jour |

## 9. Honnêteté scientifique

- Les nombres des diapositives (MOTA = 70 %, FID = 2, CER = 4,3 %, BLEU-1 = 0,75, Recall@3 = 75 %) sont recalculés dans des cellules **pédagogiques**, séparées des **mesures réelles**.
- Le modèle n'est **jamais** comparé à ses propres prédictions : la vidéo nuScenes sert à visualiser ; MOTA, IDF1 et HOTA sont mesurés sur MOT17-04 avec sa **vérité terrain officielle**.
- HOTA et CIDEr-D sont réimplémentés dans le notebook ; leurs résultats ont été vérifiés **identiques** à ceux des bibliothèques de référence (TrackEval et pycocoevalcap) sur des données aléatoires (voir `validation/`).
- **Aucun FID expérimental** n'est rapporté : le notebook montre pourquoi une ou quelques images ne suffisent pas.
- Les courbes d'entraînement de la section 0 viennent d'un **vrai** entraînement exécuté dans le notebook ; aucune courbe n'est simulée.
- Les étiquettes de pertinence de la recherche image-texte sont attribuées à la main (`assets/recherche/collection.json`).
- Les traductions anglaises des prompts et requêtes sont **affichées** ; la légende anglaise de BLIP n'est **jamais traduite** avant d'être évaluée.

## 10. Données et licences

Voir `assets/SOURCES.md`. Usage **pédagogique et non commercial** : nuScenes (CC BY-NC-SA 4.0), MOT17 (CC BY-NC-SA 3.0), Flickr8k (usage académique), photo « coffee » (CC0), chiffres manuscrits de scikit-learn (licence BSD de la bibliothèque), facture fictive (libre de droits).
