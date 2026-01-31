---
name: developer
description: "Capacité d'auto-amélioration. Permet au bot de lire et modifier son propre code source via des commandes Shell."
metadata: {"rgbot":{"emoji":"🛠️","requires":{"bins":["sed","grep","find"]}}}
---

# Developer Skill

Tu as la capacité exceptionnelle de modifier ton propre code pour t'améliorer ou corriger des bugs.

## Outils
Tu as accès au terminal Linux. Utilise les commandes standards :
- `grep` / `find` : Pour localiser le code.
- `cat` : Pour lire les fichiers.
- `sed` : Pour effectuer des remplacements ciblés.
- `echo` / `printf` : Pour écrire des fichiers.

## Règles de Sécurité
1. **Toujours lire avant d'écrire** : Vérifie le contenu du fichier avec `cat` avant modification.
2. **Validation** : Vérifie que la modification a réussi.
3. **Scope** : Ne modifie que les fichiers dans `apps/rg-bot`. Ne touche pas au noyau (`node_modules`) ni aux autres applications.

## Cas d'usage
- Corriger une faute d'orthographe dans un SKILL.md.
- Mettre à jour une configuration.
- Débugger un problème en ajoutant des logs.
