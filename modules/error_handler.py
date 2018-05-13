from discord.ext import commands
import discord, traceback, sys

class error_handler:

    def __init__(self, bot):
        self.bot = bot

    async def send_cmd_help(self, ctx):
        if ctx.invoked_subcommand:
            pages = await self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await ctx.send(page)
        else:
            pages = await self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await ctx.send(page)

    async def on_command_error(self, ctx, exception):
        channel = self.bot.get_channel(431987399581499403)
        if str(exception) == "Command raised an exception: NotFound: NOT FOUND (status code: 404): Unknown Channel":
            return
        if isinstance(exception, commands.NoPrivateMessage):
            return
        elif isinstance(exception, commands.DisabledCommand):
            return
        elif isinstance(exception, discord.Forbidden):
            return
        elif isinstance(exception, discord.NotFound):
            return
        elif isinstance(exception, commands.CommandInvokeError):
            em = discord.Embed(color=0xDEADBF,
                               title="Error",
                               description=f"Error in command {ctx.command.qualified_name}, "
                                           f"[Support Server](https://discord.gg/q98qeYN)")
            await channel.send(embed=discord.Embed(color=0xff6f3f,
                                                   title="Command Error").add_field(
                name=f"Command: {ctx.command.qualified_name}",
                value=f"```py\n{exception}```"))
            await ctx.send(embed=em)
            print('In {}:'.format(ctx.command.qualified_name), file=sys.stderr)
            traceback.print_tb(exception.original.__traceback__)
            print('{}: {}'.format(exception.original.__class__.__name__, exception.original), file=sys.stderr)
        elif isinstance(exception, commands.BadArgument):
            await self.send_cmd_help(ctx)
        elif isinstance(exception, commands.MissingRequiredArgument):
            await self.send_cmd_help(ctx)
        elif isinstance(exception, commands.CheckFailure):
            await ctx.send('You are not allowed to use that command.', delete_after=5)
        elif isinstance(exception, commands.CommandOnCooldown):
            await ctx.send('Command is on cooldown... {:.2f}s left'.format(exception.retry_after), delete_after=5)
        elif isinstance(exception, commands.CommandNotFound):
            return
        else:
            await channel.send(embed=discord.Embed(color=0xff6f3f, title="Unknown Error", description=f"{exception}"))

def setup(bot):
    bot.add_cog(error_handler(bot))