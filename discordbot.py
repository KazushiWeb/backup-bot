import json
import os
import shutil

import discord.utils
from discord.ext import commands

bot = commands.Bot(command_prefix="b!")
bot.remove_command("help")

with open("config.json", "r") as dump:
    config = json.load(dump)


@bot.event

async def on_ready():
	print("[+] Bot backup")


@bot.command(pass_context=True)
async def create(ctx):
	await ctx.message.delete()

	for guild in bot.guilds:
		for category in guild.categories:
			if category.id == config["category_to_backup_id"]:
				await ctx.send("[*] Créations de la  backup...")

                for channel in category.text_channels:
					if not os.path.exists("backup/{}".format(channel)):
						os.makedirs("backup/{}".format(channel))

					with open("backup/{}/messages.txt".format(channel), "w") as file:
						for message in await channel.history().flatten():
							file.write("{}\n".format(message.content))

				await ctx.send("[+] Backup create :white_check_mark:".format(category))

@bot.command(pass_context=True)
async def restore(ctx):
	await ctx.message.delete()

	for guild in bot.guilds:
		for category in guild.categories:
			if category.id == config["category_to_restore_id"]:
				await ctx.send("[*] Restoring backup...")

				for channel_directory in os.listdir("backup"):
					if discord.utils.get(guild.text_channels, name=channel_directory) is None:
						await ctx.guild.create_text_channel(channel_directory, category=category)

				for channel in category.text_channels:
					with open("backup/{}/messages.txt".format(channel), "r") as file:
						for message in file.readlines():
							await channel.send(message)

				await ctx.send("[*] Backup restored :white_check_mark:")


@bot.command(pass_context=True)
async def delete(ctx):
	await ctx.message.delete()

	for guild in bot.guilds:
		for category in guild.categories:
			if category.id == config["category_to_restore_id"]:
				await ctx.send("[*] suppression d'la backup...")

				try:
					if os.path.exists("backup"):
						shutil.rmtree("backup")
					for channel in category.text_channels:
						await channel.delete()

				except:
					await ctx.send("[!] Vous ne pouvez pas supprimer la sauvegarde avec la restauration! :x:")

				await ctx.send("[+] Sauvegarde supprimée :white_check_mark:")


bot.run(config["token"])


