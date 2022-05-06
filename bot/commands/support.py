from discord.ext import commands
from __config import config
import discord
import logger
from db._motor import mongo


class support(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_dm(self, msg):
        logger.log("got on_dm event")
        guild = self.bot.get_guild(config.guild("YAM_SMP"))
        categories = guild.by_category()
        for _category in categories:
            if _category[0].id == config.category("ticket"):
                category = _category[0]
                break
        channel = discord.utils.get(
            guild.channels, name=f"{msg.author.name}{msg.author.discriminator}"
        ) or (
            await guild.create_text_channel(
                f"{msg.author.name}{msg.author.discriminator}", category=category)
        )
        await channel.send(msg.content)


async def setup(bot):
    await bot.add_cog(support(bot))
