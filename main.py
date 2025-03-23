import os
import discord
import requests
from dotenv import load_dotenv
from discord import app_commands
from discord.ui import View, Button

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_API_URL = "https://api.github.com/repos/voltarian-Dev-Team/weblyne.doom/commits"


# Set up Discord bot
class Client(discord.Client):

    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


client = Client()


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.tree.command(name="info", description="Get information about WebLyne DOOM®")
async def info(interaction: discord.Interaction):
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        commit_id = response.json()[0]["sha"][:7]
    else:
        commit_id = "Unable to fetch commit ID"

    # Create an embed
    embed = discord.Embed(
        title="WebLyne DOOM®",
        description="Experience the classic DOOM® in your web browser!",
        color=0x7A0019
    )
    
    # Add version field (using commit ID as the version)
    embed.add_field(name="Version", value=commit_id, inline=True)
    embed.add_field(name="Developer", value="Voltarian Dev Team", inline=True)

    # Set a footer
    embed.set_footer(text="WebLyne DOOM® - Bringing retro gaming to your browser")

    # Set the thumbnail url
    embed.set_thumbnail(url="https://raw.githubusercontent.com/Voltarian-Dev-Team/WebLyne.DoomBot/refs/heads/main/assets/images/weblyne_banner.jpg")

    # Create buttons (optional, in case you still want them)
    button1 = Button(label="GitHub Pages", url="https://voltarian-dev-team.github.io/WebLyne.Doom/")
    button2 = Button(label="Voltaccept's Domain", url="https://voltarius.voltaccept.com/weblyne.doom/")

    # Create view and add buttons
    view = View()
    view.add_item(button1)
    view.add_item(button2)

    # Send the embed with the view and image (if available)
    await interaction.response.send_message(embed=embed, view=view)


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)