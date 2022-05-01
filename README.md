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

### debug levels:
1. Error
2. Warn
3. Info
4. Debug

### logging:
- default debugging is Error
- debugging level can be changed from config.json -> logger.level
- if `lg` is called with a value lower or equal than the config one,
the log is written
