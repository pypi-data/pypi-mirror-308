import asyncio
import logging
import sys

from pyflowery import VERSION, FloweryAPI, FloweryAPIConfig

root = logging.getLogger()
root.setLevel(level=logging.DEBUG)

handler = logging.StreamHandler(stream=sys.stdout)
handler.setLevel(level=logging.DEBUG)
formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(fmt=formatter)
root.addHandler(hdlr=handler)

api = FloweryAPI(config=FloweryAPIConfig(user_agent=f"PyFloweryTests/{VERSION}"))

ALEXANDER = "fa3ea565-121f-5efd-b4e9-59895c77df23"  # TikTok
JACOB = "38f45366-68e8-5d39-b1ef-3fd4eeb61cdb"  # Microsoft Azure
STORMTROOPER = "191c5adc-a092-5eea-b4ff-ce01f66153ae"  # TikTok


async def test_fetch_tts() -> None:
    """Test the fetch_tts method"""
    voice = api.get_voices(voice_id=ALEXANDER)
    if voice is None:
        raise ValueError("Voice not found")
    tts = await api.fetch_tts(text="Sphinx of black quartz, judge my vow. The quick brown fox jumps over a lazy dog.", voice=voice[0])
    try:
        with open(file="test.mp3", mode="wb") as f:
            f.write(tts)
    except Exception as e:  # pylint: disable=broad-except
        api.config.logger.error(e, exc_info=True)
    long_string = "a" * 2049
    try:
        await api.fetch_tts(text=long_string)
    except ValueError as e:
        api.config.logger.error("This is expected to fail, and is not causing a non-zero exit code:\n%s", e, exc_info=True)


if __name__ == "__main__":
    api.config.logger.info("testing fetch_tts")
    asyncio.run(main=test_fetch_tts())
