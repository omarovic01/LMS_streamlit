# ZEY LMS - Assistant de Création de Contenu Pédagogique

Une application Streamlit pour créer et gérer du contenu pédagogique avec l'aide de l'IA.

## Fonctionnalités

L'application comprend 5 onglets principaux :

1. **Infos cours** : Définir les informations générales sur le cours (titre, description, catégorie, durée, difficulté, etc.)
2. **Prérequis** : Spécifier les objectifs d'apprentissage, prérequis et méthodes d'enseignement
3. **Générer un cours** : Utiliser l'IA pour créer une structure hiérarchique de modules et chapitres avec contenu détaillé
4. **Générer un quizz** : Créer des évaluations interactives basées sur le contenu des modules
5. **Générer un podcast** : Transformer le contenu du cours en format audio avec synthèse vocale

### Fonctionnalités d'IA

- **Amélioration de description** : Transforme une description basique en description professionnelle et engageante
- **Génération de structure de cours** : Crée une structure hiérarchique de modules et chapitres adaptée au sujet
- **Génération de contenu détaillé** : Produit un contenu pédagogique complet pour chaque chapitre
- **Génération de quiz** : Crée des questions pertinentes basées sur le contenu des modules
- **Génération de podcast** : Produit un script de podcast et le convertit en audio avec différentes voix

## Installation

1. Clonez ce dépôt :
```
git clone <url-du-repo>
cd zey_LMS
```

2. Installez les dépendances :
```
pip install -r requirements.txt
```

## Configuration des clés API

L'application utilise l'API OpenAI pour toutes les fonctionnalités d'IA. Vous pouvez configurer votre clé API de deux façons :

### Option 1 : Variables d'environnement

Créez un fichier `.env` à la racine du projet avec le contenu suivant :

```
OPENAI_API_KEY=votre_clé_api_openai
ANTHROPIC_API_KEY=votre_clé_api_anthropic (optionnel)
```

### Option 2 : Interface utilisateur

Vous pouvez également saisir vos clés API directement dans l'interface utilisateur de l'application, dans la barre latérale.

## Utilisation

1. Lancez l'application :
```
streamlit run App.py
```

2. Accédez à l'application dans votre navigateur à l'adresse indiquée (généralement http://localhost:8501)

3. Workflow recommandé :
   - Commencez par remplir les informations du cours dans l'onglet "Infos cours"
   - Définissez les objectifs d'apprentissage, prérequis et méthodes dans l'onglet "Prérequis"
   - Générez la structure du cours dans l'onglet "Générer un cours"
   - Générez le contenu détaillé pour chaque chapitre
   - Créez des quiz basés sur les modules dans l'onglet "Générer un quizz"
   - Créez un podcast éducatif dans l'onglet "Générer un podcast"

## Fonctionnalités détaillées

### Génération de structure de cours
- Crée une structure hiérarchique de modules et chapitres
- Adapte le contenu au niveau de difficulté spécifié
- Prend en compte les documents de référence uploadés

### Génération de contenu détaillé
- Produit une introduction, des sections de contenu, des exemples et une conclusion
- Inclut des exercices pratiques pour renforcer l'apprentissage
- Adapte le contenu au niveau de difficulté du cours

### Génération de quiz
- Crée des questions à choix multiple, vrai/faux ou questions directes
- Adapte les questions au niveau de difficulté spécifié
- Fournit des explications pour chaque réponse

### Génération de podcast
- Crée un script de podcast basé sur le contenu du cours
- Supporte différents formats (Interview, Monologue, Discussion, Débat)
- Convertit le script en audio avec différentes voix

## Prérequis

- Python 3.8 ou supérieur
- Connexion Internet (pour les appels API)
- Clé API pour OpenAI

## Licence

© 2023 ZEY LMS - Tous droits réservés 