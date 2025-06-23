import asyncio
from aiogram.types import BotCommand
from create_bot import bot, dp, scheduler
from handlers.main_handlers import start_router
# from work_time.time_func import send_time_msg

async def main():
    # scheduler.add_job(send_time_msg, 'interval', seconds=10)
    main_menu_commands = [
        BotCommand(command='/start', description='Запуск бота'),
        BotCommand(command='/help', description='Помощь'),
    ]
    
    await bot.set_my_commands(main_menu_commands)
    scheduler.start()
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())