import discord
from discord.ext import commands
from discord.ext import tasks
import logging
import datetime
from decouple import config
from WoW_Price import WowToken
from USDT_Price import precio_usdt
import asyncio

hora = datetime.datetime.now()
logging.basicConfig(level=logging.INFO,
                    filename=f"Bot module - {hora.strftime('%d')}-{hora.strftime('%b')}-{hora.strftime('%Y')} - {hora.strftime('%H')}-{hora.strftime('%M')}-{hora.strftime('%S')}.log",
                    filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s")

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
wow = WowToken()
client_token = config("token_discord")


def precios():
    try:
        usdt = precio_usdt()
        texto_usdt = f'USDT/Bs C: {usdt[0]} V: {usdt[1]}'
        token_de_wow = wow.precio()
        texto_wow = f'WoW Token: {token_de_wow} Gold'
        lista = (texto_usdt,texto_wow)
        return lista
    except Exception as e:
        logging.exception("Error - {}".format(e))
        
        
@tasks.loop(seconds=10)
async def mensaje():
    try:
        estados = precios()
        for estado in estados:
            await client.change_presence(activity=discord.CustomActivity(estado))
            await asyncio.sleep(5)
    except Exception as e:
        logging.exception("Error - {}".format(e))
        
@client.event
async def on_ready():
    try:
        await client.tree.sync()
        mensaje.start()
    except Exception as e:
        logging.exception("Error - {}".format(e))
        
        
client.run(client_token)