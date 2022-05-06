from discord.ext import commands
from __config import config


class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(config.channel("welcome"))
        if channel is None:
            return
        embed = await self.bot.embed(
            title=f"\n\nWelcome {member.name}",
        )
        embed.set_thumbnail(url=member.avatar.url)
        await channel.send(
            member.mention,
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(welcome(bot))
