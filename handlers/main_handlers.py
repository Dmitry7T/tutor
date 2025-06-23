from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Давайте приступим')

@start_router.message(Command('help'))
async def cmd_start_2(message: Message):
    await message.answer('вы в разделе помощи!')

@start_router.message(F.text == 'Hi')
async def cmd_start_3(message: Message):
    await message.answer('Hi')