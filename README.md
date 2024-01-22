# CLUlm

### Générer le CPU
Pour générer le cpu : ``make``.
Cela produira un fichier `cpulm.net` contenant la description du CPU.

### Option avancée
les commandes suivantes sont également disponibles : 

- `make clean` pour supprimer tous les fichiers temporaires
- `make test` : pour vérifier le comportement du CPU sur une batterie de tests
- `make chrono` pour tester la rapidité du CPU sur le test `chrono.ulm`

### Configuration
les commandes `make test`et `make chrono`ont besoin du simulateur C et de l'assembleur pour fonctionner. Il est donc conseillé de les utiliser dans l'environnement `meta`.
