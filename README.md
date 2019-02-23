# discord_db
Use discord server as databases

Example (with `bot: discord.ext.commands.Bot`):
```
import discord_db

h = discord_db.DiscordDBHandler(bot)
db = h.get_db(SERVER_ID)

try:
  table = db.get_table('pretty-good-table-name')
except TypeError:
  table = await h.create_table('pretty-good-table-name', reason="good table hasn't existed")

try:
  record = table.get_record('super-nice-record-name')
except TypeError:
  record = table.create_record('super-nice-record-name', reason="because it wasn't so nice")

# Show current value
print(await record.value())

# You can get discord object from each discord_db object
print([db.guild.name, table.category.name, record.channel])
print(await record.message())

# Renew the record (which sends a new message into the channel)
await record.insert("IT'S A FINE DAY")
```
