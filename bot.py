import os
import re
from typing import List

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
    await bot.tree.sync()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


def is_valid_nico_video_url_regex(url):
    # Regular expression for a simple URL validation
    url_pattern = re.compile(r'^https?://www.nicovideo.jp/watch/sm\S+$', re.IGNORECASE)
    return bool(re.match(url_pattern, url))


@bot.tree.command(name="nico_add", description="ダウンロードするURLを追加。")
async def add(ctx, url: str):
    """Adds two numbers together."""
    try:
        with Session(engine) as session:
            if not is_valid_nico_video_url_regex(url):
                await ctx.response.send_message(f"{url} is ignored")
            video = Video(url=url)
            session.add(video)
            session.commit()
            await ctx.response.send_message(f"{url} is added")

    except Exception as e:
        await ctx.response.send_message(f"add failed:{e}")
        return


@bot.tree.command(name="nico_rest", description="未処理の動画状況を取得。")
async def status(ctx):
    try:
        with Session(engine) as session:
            not_processed_url = session.exec(select(Video).where(Video.end == False)).all()
            not_processed_url = list(map(lambda p: f"{p.url}", not_processed_url))
        await ctx.response.send_message("未処理動画 一覧\n" + "\n".join(not_processed_url))
        pass
    except Exception as e:
        await ctx.response.send_message(f"rest command  failed:{e}")


bot.run(os.environ["DISCORD_BOT_TOKEN"])
