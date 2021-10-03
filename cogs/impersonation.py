import asyncio
import random

import discord
from discord.ext import commands, vbu


ZERO_WIDTH_SPACE = "​"

class ImpersonationCommands(vbu.Cog):
    def __init__(self, bot, logger_name="ImpersonationCommands"):
        super().__init__(bot, logger_name=logger_name)
        self._webhook_cache = {}
        self._convos = [
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
        ]

    @commands.command(name="say")
    @commands.bot_has_permissions(
        send_messages=True, embed_links=True, manage_webhooks=True
    )
    @commands.guild_only()
    async def _say_command(
        self, ctx: commands.SlashContext, user: discord.Member, *, message: str
    ):
        """
        Make a user say anything you want!
        """

        if not isinstance(ctx, commands.SlashContext):
            return await ctx.send("Please use the slash command `/say`.")

        if not isinstance(ctx.channel, discord.TextChannel):
            return await ctx.interaction.response.send_message(
                "This command can only be used in text channels"
            )

        channel: discord.TextChannel = ctx.channel

        if channel.id in self._webhook_cache:
            webhook = self._webhook_cache[channel.id]
        else:
            for i in await channel.webhooks():
                if i.name == "impersonator":
                    webhook = i
                    break
            else:
                avatar = await ctx.guild.me.avatar.read()
                webhook: discord.Webhook = await channel.create_webhook(
                    name="impersonator",
                    avatar=avatar,
                    reason="This is used by the impersonator bot.",
                )
            self._webhook_cache[channel.id] = webhook

        await webhook.send(
            content=message,
            username=user.display_name,
            avatar_url=user.avatar.url,
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

        if not isinstance(ctx, commands.SlashContext):
            return await ctx.send("Please use the slash command `/convo`.")

        if not isinstance(ctx.channel, discord.TextChannel):
            return await ctx.interaction.response.send_message(
                "This command can only be used in text channels"
            )

        await ctx.interaction.response.defer()

        channel: discord.TextChannel = ctx.channel

        if channel.id in self._webhook_cache:
            webhook = self._webhook_cache[channel.id]
        else:
            for i in await channel.webhooks():
                if i.name == "impersonator":
                    webhook = i
                    break
            else:
                avatar = await ctx.guild.me.avatar.read()
                webhook: discord.Webhook = await channel.create_webhook(
                    name="impersonator",
                    avatar=avatar,
                    reason="This is used by the impersonator bot.",
                )
            self._webhook_cache[channel.id] = webhook

        convo = random.choice(self._convos)
        for i in convo:
            if i[0] == 0:
                await webhook.send(
                    content=i[1].format(second_user.display_name),
                    username=first_user.display_name,
                    avatar_url=first_user.avatar.url,
                    allowed_mentions=discord.AllowedMentions(
                        everyone=False, users=False, roles=False, replied_user=False
                    ),
                )
            else:
                await webhook.send(
                    content=i[1].format(first_user.display_name),
                    username=second_user.display_name,
                    avatar_url=second_user.avatar.url,
                    allowed_mentions=discord.AllowedMentions(
                        everyone=False, users=False, roles=False, replied_user=False
                    ),
                )
            await asyncio.sleep(1)

        await ctx.interaction.followup.send(":eyes:")


def setup(bot: vbu.Bot):
    x = ImpersonationCommands(bot)
    bot.add_cog(x)
