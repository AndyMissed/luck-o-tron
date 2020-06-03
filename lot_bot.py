# Code for Luck-o-Tron Discord bot
# Version 1.1.0
# Copyright © 2020 AndyMissed

import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix='%')

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game('the odds | %help'))
  print('Luck-o-Tron is online.')

bot.remove_command('help')


# Takes a list of strings (str_list) and combines them together in a formatted manner.
def align(str_list):
  index_bot = 0
  index_top = 0
  remaining = len(str_list)
  delayed_ten = 0
  loop = 1
  output = []
  while loop == 1:
    if remaining > 10:
      index_bot = index_bot + delayed_ten
      index_top = index_bot + 10
      remaining -= 10
      delayed_ten = 10
    else:
      index_bot = index_bot + delayed_ten
      index_top = index_bot + remaining
      loop = 0
    output.append('`|'+'|'.join(str_list[index_bot:index_top])+'|`')
  output = '\n'.join(output)
  return output


# Takes an integer (number) and another integer (num_max).
# Outputs [number] as a string, and adds spaces based on missing digits in comparison to [num_max].
# [num_max] should always be higher than [number].
def add_gaps(number, num_max):
  num_str = str(number)
  max_str = str(num_max)
  num_len = len(num_str)
  max_len = len(max_str)
  if num_len == max_len:
    output = (num_str)
    return output
  else:
    numgaps = max_len - num_len
    output = (' '*numgaps)+num_str
    return output


# 'Rolls' a die with a specified number of sides (sides) and outputs a random number.
# Luck is an essential argument to set the behavior of randomness.
# Luck needs to be between −[sides] and [sides].
def rng(sides, luck):
  if luck == 0:
    random.seed(os.urandom(4))
    output = random.randint(1, sides)
    return output
  else:
    abs_luck = abs(luck)
    upper_bound = abs_luck+1
    if upper_bound == sides+1:
      upper_bound = sides
    lower_bound = 1
    rolls = 2
    while rolls >= 1:
      random.seed(os.urandom(4))
      chance = random.randint(1, sides)
      if chance > abs_luck:
        rolls -= 1
      random.seed(os.urandom(4))
      lower_bound = random.randint(lower_bound, upper_bound)
      rolls -= 1
    random.seed(os.urandom(4))
    output = random.randint(lower_bound, sides)
    if luck > 0:
      return output
    elif luck < 0:
      return (sides+1)-output  # Hacky code that 'inverts' the result for negative values of luck.


def convert(string):
  output = discord.Embed(
    description=string
    )
  return output


@bot.command()
async def help(chat, word = str()):
  if word == 'd20':
    msg = discord.Embed(
      title='Usage',
      description='`%d20 [# of dice] [# of luck]`'
      )
    await chat.send(embed=msg)
  elif word == 'roll':
    msg = discord.Embed(
      title='Usage',
      description='`%roll [# of sides] [# of dice] [# of luck]`'
      )
    await chat.send(embed=msg)
  elif word == 'luck':
    msg = discord.Embed(
      title='Luck',
      description=
      'Luck is a value that modifies the randomness of a roll.\n\n'+
      'If the value of luck is 0 (Default), rolls behave normally.\n\n'+
      'As the value of luck increases (Up to a maximum of [the # of sides]), '+
      'low numbers become rolled less frequently.\n\n'+
      'As the value of luck decreases, '+
      'high numbers become rolled less frequently.\n'+
      '(It should be noted that luck can go negative down to '+
      'a minimum of [the # of sides, but negative])\n\n'+
      'In essence, your average roll gets lower with lower luck, '+
      'and gets higher with higher luck.\n\n'+
      'As an example, if you have a d20 with 20 luck (maximum luck), '+
      'the odds of rolling a 1 is essentially reduced to 1 out of every 8000 rolls.'
      )
    await chat.send(embed=msg)
  elif word == 'features':
    msg = discord.Embed(
      title='Features'
      )
    msg.add_field(
      name='`luck`',
      value='Controls the randomness of a roll.',
      inline=False
      )
    msg.set_footer(
      text='Use "%help [feature]" for more information.'
      )
    await chat.send(embed=msg)
  elif word != '':
    msg = convert(f'`{word}` is not a recognized command or feature.')
    await chat.send(embed=msg)
  else:
    msg = discord.Embed(
      title='Commands'
      )
    msg.add_field(
      name='`%d20`',
      value='Rolls a 20-sided die.',
      inline=False
      )
    msg.add_field(
      name='`%roll`',
      value=
      'Rolls a die with a specified amount of sides.\n'+
      'Defaults to 6 if no sides specified.',
      inline=False
      )
    msg.set_footer(
      text=
      'Use "%help [command]" for more information.\n'+
      'Use "%help features" for information about features.'
      )
    await chat.send(embed=msg)


