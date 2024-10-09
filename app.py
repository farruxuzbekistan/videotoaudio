#! farruhdeveloper
# 7895621883:AAHNX4tBg8_63NQ4_MRH21VDnB6K2xGTaVw
from aiogram import Bot, Dispatcher, executor, types

import moviepy.editor as mp
import os
import io
import tempfile
import aiogram.utils.exceptions

API_TOKEN = "7895621883:AAHNX4tBg8_63NQ4_MRH21VDnB6K2xGTaVw"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


MAX_FILE_SIZE = 50 * 1024 * 1024


def convert_video_to_audio(video_stream: io.BytesIO):
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".mp4"
        ) as temp_video_file:
            temp_video_file.write(video_stream.read())
            temp_video_file.flush()
            video = mp.VideoFileClip(temp_video_file.name)
            audio_path = temp_video_file.name.replace(".mp4", ".mp3")

            video.audio.write_audiofile(audio_path)

            return audio_path

    except Exception as e:
        print(f"Error processing video file: {e}")
        return None


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer(
        "Assalom alaykum, bizga 50mb kam bo'lgan video yuboring, va biz uni audioga aylantirib beramiz."
    )


# @dp.message_handler(content_types=types.ContentType.VIDEO)
@dp.message_handler(content_types=["video"])
async def handle_video(message: types.Message):
    try:
        print("try")
        if message.video.file_size > MAX_FILE_SIZE:
            await message.reply(
                f"Fayl Hajmi juda katta, iltimos {MAX_FILE_SIZE // (1024*1024)}mb dan oshmasin "
            )
            return
        video_bytes = await message.video.download(destination_file=io.BytesIO())

        audio_path = convert_video_to_audio(video_bytes)

        if not audio_path:
            await message.reply("Video yuklashda xatolik yuz berdi")
            return

        with open(audio_path, "rb") as audio:
            await message.reply("Mana sizni audio faylngiz!")
            await message.answer_audio(audio)

        os.remove(audio_path)

    except aiogram.utils.exceptions.FileIsTooBig:
        await message.reply("Fayl Hajmi juda katta, iltimos 50mb dan oshmasin ")

    except Exception as e:
        await message.reply(f"Xato Yuz berdi: {e}")


if __name__ == "__main__":
    os.makedirs("videos", exist_ok=True)
    executor.start_polling(dp, skip_updates=True)
