# Rapport de validation — version visuelle du notebook

Ce rapport distingue ce qui a été **exécuté**, ce qui a seulement été **vérifié par un test à blanc**, et ce qui **n'a pas pu être vérifié**.

## 1. Environnement de validation

| Élément | Valeur |
|---|---|
| Système | Linux (conteneur), **sans GPU** |
| Python | 3.13.18 |
| Bibliothèques | torch 2.15.0 · ultralytics 8.4.207 · open_clip_torch 4.2.1 · transformers 5.22.2 · diffusers 0.42.1 · motmetrics 1.4.0 · jiwer 4.0.0 · nltk 3.10.4 · scikit-learn 1.9.1 · ipywidgets 8.1.9 · numpy 2.5.3 · pandas 3.0.5 · scipy 1.18.1 |
| Programme externe | Tesseract 5.3.4 avec le modèle `fra` |
| Réseau | GitHub et PyPI accessibles ; **Hugging Face inaccessible** |

Conséquence : les poids de BLIP, de Stable Diffusion et du CLIP d'OpenAI n'ont pas pu être téléchargés. Le notebook a utilisé, comme prévu, son **modèle de repli** pour CLIP (OpenCLIP ViT-B/32, LAION-400M, poids sur GitHub) et n'a inventé aucune légende ni aucune image.

## 2. Exécutions réalisées

1. **Mode A, exécution complète** dans une copie neuve du projet (sans `modeles/` ni `resultats/`), avec `jupyter nbconvert --execute` : **63 cellules de code sur 63, 0 erreur, ≈ 40 s**, téléchargements compris. Résultat : `execution_mode_A.html`.
2. **Mode B, test à blanc** (`MODE = "B"`, `GENERER_IMAGE_SUR_CPU = True`) : une cellule ajoutée **uniquement pour ce test** remplaçait Stable Diffusion et BLIP par des modèles miniatures à poids aléatoires, pour vérifier que le code (états intermédiaires du débruitage, génération multi-graines, nuage de caractéristiques CLIP, légendage, BoT-SORT) s'exécute avec les versions actuelles des bibliothèques : **0 erreur**. Les sorties de ces modèles aléatoires n'ont aucune valeur et ne sont pas livrées.
3. **Sans ipywidgets** (module masqué) : **0 erreur** ; les contrôles interactifs sont remplacés par une vue fixe ou un message.
4. **Indépendance des sections** : préparation, puis section 5 et synthèse seulement : **0 erreur**.
5. **HOTA et CIDEr-D** : `verifier_hota_cider.py` compare les fonctions du notebook aux bibliothèques de référence. HOTA, DetA et AssA sont **identiques à TrackEval** (40 séquences aléatoires, écart < 10⁻⁹) ; CIDEr-D est **identique à pycocoevalcap** (15 images aléatoires).
6. **Contrôles des calculs** : CER et WER recoupés avec `jiwer` ; BLEU-1 recoupé avec NLTK ; MOTA recalculé à la main à partir de FN, FP et IDSW ; FID à une dimension (exemple de la diapositive 9) = 2,00.

## 3. Résultats mesurés (mode A, CPU)

| Section | Résultat réel |
|---|---|
| 0. Entraînement | petit réseau convolutif, 40 époques en ≈ 2 s ; meilleure validation à l'époque 35 ; **exactitude sur le test : 96,7 %** (360 images) |
| 1. Suivi | scène nuScenes : 28 identifiants ; MOT17-04 (8 images) : **MOTA 0,467 · IDF1 0,718 · HOTA 0,676** (DetA 0,533, AssA 0,896) ; à 640 px, MOTA chute |
| 2. Génération | pas de GPU : aucune image générée ; cosinus CLIP (repli) photo réelle / prompt anglais : 0,311 |
| 3. OCR | scan de la présentation : CER 1,0 %, WER 5,7 %, champs critiques exacts 100 % ; condition dégradée : CER 15,6 % (50 substitutions, 39 suppressions) |
| 4. Légendage | BLIP non exécuté (Hugging Face inaccessible). Phrases manuelles : CIDEr-D 0,44 (humaine retirée des références), 0,35 (phrase fausse), 0,19 (paraphrase fidèle) |
| 5. Recherche | CLIP de repli : rangs 3, 8, 1, 1 → Recall@3 = 75 %, MRR = 0,615 |

## 4. Bilan

| Élément | Exécuté réellement | Test à blanc | Non vérifié ici |
|---|---|---|---|
| Préparation, section 0, suivi, OCR, recherche | oui | — | Colab, Windows, GPU |
| Génération (Stable Diffusion) | principe, FID, CLIP | génération, étapes, nuage de caractéristiques | vrais poids de Stable Diffusion |
| Légendage (BLIP) | métriques sur phrases manuelles | appel de BLIP | vrais poids de BLIP |
| CLIP d'OpenAI | — | — | non téléchargeable ici (repli utilisé) |
| Contrôles interactifs | affichage initial, sans erreur | — | interaction réelle dans Jupyter ou Colab |

**À faire avant la soutenance** : exécuter le notebook une fois dans Colab, en mode A puis en mode B avec un GPU T4, pour confirmer BLIP, Stable Diffusion et le CLIP d'OpenAI.
