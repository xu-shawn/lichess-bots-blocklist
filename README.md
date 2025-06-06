Block lichess bots running Stockfish

## Usage

> [!NOTE]
> These instructions are for bots running on the [lichess-bot][lichess-bot-url] framework.

In your config.yml, under `challenge`, create the following field

```yaml
  online_block_list:
    - https://raw.githubusercontent.com/xu-shawn/lichess-bots-blocklist/refs/heads/main/blocklist
```

Optionally, enable `include_challenge_block_list` under `matchmaking`

[lichess-bot-url]: https://github.com/lichess-bot-devs/lichess-bot
