# git-mining

Het extraheren van bruikbare data uit een git repository

## Aanpak

Om snel commit history en metadata uit een git repository te halen, kan gebruik worden gemaakt van `git log`. Dit output text in de vorm:

```txt
commit 886cfe82d043c69f8bcdaee32b0b274fa1727ec7
Author: JiaLiPassion <JiaLi.Passion@gmail.com>
Date:   Sat Mar 5 21:06:03 2022 +0900

    ci: components CI test should use local zone.js build (#45277)
    
    CI components test install the angular package from the local
    version, but still use the zone.js from npm, so this commit let
    components also install zone.js from local too.
    
    PR Close #45277

```

(Voorbeeld uit [angular/angular](https://github.com/angular/angular))

`git log` heeft meerdere opties:

output `git log -h` (git version 2.32.0 (Apple Git-132)):

```txt
usage: git log [<options>] [<revision-range>] [[--] <path>...]
   or: git show [<options>] <object>...

    -q, --quiet           suppress diff output
    --source              show source
    --use-mailmap         use mail map file
    --mailmap             alias of --use-mailmap
    --decorate-refs <pattern>
                          only decorate refs that match <pattern>
    --decorate-refs-exclude <pattern>
                          do not decorate refs that match <pattern>
    --decorate[=...]      decorate options
    -L <range:file>       trace the evolution of line range <start>,<end> or function :<funcname> in <file>
```

Gebruik van `git log` en `git log -q` lijkt geen verschil te maken in grootte van output:

```zsh
9275463 angular.log.quiet.txt
9275463 angular.log.txt
```

(Truncated output of `ls -al` with size in bytes)

Om dit bruikbaar te maken, pipe ik de uitvoer van `git log` naar een bestand met: `git log > log.txt`.

## Bestaande tools

Met de bovenstaande voorkennis is het makkelijk gericht te zoeken naar bestaande oplossingen:

* [Python](https://github.com/gaborantal/git-log-parser)
* [Javascript](https://www.npmjs.com/package/git-log-parser)
* [Shell/ NuShell](https://www.nushell.sh/cookbook/parsing_git_log.html)

Al deze tools doen grofweg hetzelfde: de output van `git log` parsen naar een vorm van object notatie.

### Python

De eerste tool is interessant, omdat python veel gebruikt wordt in de ML wereld, en dit dus mogelijk ook uitgevoerd zou kunnen worden op google colab.

Om de tool te installeren gebruik je `pip install -r requirements.txt` (of `pip3` als je zowel python 2 als 3 hebt).

De python tool voert onder water `git log` uit, waarna de uitvoer omgezet wordt in json formaat:

```json
[
    {
        "author": {
            "email": "JiaLi.Passion@gmail.com",
            "name": "JiaLiPassion"
        },
        "change_id": null,
        "commit_date": "2022-03-05 21:06:03+09:00",
        "commit_hash": "886cfe82d043c69f8bcdaee32b0b274fa1727ec7",
        "deletions": 0,
        "files_changed": 0,
        "insertions": 0,
        "isMerge": false,
        "message": "ci: components CI test should use local zone.js build (#45277)\nCI components test install the angular package from the local\nversion, but still use the zone.js from npm, so this commit let\ncomponents also install zone.js from local too.\nPR Close #45277"
    },
]

```

(JSON uitvoer van [Python tool](https://github.com/gaborantal/git-log-parser) van eerder genoemd voorbeeld uit [angular/angular](https://github.com/angular/angular))

