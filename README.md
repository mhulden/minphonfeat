# Distinctive Feature Minimization

This code implements a few search strategies discussed in the empirical section of the paper "The Computational Complexity of Distinctive Feature Minimization in Phonology" (Chen and Hulden, 2018) for finding the minimal set of distinctive features that captures some set of phonemes.

Usage:

```
python3 featuremin.py inventory.txt phonemelisting [-v]
```

For example:

```
python3 featuremin.py testinventory2.txt b,g
```

would find the minimal specification for the phoneme set {b,g} using two different strategies: (1) exhaustive search, which is guaranteed to find all the minimal solutions, and (2) greedy search, which returns a single solution (if one exists), which is not guaranteed to be minimal.

The feature inventory is a text file in a text-based self-explanatory format. Included are two inventories discussed in the paper, a simple toy inventory (`testinventory2.txt`) and an inventory for English following Hayes (2011) (`testinventory1.txt`)

The phonemes are given by listing them in the last argument.

# Cite

```
@InProceedings{chenhulden2018,
  author    = {Chen, Hubie and Hulden, Mans},
  title     = {The Computational Complexity of Distinctive Feature Minimization in Phonology},
  booktitle = {Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 2 (Short Papers)},
  year      = {2018},
  publisher = {Association for Computational Linguistics},
  pages     = {542--547},
  location  = {New Orleans, Louisiana},
  url       = {http://aclweb.org/anthology/N18-2086}
}
```
