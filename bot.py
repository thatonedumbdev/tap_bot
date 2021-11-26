import discord
import random
import discord.utils
from discord.utils import get
from time import sleep
from discord import Member, Guild
from discord.ext import commands
import webbrowser

#site variables
youtube = ('https://www.youtube.com')
discord_url = ('https://discord.com')
twitter = ('https://twitter.com')
github = ('https://github.com')
stackoverflow = ('https://stackoverflow.com')
bot = commands.Bot(command_prefix="c!")
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=f'c!help https://discord.gg/8xJJVKZjEN'))
    print('I\'m logged in. Beep Bop.')

#botinfo command
@bot.command()
async def botinfo(ctx):
    botinfo_embed = discord.Embed(
        color = discord.Colour.blue()
    )
    botinfo_embed.set_author(name="-----Bot Info-----")
    botinfo_embed.add_field(name='About this Bot:', value='Chibibot is a Fully Open-Source Discord Bot  with Source Code on GitHub. ')
    botinfo_embed.add_field(name="Prefix:", value="c!, If you want to change it, edit the Source Code.")
    botinfo_embed.add_field(name='Source Code:', value='Bot Source Code on GitHub:'
                                                       ' https://github.com/atomfrog/Chibibot/blob/main/bot.py')
    await ctx.send(embed=botinfo_embed)


#moderation commands
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, user: discord.Member, *, reason=None):
    await user.kick(reason=reason)
    await user.send(f'You have been kicked for reason {reason} !')
    await ctx.send(f"\u2705 User {user.mention} has been kicked!")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry, You aren\'t allowed to kick Users! ")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to specify a User to kick!")

@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, user: discord.Member, *, reason=None):
    await user.ban(reason=reason)
    await user.send(f'You have been banned for reason {reason} !')
    await ctx.send(f"\u2705 User {user.mention} has been banned!")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry, You aren\'t allowed to ban Users! ")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please Specify a User to ban!")



@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'\u2705 Unbanned {user.mention} !')
            return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry, You aren\'t allowed to unban Users! ")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to specify a User to unban!")

@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, user: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)
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
    await user.send(embed=embed, delete_after=60*60)
    await ctx.send(embed=embed2)
    warn_count = 0
    current_warn_count = warn_count + 1
    if current_warn_count == 3:
        await user.kick()

@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry, You aren\'t allowed to warn Users. ")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to specify a User!")

#some commands just for fun
@bot.command()
async def rickroll(ctx):
    await ctx.send("You just got **Rickrolled**")
    await webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')


@bot.command()
async def lotto(ctx, amount: int):
    lottonumber = random.randint(1, 50)
    if amount == lottonumber:
        await ctx.send("Congratulations! You\'re right!")
    elif amount < 1 or amount > 50:
        await ctx.send("Only Numbers between 1 and 50 are valid!")
    else:
        await ctx.send(f"Noo... Sorry, {amount} isn\'t right... The Solution was {lottonumber}. Better Luck next Time!")

@lotto.error
async def lotto_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a number between 1 and 50 after the c!lotto command.")


#opens a site
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
        await ctx.send('This is not a valid URl! Please try YouTube, Discord, Twitter,
                       'GitHub or StackOverflow ')




#help command
@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        color=discord.Colour.blue()
    )
    embed.set_author(name='--Help for the Commands--')
    embed.add_field(name='c!ban', value='Bans a Member', inline=False)
    embed.add_field(name='c!kick', value='Kicks a Member', inline=False)
    embed.add_field(name='c!unban', value='Unbans Member', inline=False)
    embed.add_field(name='c!warn', value='warns a Member, this Command is still in development', inline=False)
    embed.add_field(name='c!clear (amount of messages)', value='deletes Messages', inline=False)
    embed.add_field(name='c!open {YouTube, GitHub, Discord etc.}', value='opens the site', inline=False)
    embed.add_field(name='c!rickroll', value='rickrolls yourself, so don\'t try it', inline=False)
    embed.add_field(name='c!lotto {any number between 1 and 50}', value='starts a small lottery', inline=False)
    embed.add_field(name='If you need help:', value='https://discord.gg/2WRXSjEkzY', inline=False)
    embed.add_field(name='Bot made and Developed by atomfrog and FreerideFriendsYT, Source Code: https://github.com/atomfrog/Chibibot/blob/main/bot.py', value='-----------------------------------', inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('\u2705')


#command to clear a amount of messages
@bot.command()
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

        
bot.run("Your Token here")
