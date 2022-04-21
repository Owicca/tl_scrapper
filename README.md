# A telegram scrapper

### prerequisites:
- docker
- make
- a compiled [tdlib](https://github.com/tdlib/td)

### developer flow:
1. copy `config.json.example` to `config.json` and update with your settings
2. `make up`
3. `make run`
4. (inside container) `make uv`
5. access `localhost:9000/docs`