@bot.command()
async def d20(chat, n_dice: str = '1', n_luck: str = '0'):
  error = 0
  try:
    n_dice = int(n_dice)
  except ValueError:
    msg = convert(f'`{n_dice}` is not a valid number.')
    await chat.send(embed=msg)
    error = 1
  try:
    n_luck = int(n_luck)
  except ValueError:
    msg = convert(f'`{n_luck}` is not a valid number.')
    await chat.send(embed=msg)
    error = 1
    
  if error == 0:
    if not -20 <= n_luck <= 20 or not 1 <= n_dice <= 100:
      if not -20 <= n_luck <= 20:
        msg = convert('Luck must be within −20 to 20.')
        await chat.send(embed=msg)
      if n_dice > 100:
        msg = convert('Dice must be within 1 to 100.')
        await chat.send(embed=msg)
      if n_dice == 0:
        msg = convert('No dice. Sorry.')
        await chat.send(embed=msg)
      if n_dice < 0:
        msg = convert('In Soviet Russia, dice throw *you*.')
        await chat.send(embed=msg)
      error = 1
      
    if error == 0:
      roll = []
      total = 0
      for i in range(n_dice):
        num = rng(20, n_luck)
        total += num
        roll.append(add_gaps(num, 20))
        
      msg = discord.Embed(
        title='Result',
        description=f'{align(roll)}',
        color=0xf0f0f0
        )
      if n_dice > 1:
        msg.title = 'Results'
        msg.set_footer(
          text=f'Total: {total}'
          )
      await chat.send(embed=msg)


@bot.command()
async def roll(chat, n_sides: str = '6', n_dice: str = '1', n_luck: str = '0'):
  error = 0
  pointless = 0  # Flag for pointless code execution.
  try:
    n_sides = int(n_sides)
  except ValueError:
    msg = convert(f'`{n_sides}` is not a valid number.')
    await chat.send(embed=msg)
    error = 1
  try:
    n_dice = int(n_dice)
  except ValueError:
    msg = convert(f'`{n_dice}` is not a valid number.')
    await chat.send(embed=msg)
    error = 1
  try:
    n_luck = int(n_luck)
  except ValueError:
    msg = convert(f'`{n_luck}` is not a valid number.')
    await chat.send(embed=msg)
    error = 1
    
  if error == 0:
    if not (n_sides*-1) <= n_luck <= n_sides or not 1 <= n_sides <= 9999 or not 1 <= n_dice <= 100:
      if not ((n_sides*-1) <= n_luck <= n_sides) and n_sides > 1:
        msg = convert(f'Luck must be within −{n_sides} to {n_sides}.')
        await chat.send(embed=msg)
      if n_sides > 9999:
        msg = convert('Sides must be within 2 to 9999.')
        await chat.send(embed=msg)
      if n_sides == 0:
        msg = convert('You can\'t have zero sides; You\'d break the universe.')
        await chat.send(embed=msg)
      if n_sides < 0:
        msg = convert('Negative sides? Don\'t be silly.')
        await chat.send(embed=msg)
      if n_dice > 100:
        msg = convert('Dice must be within 1 to 100.')
        await chat.send(embed=msg)
      if n_dice == 0:
        msg = convert('No dice. Sorry.')
        await chat.send(embed=msg)
      if n_dice < 0:
        msg = convert('In Soviet Russia, dice throw *you*.')
        await chat.send(embed=msg)
      error = 1
    if n_sides == 1:  # Why has the user done this?
      pointless = 1
      
    if error == 0:
      roll = []
      total = 0
      for i in range(n_dice):
        num = rng(n_sides, n_luck)
        total += num
        roll.append(add_gaps(num, n_sides))
        
      msg = discord.Embed(
        title='Result',
        description=f'{align(roll)}',
        color=0xf0f0f0
        )
      if n_dice > 1:
        msg.title = 'Results'
        msg.set_footer(
          text=f'Total: {total}'
          )
      if pointless == 1:  # If you insist...
        msg.title = 'Seriously?'
      await chat.send(embed=msg)


bot.run(TOKEN)