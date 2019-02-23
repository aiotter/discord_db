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
from .record import Record


class DiscordDBHandler:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_db(self, guild: typing.Union[int, str]) -> DataBase:
        """Get DataBase object -- wrapper of discord.Guild.

        Parameters
        ----------
        guild : int, str, discord.Guild
            id or name of the guild to wrap
        """
        return DataBase.get(self.bot, guild)

    def get_table(self, category_id: int) -> Table:
        """Get Table object -- wrapper of discord.CategoryChannel.

        Parameters
        ----------
        category_id : int
            id of the category to wrap
        """
        category = self.bot.get_channel(category_id)
        assert isinstance(category, discord.CategoryChannel)
        return Table(self.bot, category)

    def get_record(self, channel_id: int) -> Record:
        """Get Record object -- wrapper of discord.TextChannel.

        Parameters
        ----------
        channel_id : int
            id of the channel to wrap
        """
        channel = self.bot.get_channel(channel_id)
        assert isinstance(channel, discord.TextChannel)
        return Record(self.bot, channel)
