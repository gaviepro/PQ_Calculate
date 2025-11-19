# PQ_Calculate

Ce projet permet de **retrouver automatiquement les deux nombres premiers `P` et `Q`** utilisés pour générer une clé RSA, **à partir du module `N` et de φ(N)** déjà connus (par exemple récupérés dans un TP, un CTF ou une mauvaise implémentation).

L’objectif est de montrer qu’**une fois `N` et φ(N) connus, la clé privée RSA est totalement compromise**, car on peut retrouver `P` et `Q` de manière purement algébrique.

---

## Principe général

On rappelle que pour RSA :

- `N = P × Q`
- `φ(N) = (P − 1) × (Q − 1) = N − (P + Q) + 1`

À partir de là, on peut calculer :

- `S = P + Q = N + 1 − φ(N)`

Les deux nombres `P` et `Q` sont alors les solutions de l’équation du second degré :

\[
X^2 - S X + N = 0
\]

Concrètement, l’algorithme fait :

1. Récupération de `N` et `φ(N)` (entiers sur de grandes tailles, typiquement 1024 bits et plus).
2. Calcul de `S = N + 1 − φ(N)`.
3. Calcul du **discriminant** :  
   `Δ = S² − 4N`.
4. Calcul de la racine carrée entière de Δ.
5. Détermination des deux racines :

   \[
   P = \frac{S - \sqrt{Δ}}{2}, \quad Q = \frac{S + \sqrt{Δ}}{2}
   \]

6. Vérifications :
   - `P × Q == N`
   - `P` et `Q` sont bien premiers (test de primalité basique ou avancé).

Si tout est cohérent, le programme affiche les valeurs de `P` et `Q`, qui peuvent ensuite être utilisées pour reconstruire la clé privée RSA.

---

## Intérêt pédagogique

Ce projet illustre plusieurs points vus en cours :

- **Fragilité de RSA si des valeurs internes comme φ(N) fuitent** (log, bug, mauvaise API…).
- Lien entre **maths (équation du second degré)** et **cryptanalyse pratique**.
- Importance de **protéger non seulement `d` et les facteurs, mais aussi φ(N)**.

Il montre qu’il n’y a pas besoin d’attaque “magique” : si `N` et φ(N) sont disponibles, le calcul de `P` et `Q` est **direct et déterministe**.

---

## Usage typique

Exemple d’utilisation en ligne de commande (à adapter selon votre script) :

```bash
python3 pq_calculate.py [-f <path_file> | (-N <valeur_de_N> -p <valeur_de_phiN>)]
```
-N : module RSA N (en décimal ou hexadécimal selon l’implémentation)

-p : valeur de φ(N) correspondante

-f : chemin du fichier contenant le nom de la clé, N et phi, le programme parse le fichier et récupere les valeurs utiles
