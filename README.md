# discord_db
Use discord server as databases

Example (with `bot: discord.ext.commands.Bot`):
```
import discord_db

h = discord_db.DiscordDatabaseHandler(bot)
db = h.get_db(SERVER_ID)
table = db.get_table(CATEGORY_CHANNEL_ID)
record = table.get_record(TEXT_CHANNEL_ID)

print(await record.value())
```
