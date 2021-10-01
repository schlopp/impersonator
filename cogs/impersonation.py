import discord
from discord.ext import commands, vbu


class ImpersonationCommands(vbu.Cog):
    def __init__(self, bot, logger_name="ImpersonationCommands"):
        super().__init__(bot, logger_name=logger_name)
        self._webhook_cache = {}

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
                avatar = await user.avatar.read()
                webhook: discord.Webhook = await channel.create_webhook(
                    name="impersonator",
                    avatar=avatar,
                    reason="This is used by the impersonator bot.",
                )
            self._webhook_cache[channel.id] = webhook

        await webhook.send(
            content=message, username=user.display_name, avatar_url=user.avatar.url
        )

        await ctx.interaction.response.send_message("Done :D", ephemeral=True)


def setup(bot: vbu.Bot):
    x = ImpersonationCommands(bot)
    bot.add_cog(x)
