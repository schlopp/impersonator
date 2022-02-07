import asyncio
import random
from typing import List, Dict, Tuple

import discord  # type: ignore
from discord.ext import commands, vbu  # type: ignore


ZERO_WIDTH_SPACE = "​"


class ImpersonationCommands(vbu.Cog):
    def __init__(self, bot: vbu.Bot):
        super().__init__(bot)
        self._webhook_cache: Dict[int, discord.Webhook] = {}
        self._convos: List[List[Tuple[int, str]]] = [
            [
                (0, "{}..."),
                (1, "What's up?"),
                (0, "I'm sorry I have to break it to you but..."),
                (0, "I had sexual intercourse with your mother."),
                (1, "Oh."),
            ],
            [
                (1, "I love sniffing farts so much bro"),
                (0, "SAME they smell so good!"),
                (0, "Glad we could agree {}"),
            ],
            [
                (0, "Who's my good little kitten."),
                (1, "{} I- I am."),
                (1, "\*shits agressively\*"),
                (0, "Mmmm. Tasty."),
            ],
            [
                (1, "I am so hungry"),
                (1, "Can I sprinkle some Doritos powder on your toes please?"),
                (0, "Sure bro!"),
                (1, "\*sucks on {} toes\*"),
                (0, "\*moans\*"),
            ],
        ]

    @commands.command(name="say")
    @commands.bot_has_permissions(
        send_messages=True, embed_links=True, manage_webhooks=True
    )
    @commands.guild_only()
    @commands.is_slash_command()
    async def _say_command(
        self, ctx: commands.SlashContext, user: discord.Member, *, message: str
    ):
        """
        Make a user say anything you want!
        """

        if not isinstance(ctx.channel, discord.TextChannel):
            return await ctx.interaction.response.send_message(
                "This command can only be used in text channels."
            )

        if ctx.channel.id in self._webhook_cache:
            webhook = self._webhook_cache[ctx.channel.id]
        else:
            for i in await ctx.channel.webhooks():
                if i.name == "impersonator":
                    webhook = i
                    break
            else:
                avatar = await ctx.guild.me.avatar.read()
                webhook = await ctx.channel.create_webhook(
                    name="impersonator",
                    avatar=avatar,
                    reason="This is used by the impersonator bot.",
                )
            self._webhook_cache[ctx.channel.id] = webhook

        await webhook.send(
            content=message,
            username=user.display_name,
            avatar_url=user.avatar.url if user.avatar else None,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=False, roles=False, replied_user=False
            ),
        )

        # Zero-width space, to make the emoji appear smaller
        await ctx.interaction.response.send_message(f":eyes:{ZERO_WIDTH_SPACE}")

    @commands.command(name="convo")
    @commands.bot_has_permissions(
        send_messages=True, embed_links=True, manage_webhooks=True
    )
    @commands.guild_only()
    async def _convo_command(
        self,
        ctx: commands.SlashContext,
        first_user: discord.Member,
        second_user: discord.Member,
    ):
        """
        Generate a fake convorsation between two users!
        """

        if not isinstance(ctx.channel, discord.TextChannel):
            return await ctx.interaction.response.send_message(
                "This command can only be used in text channels."
            )

        await ctx.interaction.response.defer()

        if ctx.channel.id in self._webhook_cache:
            webhook = self._webhook_cache[ctx.channel.id]
        else:
            for webhook in await ctx.channel.webhooks():
                if webhook.name == "impersonator":
                    webhook = webhook
                    break
            else:
                avatar = await ctx.guild.me.avatar.read()
                webhook = await ctx.channel.create_webhook(
                    name="impersonator",
                    avatar=avatar,
                    reason="This is used by the impersonator bot.",
                )
            self._webhook_cache[ctx.channel.id] = webhook

        convo = random.choice(self._convos)
        for convo_user_id, convo_message in convo:
            convo_user = first_user if not convo_user_id else second_user
            await webhook.send(
                content=convo_message.format(second_user.display_name),
                username=convo_user.display_name,
                avatar_url=convo_user.avatar.url if convo_user.avatar else None,
                allowed_mentions=discord.AllowedMentions.none(),
            )
            await asyncio.sleep(1)

        # Zero-width space, to make the emoji appear smaller
        await ctx.interaction.response.send_message(f":eyes:{ZERO_WIDTH_SPACE}")


def setup(bot: vbu.Bot):
    x = ImpersonationCommands(bot)
    bot.add_cog(x)
