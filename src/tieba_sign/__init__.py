import asyncio
import logging
from dataclasses import dataclass

from tieba_sign.tieba import Tieba, Forum
from tieba_sign.config import Config
import tieba_sign.error_handling as _

__all__ = ["Tieba", "Forum", "main"]

async def _main():

    config = Config(request=dict(concurrency=3))

    @dataclass
    class SignErrorInfo:
        name: str
        exception_type: str
        exception_message: str

    tieba = Tieba()

    # get forums to sign
    forums = await tieba.get_forums()
    forums_total_count = len(forums)

    forums = [forum for forum in forums if not forum.is_sign]
    forums_not_signed_count = len(forums)

    forums_signed_count = forums_total_count - forums_not_signed_count

    logging.info(f"贴吧签到状态: {forums_signed_count}/{forums_total_count}")

    if forums_not_signed_count == 0:
        logging.info("所有贴吧已签过")
        return

    # sign
    logging.info("签到中...")

    semaphore = asyncio.Semaphore(config.config["request"]["concurrency"])
    async def sign(forum: Forum):
        try:
            async with semaphore:
                await forum.sign()
        except Exception as e:
            return SignErrorInfo(forum.name, type(e).__name__, str(e))

    # result
    sign_results = asyncio.gather(*[sign(forum) for forum in forums])
    sign_errors = [result for result in await sign_results if result]

    if len(sign_errors) == 0:
        logging.info("贴吧签到成功")
        return

    # error logging
    for sign_error in sign_errors:
        logging.error(f"签到失败: {sign_error.name}")
        logging.error(f"{sign_error.exception_type}: {sign_error.exception_message}")

    logging.info(f"签到失败: {len(sign_errors)}/{forums_not_signed_count}")

def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    asyncio.run(_main())
