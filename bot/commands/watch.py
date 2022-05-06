from discord.ext import commands
import time
import asyncio
import random
import discord


class watch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if isinstance(msg.channel, discord.channel.DMChannel):
            self.bot.dispatch("dm", msg)

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, msg):
        if msg.author.bot:
            return
        await self.bot.process_edit(message_before, msg)


async def setup(bot):
    await bot.add_cog(watch(bot))
