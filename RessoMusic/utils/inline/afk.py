import discord
from discord.ext import commands

# AFK Users Dictionary
afk_users = {}

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="afk")
    async def afk(self, ctx, *, reason="No reason provided"):
        """Sets the user as AFK"""
        afk_users[ctx.author.id] = reason
        await ctx.send(f"{ctx.author.mention} is now AFK: {reason}")

    @commands.Cog.listener()
    async def on_message(self, message):
        """Checks mentions and notifies if a user is AFK"""
        if message.author.bot:
            return

        if message.author.id in afk_users:
            del afk_users[message.author.id]  # Remove AFK status
            await message.channel.send(f"{message.author.mention}, welcome back! I removed your AFK status.")

        for mention in message.mentions:
            if mention.id in afk_users:
                await message.channel.send(f"{mention.mention} is currently AFK: {afk_users[mention.id]}")

# Add Cog to Bot
async def setup(bot):
    await bot.add_cog(AFK(bot))
