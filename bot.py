import os
import re

import discord
from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from nico_bot.model import Video
from nico_bot.sm import load_secret_variables

load_dotenv()
load_secret_variables()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
engine = create_engine(f"sqlite:///{os.environ['DB_NAME']}")
SQLModel.metadata.create_all(engine)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


def is_valid_nico_video_url_regex(url):
    # Regular expression for a simple URL validation
    url_pattern = re.compile(r'^https?://www.nicovideo.jp/watch/sm\S+$', re.IGNORECASE)
    return bool(re.match(url_pattern, url))


@bot.command(name="nico_add")
async def add(ctx, *args):
    """Adds two numbers together."""
    try:
        with Session(engine) as session:
            for url in args:
                if not is_valid_nico_video_url_regex(url):
                    await ctx.send(f"{url} is ignored")
                    continue
                video = Video(url=url)
                session.add(video)
                session.commit()
                await ctx.send(f"{url} is added")

    except Exception as e:
        await ctx.send(f"add failed:{e}")
        return


@bot.command(name="nico_rest")
async def status(ctx):
    try:
        with Session(engine) as session:
            not_processed_url = session.exec(select(Video).where(Video.end == False)).all()
            not_processed_url = list(map(lambda p: f"{p.url}", not_processed_url))
        await ctx.send("未処理動画 一覧\n" + "\n".join(not_processed_url))
        pass
    except Exception as e:
        await ctx.send(f"rest command  failed:{e}")


bot.run(os.environ["DISCORD_BOT_TOKEN"])
