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
from .record import Record


class Table:
    # Discordのカテゴリチャンネルをラップするクラス
    def __init__(self, bot: commands.Bot, category: discord.CategoryChannel):
        self.bot = bot
        self.category = category
        self.db = DataBase.get(bot, category.guild)

    @classmethod
    def get(cls, bot: commands.Bot, db: DataBase, category: typing.Union[int, str, discord.CategoryChannel]) -> Table:
        if isinstance(category, int):
            # idによる指定
            category = bot.get_channel(category)
        elif isinstance(category, str):
            # 名前による指定
            category = next(
                c for c in db.guild.channels if c.name == category and isinstance(c, discord.CategoryChannel))

        # categoryがカテゴリチャンネルであることを確認
        if not isinstance(category, discord.CategoryChannel):
            raise TypeError
        return cls(bot, category)

    @classmethod
    async def create(cls, bot: commands.Bot, db: DataBase, name: str, reason: str = None) -> Table:
        category = await db.guild.create_category_channel(name, reason=reason)
        return cls(bot, category)

    def records(self):
        """Get the list of the Records under this DataBase.

        Returns
        -------
        generator
            Generator to generate Record
        """
        return (Record.get(self.bot, self, c) for c in self.category.channels if isinstance(c, discord.TextChannel))

    def get_record(self, *args) -> Record:
        """Get the Record of the specified channel.

        Parameters
        ----------
        channel : int, str, discord.CategoryChannel

        Returns
        -------
        record : Record
        """
        return Record.get(self.bot, self, *args)

    async def create_record(self, *args) -> Record:
        """Create a new Record under this Table

        Parameters
        ----------
        name : str
            Name of the new Record
        reason : str, default None
            The reason of making new Record

        Returns
        -------
        record : Record
        """
        return await Record.create(self.bot, self, *args)