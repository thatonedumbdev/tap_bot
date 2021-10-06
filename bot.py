import discord
import random
import discord.utils
from discord.utils import get
from time import sleep
import asyncio
from discord import Member, Guild
from discord.ext import commands
import webbrowser

youtube = ('https://www.youtube.com')
discord_url = ('https://discord.com')
twitter = ('https://twitter.com')
github = ('https://github.com')
stackoverflow = ('https://stackoverflow.com')

bot = commands.Bot(command_prefix="Your Prefix here")
bot.remove_command('help')
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f'Your Prefix here'))
    print('I logged me in. Beep Bop.')

#moderation commands
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user: discord.Member, *, reason=None):
    await user.kick(reason=reason)
    await user.send(f'You have been kicked by {ctx.author} for reason {reason} !')
    await ctx.send(f"User {user.mention} has been kicked!")
    
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user: discord.Member, *, reason=None):
    await user.ban(reason=reason)
    await user.send(f'You have been banned by {ctx.author} for reason {reason} !')
    await ctx.send(f"\u2705 User {user.mention} has been banned!")
    
@bot.command()
async def unban(ctx, user: discord.Member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention} !')
            await user.send(f'You have been unbanned')
            return

@bot.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        color=discord.Colour.blue()
    )
    embed.set_author(name='--Help for the Commands--')
    embed.add_field(name='ban', value='Bans a Member', inline=False)
    embed.add_field(name='kick', value='Kicks a Member', inline=False)
    embed.add_field(name='unban', value='Unbans Member', inline=False)
    embed.add_field(name='warn', value='warns a Member, this Command is still in development', inline=False)
    embed.add_field(name='clear (amount of messages)', value='deletes Messages', inline=False)
    embed.add_field(name='open(youtube, discord, github etc...)', value='opens the website', inline=False)
    embed.add_field(name='rickroll', value='rickrolls yourself', inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('\u2705')

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount: int):
    sleep(0.5)
    if amount > 100:
        return await ctx.send("You can\'t delete more than 100 messages!")
    elif amount < 1:
        return await ctx.send("You can\'t clear less than 1 message!")
    else:
        await ctx.channel.purge(limit=amount+1)
        
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete!')
        
@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, user: discord.Member, *, reason=None):
    embed = discord.Embed(
        color=discord.Colour.red()
    )
    embed.set_author(name='---You have been warned---')
    embed.add_field(name=f'You have been warned by {ctx.author} for reason {reason} .', value='This message is automatically '
                                                                              'sent. It will be deleted after an '
                                                                              'hour.', inline=False)
    embed2 = discord.Embed(
        color=discord.Colour.green()
    )
    embed2.set_author(name=f'\u2705 Member {user} has been warned')
    embed2.add_field(name=f'You warned {user} for reason {reason} .', value=f'I sent a direct Message to {user} !')
    if user == ctx.author:
        return await ctx.send("You cannot warn yourself!")
    if reason == None:
        return await ctx.send("Please specify a reason to warn this user.")
    warn_count = 0
    warn_count = warn_count + 1
    if warn_count == 3:
        await user.kick()
    await user.send(embed=embed, delete_after=60*60)
    await ctx.send(embed=embed2)
    
#some commands just for fun
@bot.command()
async def rickroll(ctx):
    await ctx.send("You have been **Rickrolled**")
    await webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')




@bot.command()
async def open(ctx, *, reason=None):
    if reason == 'youtube':
        await webbrowser.open(youtube)
    if reason == 'discord':
        await webbrowser.open(discord_url)
    if reason == 'twitter':
        await webbrowser.open(twitter)
    if reason == 'github':
        await webbrowser.open(github)
    if reason == 'stackoverflow':
        await webbrowser.open(stackoverflow)
    else:
        await ctx.send(''''This is not a valid site. The sites that are
                       currently working are YouTube, Discord, Twitter
                       GitHub and StackOverflow.'''')






        
bot.run("Your Token here")
