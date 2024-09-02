## Project details

| key               | value                     | 
|-------------------|---------------------------|
| URL prod          | http://13.84.205.162/8011 | 
| URL test          | http://13.84.205.162/8011 | 
| Test user         | frpk21 / ZgZyWJbaKv       |
| Requirements path | requirements.txt          |
| Settings path     | smt/settings.py           |
| Python version    | 3.7.7                     |

## DB

dump db

```bash
docker compose exec postgres pg_dump -U onic-user -F c -d onic -f /tmp/onic_dump

docker compose cp postgres:/tmp/onic_dump /tmp/
```

download dump from server

```bash
scp smt@164.92.104.179:/tmp/onic_dump /tmp/
```

```bash
```