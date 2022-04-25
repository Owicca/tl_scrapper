# A telegram scrapper

### prerequisites:
- docker
- make

### developer flow:
1. copy `config.json.example` to `config.json` and update with your settings
2. `make up`
3. import db from `/mysql_schema.sql`
4. `make run`
5. (inside container) `make uv`
6. access `localhost:9000/docs`
