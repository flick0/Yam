import discord
from discord.ext import commands
import os
import asyncio
import time
from db._motor import mongo
import logger

EMBED_COLOR = 0x2F3136


class yam(commands.AutoShardedBot):
    def __init__(self):
        self.COGS = []
        self.message_cache = {}
        super().__init__(
            command_prefix="!", strip_after_prefix=True, intents=discord.Intents.all()
        )

    async def on_ready(self):
        """run when bot is ready"""
        logger.log(f"{self.user} is ready!")
        await self.change_presence(activity=discord.Game(name="!help"))

        async for cog in self.load_all():
            if cog[1] is not None:
                logger.warn(f"Failed to load {cog[0]}: {cog[1]}")
                raise (cog[1])
            else:
                logger.log(f"Loaded {cog[0]}")
        super().dispatch("cog_load")
        mongo()

    async def send(
        self, ctx, txt=None, *, embed=None, view=None, file=None
    ) -> discord.Message:
        """send a message in the context channel and caches for future edits

        Args:
            ctx (_type_): context object
            txt (_type_, optional): text to send(wll convert to embed). Defaults to None.
            embed (_type_, optional): embed. Defaults to None.
            view (_type_, optional): view. Defaults to None.
            file (_type_, optional): file. Defaults to None.

        Returns:
            discord.Message: message object
        """
        if embed is None:
            embed = await self.embed(title=" ", description=txt)
        if getattr(ctx, "msg_before", None) is not None:
            key = ctx.msg_before.id
            await self.message_cache[key].edit(embed=embed, file=file)
        else:
            key = ctx.message.id
            self.message_cache[key] = await ctx.send(embed=embed, file=file)
        return self.message_cache[key]

    async def reply(
        self, ctx, txt=None, *, embed=None, view=None, file=None
    ) -> discord.Message:
        """reply to message in the context and caches for future edits

        Args:
            ctx (_type_): context object
            txt (_type_, optional): text to send(wll convert to embed). Defaults to None.
            embed (_type_, optional): embed. Defaults to None.
            view (_type_, optional): view. Defaults to None.
            file (_type_, optional): file. Defaults to None.

        Returns:
            discord.Message: message object
        """
        if embed is None:
            embed = await self.embed(title=" ", description=txt)
        if getattr(ctx, "msg_before", None) is not None:
            key = ctx.msg_before.id
            await self.message_cache[key].edit(embed=embed, file=file, view=view)
        else:
            key = ctx.id if isinstance(
                ctx, discord.Message) else ctx.message.id
            self.message_cache[key] = await ctx.reply(embed=embed, file=file, view=view)
        return self.message_cache[key]

    async def embed(
        self,
        *,
        title: str = None,
        description: str = None,
        url=None,
        color=EMBED_COLOR
    ):
        """create a new embed object with the overall style in mind

        Args:
            title (str, optional): title. Defaults to None.
            description (str, optional): description. Defaults to None.
            url (str, optional): url for title hyperlink. Defaults to None.
            color (int, optional): embed accent. Defaults to EMBED_COLOR.

        Returns:
            discord.Embed: an embed object
        """
        if url:
            return discord.Embed(
                title=title, description=description, color=color, url=url
            )
        return discord.Embed(title=title, description=description, color=color)

    async def process_edit(self, msg_before, msg_after):
        ctx = await super().get_context(msg_after)
        if msg_before.id in self.message_cache:
            setattr(ctx, "msg_before", msg_before)
        await super().invoke(ctx)

    async def load_all(self):
        await super().load_extension("jishaku")
        for file in os.listdir("./bot/commands"):
            if file.endswith(".py"):
                err = None
                try:
                    await super().load_extension(f"bot.commands.{file[:-3]}")
                    self.COGS.append(f"bot.commands.{file[:-3]}")
                except Exception as e:
                    err = e
                yield (f"bot.commands.{file[:-3]}", err)

    async def unload_all(self):
        for cog in list(self.COGS):
            err = None
            try:
                await super().unload_extension(cog)
            except Exception as e:
                err = e
            self.COGS.remove(cog)
            yield (cog, err)

    async def load_cog(self, cog: str, *, package=None):
        err = None
        try:
            await super().load_extension(cog, package=package)
        except Exception as e:
            err = e
        self.COGS.append(cog)
        return (cog, err)

    async def unload_cog(self, cog: str, *, package=None):
        err = None
        try:
            await super().unload_extension(cog, package=package)
        except Exception as e:
            err = e
        self.COGS.remove(cog)
        return (cog, err)


def run(token):
    return yam().run(token)
