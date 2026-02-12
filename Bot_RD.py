import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ChatMemberStatus

TOKEN = "8083632977:AAGAREk7wP9Xo1EWF5mEQBmgTCXAygAKRuM"

bot = Bot(token=TOKEN)
dp = Dispatcher()


# قبول خودکار جوین ریکوئست
@dp.chat_join_request()
async def approve_join_request(event: types.ChatJoinRequest):
    await bot.approve_chat_join_request(
        chat_id=event.chat.id,
        user_id=event.from_user.id
    )
    print(f"Approved: {event.from_user.id}")


# بن بعد از لفت
@dp.chat_member()
async def ban_after_leave(event: types.ChatMemberUpdated):
    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status

    if old_status in [ChatMemberStatus.MEMBER,
                      ChatMemberStatus.RESTRICTED] and \
       new_status == ChatMemberStatus.LEFT:

        await bot.ban_chat_member(
            chat_id=event.chat.id,
            user_id=event.from_user.id
        )
        print(f"Banned: {event.from_user.id}")


async def main():
    await dp.start_polling(bot)

asyncio.run(main())