import asyncio
import os
import shutil
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlmodel import Session, select

from nico_bot.download import download as yt_download
from nico_bot.model import *
from nico_bot.notify import discord_webhook
from nico_bot.sm import load_secret_variables
from nico_bot.upload import upload_drive

load_dotenv()
load_secret_variables()
engine = create_engine(f"sqlite:///{os.environ['DB_NAME']}")
SQLModel.metadata.create_all(engine)


async def download():
    with Session(engine) as session:
        # 登録されたURLを取得
        # URLからダウンロード
        # ダウンロードした動画をGoogle Driveにアップロード
        # URLを完了に登録
        statement = select(Video).where(Video.end == False)
        urls = session.exec(statement).first()
        tmpdir = "./tmp"
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        if not urls:
            print("Rest URL:Not Found ")
            return

        for url in [urls]:
            print(url, tmpdir)
            local_file = yt_download(url.url, tmpdir)
            name = Path(local_file).stem
            drive_file = upload_drive(local_file)
            upload_link = drive_file.get("alternateLink")
            await discord_webhook({
                "username": "nico bot",
                "content": f"{name} is uploaded at {upload_link}"
            },
                os.environ["DISCORD_WEBHOOK_URL"])
        url.end = True
        session.add(url)
        session.commit()


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(download, "cron", minute="*/30")
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    while True:
        await asyncio.sleep(1000)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        # 起動時に取得処理を一度実行
        loop.run_until_complete(download())
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass
