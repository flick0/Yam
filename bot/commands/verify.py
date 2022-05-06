from __config import config
from bot import bot
from discord.ext import commands
import discord
import asyncio


class verify(commands.Cog):
    def __init__(self, bot):
        self.bot: bot.yam = bot

    @commands.Cog.listener()
    async def on_cog_load(self):
        print("running on_cog_load [verify]")
        channel = self.bot.get_channel(config.channel("verification"))
        if channel is None:
            print(channel)
            print("channel is none")
            return

        await channel.purge(limit=1)

        class check(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=180)

            @discord.ui.button(label="✔", custom_id="verify", style=discord.ButtonStyle.green)
            async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
                role = interaction.guild.get_role(config.role("verified"))
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"added role {role.mention}", ephemeral=True)

        msg = await channel.send(
            embed=await self.bot.embed(
                title="Verification",
                description=config.message("verification"),
            ),
            view=check()
        )
        while True:
            await asyncio.sleep(170)
            t = await msg.reply("```refreshing button```")
            print("refresh-")
            await msg.delete()
            msg = await channel.send(
                embed=await self.bot.embed(
                    title="Verification",
                    description=config.message("verification"),
                ),
                view=check()
            )
            await t.delete()


async def setup(bot):
    await bot.add_cog(verify(bot))
