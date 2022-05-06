from discord.ext import commands
from __config import config
import discord
import logger
import json


def get_json():
    with open("./db/support.json", "r") as f:
        return json.load(f)


def update_json(data):
    with open("./db/support.json", "w") as f:
        json.dump(data, f)


class support(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.guild = self.bot.get_guild(config.guild("YAM_SMP"))
        categories = self.guild.by_category()
        for _category in categories:
            if _category[0].id == config.category("ticket"):
                self.category = _category[0]
                break

    @commands.Cog.listener()
    async def on_dm(self, msg):
        logger.log("got on_dm event")
        channel = discord.utils.get(
            self.guild.channels,
            name=f"{msg.author.name}{msg.author.discriminator}"
        ) or (
            await self.guild.create_text_channel(
                f"{msg.author.name}{msg.author.discriminator}",
                category=self.category,
                topic=str(msg.author.id)
            )
        )
        files = []
        for attachment in msg.attachments:
            files.append(await attachment.to_file(use_cached=True, spoiler=attachment.is_spoiler()))
        await channel.send(msg.content, files=files)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if msg.guild is None:
            return
        if msg.channel.category != self.category:
            return
        ids = [int(i) for i in msg.channel.topic.split()]
        for _id in ids:
            user = self.guild.get_member(_id)
            files = []
            for attachment in msg.attachments:
                files.append(await attachment.to_file(use_cached=True, spoiler=attachment.is_spoiler()))
            print(files)
            await user.send(msg.content or None, files=files)


async def setup(bot):
    await bot.add_cog(support(bot))
