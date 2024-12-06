# griff

DDD library

## Créer une nouvelle version de la librairie

Increment `pyproject.toml` `version` number.

## Publier Griff sur PyPi

Pour cela, il faut créer une nouvelle release sur GitHub avec le tag correspondant à la version de la librairie c'est à dire la version renseignée dans `pyproject.toml`.

- Aller sur la page GitHub du repository : https://github.com/Wedge-Digital/griff
- Cliquer sur `Tags`
- Cliquer sur `Releases`
- Cliquer sur `Draft a new release`
- Dans `Choose a tag` saisir la version de la raison = version renseignée dans `pyproject.toml`
- Dans `Target` sélectionner la branche `v1` 
- Cliquer sur `Generate release notes`
- Cliquer sur `Publish release`

Le CI s'occupera ensuite de publier la librairie sur PyPi si les tests ne sont pas KO.

## Init Bdd
Initialise:
- la bdd à partir des migrations
- charge si nécessaire les **Db Templates** pour les tests.

```bash
griff common init_bdd
```

## Gestion des templates de Bdd (aka db_tpl)

### Créer ou mettre à jour un db_tpl

```bash
griff common db_tpl init <bounded context name>
```

### Restaurer un db_tpl en bdd

Permet de charger/recharger un db_tpl pour un bounded context. 

```bash
griff common db_tpl restore <bounded context name>
```

### Appliquer de nouvelles migrations sur les db_tpl

Cas d'usage : une ou plusieurs migrations ont été ajoutées. 

La commande suivante va mettre à jour les db_tpl avec les nouvelles migrations.
```bash
griff common db_tpl migrate
```

## Initialisation des migrations et queries d'un nouvel aggregat

Cela va créer :
- la migration de création de(s) table(s)
- la migration de(s) rollback(s)
- le fichier des queries

```bash
griff common agg2sql run <bounded context> <domain> <class aggregat>

# exemple pour le domaine user_account dans le bounded contexte Access
griff common agg2sql run access user_account UserAccount
```

