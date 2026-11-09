"""Vérifie que HOTA et CIDEr-D, réimplémentés dans le notebook, donnent exactement les résultats des bibliothèques de référence.

Usage (depuis la racine du projet) :
    pip install pycocoevalcap "git+https://github.com/JonathonLuiten/TrackEval.git"
    python validation/verifier_hota_cider.py
"""
import json
from collections import Counter

import numpy as np
from scipy.optimize import linear_sum_assignment

cellules = ["".join(c["source"]) for c in json.load(open("Demonstration_IA_Notebook_Visuel.ipynb", encoding="utf-8"))["cells"]
            if c["cell_type"] == "code"]
exec([c for c in cellules if c.startswith("def hota")][0].split("\n\nh = hota(")[0])
exec([c for c in cellules if c.startswith("def ngrammes")][0].split("\n\ncollection_legendes")[0])

np.float, np.int, np.bool = float, int, bool  # TrackEval utilise des alias retirés de NumPy 2
from trackeval.metrics import HOTA  # noqa: E402
from pycocoevalcap.cider.cider import Cider  # noqa: E402

rng = np.random.default_rng(0)
n_seq = 0
for _ in range(40):
    T, ng, nt = rng.integers(3, 12), rng.integers(2, 8), rng.integers(2, 9)
    donnees, data = [], {"gt_ids": [], "tracker_ids": [], "similarity_scores": []}
    for _t in range(T):
        g = rng.choice(ng, rng.integers(0, ng + 1), replace=False)
        p = rng.choice(nt, rng.integers(0, nt + 1), replace=False)
        sim = rng.uniform(0, 1, (len(g), len(p))) * (rng.uniform(0, 1, (len(g), len(p))) < 0.5)
        donnees.append((g + 100, p + 500, sim))
        data["gt_ids"].append(g); data["tracker_ids"].append(p); data["similarity_scores"].append(sim)
    ug = sorted({x for g in data["gt_ids"] for x in g}); ut = sorted({x for p in data["tracker_ids"] for x in p})
    data["gt_ids"] = [np.array([ug.index(x) for x in g], dtype=int) for g in data["gt_ids"]]
    data["tracker_ids"] = [np.array([ut.index(x) for x in p], dtype=int) for p in data["tracker_ids"]]
    data.update(num_gt_ids=len(ug), num_tracker_ids=len(ut), num_gt_dets=sum(map(len, data["gt_ids"])),
                num_tracker_dets=sum(map(len, data["tracker_ids"])))
    if not data["num_gt_dets"] or not data["num_tracker_dets"]:
        continue
    ref, mien = HOTA().eval_sequence(data), hota(donnees)
    for cle in ("HOTA", "DetA", "AssA"):
        assert abs(mien[cle] - ref[cle].mean()) < 1e-9, (cle, mien[cle], ref[cle].mean())
    n_seq += 1
print(f"HOTA, DetA, AssA : identiques à TrackEval sur {n_seq} séquences aléatoires")

mots = "a man woman dog cat street rain red blue train metro platform people wait the on in with".split()
gts, res, corpus = {}, {}, []
for i in range(15):
    refs = [" ".join(rng.choice(mots, rng.integers(4, 12))) for _ in range(5)]
    gts[i], res[i] = refs, [" ".join(rng.choice(mots, rng.integers(3, 12)))]
    corpus.append([r.split() for r in refs])
_, scores_coco = Cider().compute_score(gts, res)
c = CIDErD(corpus)
miens = [c.score(res[i][0].split(), [r.split() for r in gts[i]]) for i in range(15)]
assert np.allclose(miens, scores_coco, atol=1e-9)
print("CIDEr-D : identique à pycocoevalcap sur 15 images aléatoires")
