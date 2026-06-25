# D'un domaine à l'autre : toujours la même structure

*(Document d'accompagnement — rien à coder ici, c'est une aide pour
comprendre.)*

## L'idée

Le cœur de la programmation orientée objet, c'est de **séparer la
structure du décor**. Une bonne architecture de classes se réutilise d'un
sujet à l'autre : on change les noms et le domaine, mais l'ossature reste
la même.

Vous avez **déjà rencontré cette ossature**. En cours, avec la
**bibliothèque** (les livres). Et si vous avez passé l'épreuve précédente,
avec la **flotte de véhicules**. Cette nouvelle épreuve — la **centrale de
réservation** — est bâtie sur **exactement le même plan**. Si vous repérez
ce plan, vous savez déjà, en grande partie, quoi faire.

## Le tableau des correspondances

| Rôle dans la structure | Bibliothèque (cours) | Flotte (épreuve précédente) | Centrale (ici) |
|---|---|---|---|
| **Entité** identifiée par un code | `Livre` — *ISBN* | `Vehicule` — *châssis* | `Hebergement` — *code de réservation* |
| **Sous-classe qui ENRICHIT** la fiche | `LivreNumerique` *(+ format)* | `VoitureElectrique` *(+ autonomie)* | `Gite` *(+ nombre de chambres)* |
| **Sous-classe qui REMPLACE** la fiche | `LivreAudio` *(+ durée)* | `Camion` *(+ charge utile)* | `EmplacementCamping` *(+ surface)* |
| **Objet-valeur** (comparé par sa valeur) | `Argent` | `Tarif` | `TarifNuitee` |
| **Conteneur** (regroupe, `len` / `in` / `for`) | `Bibliotheque` | `Flotte` | `CentraleReservation` |
| **État** qui évolue dans le temps | disponible / emprunté | disponible / loué | libre / réservé |
| **Persistance** (enregistrer + relire en JSON) | catalogue | persistance | persistance |

Lisez ce tableau **colonne par colonne** : chaque domaine raconte la même
histoire avec d'autres mots. Puis lisez-le **ligne par ligne** : c'est la
liste des rôles qui reviennent à chaque fois.

## Ce qui ne change jamais (les six rôles)

1. **Une entité avec une identité.** Un livre est identifié par son ISBN,
   un véhicule par son châssis, un hébergement par son code de
   réservation. Deux objets de même code sont « le même » : l'égalité se
   fonde sur ce code, pas sur le reste. Le code est vérifié par une petite
   méthode dédiée (`isbn_valide`, `chassis_valide`, `code_valide`).

2. **Une sous-classe qui enrichit.** Elle *est* une entité de base, à
   laquelle on **ajoute** une information. Sa fiche **reprend** la fiche de
   base et la complète : on réutilise le travail du parent avec `super()`.
   (Le livre numérique, la voiture électrique, le gîte.)

3. **Une sous-classe qui remplace.** Elle ajoute aussi une information,
   mais cette fois la mesure de base **n'a plus de sens** : sa fiche est
   **entièrement différente**, elle ne réutilise pas celle du parent. (Le
   livre audio se mesure en durée, le camion en charge, l'emplacement en
   surface.)

   > Savoir **quand enrichir et quand remplacer** est l'un des points les
   > plus intéressants de l'exercice — et une bonne question d'oral.

4. **Un objet-valeur.** Un montant (avec sa devise) ne se compare pas par
   identité mais par **valeur** : deux montants égaux sont égaux. Il peut
   se comparer et s'additionner. (`Argent`, `Tarif`, `TarifNuitee`.)

5. **Un conteneur.** Il regroupe les entités et se manipule avec les
   outils naturels de Python (`len(...)`, `x in ...`, `for ... in ...`),
   **sans jamais tester le type** des objets qu'il contient.

6. **La persistance polymorphe.** On enregistre tout en JSON, et à la
   relecture **chaque objet retrouve son type exact**, grâce à un champ
   `"type"` et à un **registre** qui associe ce nom à la bonne classe.

## Comment vous en servir

Quand vous découvrez un nouveau sujet, ne vous laissez pas impressionner
par le vocabulaire (gîtes, nuitées, emplacements…). Posez-vous plutôt :

- *Qui est l'entité, et quel est son code d'identité ?*
- *Quelle sous-classe enrichit, laquelle remplace ?*
- *Où est l'objet-valeur ? Le conteneur ? L'état qui change ?*
- *Comment se fait l'aller-retour vers le fichier ?*

Une fois ces rôles repérés, vous retrouvez un terrain connu : vous avez
déjà écrit ce genre de code deux fois.

## Le lien avec l'évaluation

Reconnaître cette structure sous un domaine inhabituel, et **expliquer**
vos choix (« ici j'enrichis parce que la capacité reste pertinente ; là je
remplace parce que la surface n'a rien à voir avec un nombre de
personnes »), c'est précisément ce que vérifie l'**AA3 — justifier ses
choix**. Ce document n'est pas un raccourci : c'est la grille de lecture
que l'on attend de vous à la fin du cours.

Bon travail !
