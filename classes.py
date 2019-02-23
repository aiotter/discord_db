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


class DiscordDBHandler:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_db(self, guild: typing.Union[int, str]):
        """Get DataBase object -- wrapper of discord.Guild.

        Parameters
        ----------
        guild : int, str, discord.Guild
            id or name of the guild to wrap

        Returns
        -------
        database : DataBase
        """
        return DataBase.get(self.bot, guild)

    def get_table(self, category_id: int):
        """Get Table object -- wrapper of discord.CategoryChannel.

        Parameters
        ----------
        category_id : int
            id of the category to wrap

        Returns
        -------
        table : Table
        """
        category = self.bot.get_channel(category_id)
        assert isinstance(category, discord.CategoryChannel)
        return Table(self.bot, category)

    def get_record(self, channel_id: int):
        """Get Record object -- wrapper of discord.TextChannel.

        Parameters
        ----------
        channel_id : int
            id of the channel to wrap

        Returns
        -------
        record : Record
        """
        channel = self.bot.get_channel(channel_id)
        assert isinstance(channel, discord.TextChannel)
        return Record(self.bot, channel)


class DataBase:
    # Discordのサーバーをラップするクラス
    def __init__(self, bot: commands.Bot, guild: discord.Guild):
        self.bot = bot
        self.guild = guild

    def __getattr__(self, item):
        return getattr(self.guild, item)

    @classmethod
    def get(cls, bot: commands.Bot, guild: typing.Union[int, str, discord.Guild]):
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

    def tables(self):
        """Get the list of the Tables under this DataBase.

        Returns
        -------
        generator
            Generator to generate Table
        """
        return (Table.get(self.bot, self, c) for c in self.guild.channels if isinstance(c, discord.CategoryChannel))

    def get_table(self, *args):
        """Get the Table of the specified category.

        Parameters
        ----------
        category : int, str, discord.CategoryChannel

        Returns
        -------
        table : Table
        """
        return Table.get(self.bot, self, *args)

    async def create_table(self, *args):
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


class Table:
    # Discordのカテゴリチャンネルをラップするクラス
    def __init__(self, bot: commands.Bot, category: discord.CategoryChannel):
        self.bot = bot
        self.category = category
        self.db = DataBase.get(bot, category.guild)

    def __getattr__(self, item):
        return getattr(self.db, item)

    @classmethod
    def get(cls, bot: commands.Bot, db: DataBase, category: typing.Union[int, str, discord.CategoryChannel]):
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
    async def create(cls, bot: commands.Bot, db: DataBase, name: str, reason: str = None):
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

    def get_record(self, *args):
        """Get the Record of the specified channel.

        Parameters
        ----------
        channel : int, str, discord.CategoryChannel

        Returns
        -------
        record : Record
        """
        return Record.get(self.bot, self, *args)

    async def create_record(self, *args):
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

    async def insert(self, *args):
        """alias to `create_record()`"""
        return await self.create_record(*args)


class Record:
    # Discordのテキストチャンネルをラップするクラス
    def __init__(self, bot: commands.Bot, channel: discord.TextChannel):
        self.bot = bot
        self.channel = channel
        self.table = Table.get(bot, DataBase.get(bot, channel.guild), channel.category)

    def __getattr__(self, item):
        return getattr(self.channel, item)

    @classmethod
    def get(cls, bot: commands.Bot, table: Table, channel: typing.Union[int, str, discord.TextChannel]):
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
    async def create(cls, bot: commands.Bot, table: Table, name: str, reason: str = None):
        channel = await table.category.guild.create_text_channel(name, category=table.category, reason=reason)
        return cls(bot, channel)

    async def message(self):
        async for message in self.channel.history(limit=1):
            return message

    async def value(self):
        return (await self.message()).content

    async def insert(self, content: str):
        return await self.channel.send(content)
