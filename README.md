# Meta-récits de l'Italie contemporaine

Dans le cadre du cours *Lignuistique pour le TAL* (INALCO 2025).

## Carnet de recherche

### Construction d'un corpus

Dans un premier temps, nous avons collecté les communiqués de presse de la présidence du conseil italien. Notre idée était de trouver des descriptions de la vie politique du gouvernement révélatrice de récits politiques. Finalement, le contenu ne semblait pas assez marqué d'opinion. Nous avons donc décidé de collecter les communiqués de presse du parti Fratelli d'Italia, parti actuellement au pouvoir en Italie. Notre hypothèse est que la communication d'un parti verse plus dans l'opinion qu'une institution d'Etat – aussi politique qu'elle soit.

### Modélisation des récits

Les communiqués de presse du parti en poche, la prochaine étape consiste à construire un prompt de LLM assez efficace pour 1) identifier les récits dans un texte 2) identifier les éléments de chacun de ces récits.

**expérience**

Ecriture d'un petit script pour tester la méthode d'annotation des récits (éléments actantiels). Pour l'utiliser :

```bash
$ uv run extract.py <path texte> <path system prompt> <path reason prompt> <path extract prompt>
```
