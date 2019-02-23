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
from .table import Table
from .record import Record


class DataBase:
    # Discordのサーバーをラップするクラス
    def __init__(self, bot: commands.Bot, guild: discord.Guild):
        self.bot = bot
        self.guild = guild

    @classmethod
    def get(cls, bot: commands.Bot, guild: typing.Union[int, str, discord.Guild]) -> DataBase:
        if isinstance(guild, discord.Guild):
            pass
        elif isinstance(guild, int):
            # idによる指定
            guild = bot.get_guild(guild)
        elif isinstance(guild, str):
            # 名前による指定
            guild = next(g for g in bot.guilds if g.name == guild)
        else:
            raise TypeError
        return cls(bot, guild)

    def tables(self) -> typing.Generator[Table]:
        """Get the list of the Tables under this DataBase.

        Returns
        -------
        generator
            Generator to generate Table
        """
        return (Table.get(self.bot, self, c) for c in self.guild.channels if isinstance(c, discord.CategoryChannel))

    def get_table(self, *args) -> Table:
        """Get the Table of the specified category.

        Parameters
        ----------
        category : int, str, discord.CategoryChannel

        Returns
        -------
        table : Table
        """
        return Table.get(self.bot, self, *args)

    async def create_table(self, *args) -> Table:
        """Create a new Table under this DataBase

        Parameters
        ----------
        name : str
            Name of the new Table
        reason : str, default None
            The reason of making new Table

        Returns
        -------
        table : Table
        """
        return await Table.create(self.bot, self, *args)