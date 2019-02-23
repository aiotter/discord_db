"""
The MIT License (MIT)
Copyright (c) 2019 Azuki
Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import discord
from discord.ext import commands
import typing
from .database import DataBase
from .table import Table


class Record:
    # Discordのテキストチャンネルをラップするクラス
    def __init__(self, bot: commands.Bot, channel: discord.TextChannel):
        self.bot = bot
        self.channel = channel
        self.table = Table.get(bot, DataBase.get(bot, channel.guild), channel.category)

    @classmethod
    def get(cls, bot: commands.Bot, table: Table, channel: typing.Union[int, str, discord.TextChannel]) -> Record:
        if isinstance(channel, int):
            # idによる指定
            channel = bot.get_channel(channel)
        elif isinstance(channel, str):
            # 名前による指定
            channel = next(
                c for c in table.category.channels if c.name == channel and isinstance(c, discord.TextChannel))
        else:
            record.channel = None

        # record.categoryがテキストチャンネルであることを確認
        if not isinstance(channel, discord.TextChannel):
            raise TypeError
        return cls(bot, channel)

    @classmethod
    async def create(cls, bot: commands.Bot, table: Table, name: str, reason: str = None) -> Record:
        channel = await table.category.create_text_channel(name, reason=reason)
        return cls(bot, channel)

    async def message(self):
        async for message in self.channel.history(limit=1):
            return message

    async def value(self):
        return (await self.message()).content

    async def insert(self, content: str) -> discord.Message:
        return await self.channel.send(content)