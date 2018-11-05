import discord
import asyncio
from discord.ext import commands

class Moderation:
    def __init__(self, client):
        self.client = client
        
    @commands.command(pass_context = True)
    async def clear(self, ctx, amount=0):
        if ctx.message.author.server_permissions.manage_messages:
            channel = ctx.message.channel
            messages = []
            async for message in self.client.logs_from(channel, limit=int(amount) + 1):
                messages.append(message)
            await self.client.delete_messages(messages)
            msg = await self.client.say(f'Cleared {amount} message(s)')
            await asyncio.sleep(2)
            await self.client.delete_message(msg)
            return
        else:
            embed = discord.Embed(color=0x36393E)
            embed.add_field(name="<:error:506132126610227200> Error", value="You are missing the following permission: ```Manage Messages```")
            await self.client.say(embed=embed)
            
    @commands.command(pass_context = True)
    async def addrole(ctx, user: discord.Member = None, *, name = None):
      author = ctx.message.author
      try:       
        if ctx.message.author.server_permissions.manage_roles:
          role = discord.utils.get(ctx.message.server.roles, name=name)
          if user is None:
            embed = discord.Embed(color=0xff0200)
            embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
            embed.add_field(name=":x: Error", value="Please specify a user!", inline=False)
            embed.set_footer(text=f"Error Created by: {author.name}")
            await client.say(embed=embed)
            return
          
          if role is None:
            embed = discord.Embed(color=0xff0200)
            embed.set_author(icon_url=author.avatar_url, name="Unknown role!")
            embed.add_field(name=":x: Error", value=f"You made an mistake! ```Error: No role called: {name}```")
            await client.say(embed=embed)
            return
          
          await client.add_roles(user, role)
            embed = discord.Embed(color=0x00ff00)
            embed.add_field(name=":white_check_mark: Sucessful!", value="Role added!")
            embed.add_field(name="Role:", value=f"{role}", inline=False)
            embed.add_field(name="User:", value=f"{user.mention}", inline=False)
            await client.say(embed=embed)
            
        else:
          embed = discord.Embed(color=0xff0200)
          author = ctx.message.author
          embed.set_author(icon_url=author.avatar_url, name="Something went wrong ;-;")
          embed.add_field(name=":x: Error", value="You are missing the following permission: ```Manage Roles```", inline=False)
          await client.say(embed=embed)
          
       except discord.Forbidden:
        embed = discord.Embed(color=0xff0200)
        author = ctx.message.author
        embed.set_author(icon_url=author.avatar.url, name="An error had occured!")
        embed.add_field(name=":x: Error", value="I'm missing the following permission: ```Manage Roles```", inline=False)
        embed.set_footer(text = f"Make sure my role id higher than {user.mention}")
        await client.say(embed=embed)
        
def setup(client):
  client.add_cog(Moderation(client))   
