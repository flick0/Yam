from __config import config
from bot import bot
from discord.ext import commands
import discord


class verify(commands.Cog):
    def __init__(self, bot):
        self.bot: bot.yam = bot

    async def on_ready(self):
        print("got ready")
        channel = self.bot.get_channel(config.channel("verification"))
        print(channel)
        if channel is None:
            print(channel)
            print("channel is none")
            return
        await channel.purge(limit=100)

        class check(discord.ui.View):
            def __init__(self):
                super().__init__()

            @discord.ui.button(label="✔", custom_id="verify", style=discord.ButtonStyle.green)
            async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
                role = interaction.guild.get_role(config.role("verified"))
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"added role {role.mention}", ephemeral=True)

        await channel.send(
            embed=await self.bot.embed(
                title="Verification",
                description=config.message("verification"),
            ),
            view=check()
        )


async def setup(bot):
    tmp = verify(bot)
    await bot.add_cog(tmp)
    await tmp.on_ready()
