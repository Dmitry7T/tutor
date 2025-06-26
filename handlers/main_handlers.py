from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards.inline_kbs import ease_link_kb
from create_bot import admins
from keyboards.all_kb import main_kb

start_router = Router()


'''Commands'''
@start_router.message(CommandStart() or F.data == 'start')
async def cmd_start(message: Message):
    await message.answer('Начало работы с ботом',
                         reply_markup=main_kb(message.from_user.id))

@start_router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('вы в разделе помощи!')

'''main_kb answer'''
@start_router.message(F.text == '📖 О нас')
async def about(message: Message):
    #await message.delete()
    await message.answer('Мы онлайн школа...', reply_markup=ease_link_kb())

'''@start_router.message(F.text == '👤 Профиль')
async def profile(message: Message):
    #await message.delete()
    await message.answer('ваш профиль')'''

@start_router.message(F.text == '📚 Каталог')
async def Catalog(message: Message):
    #await message.delete()
    await message.answer('Мы предлогаем следующие курсы:\n...')

@start_router.message(F.text == '⚙️ Админ панель')
async def admin_panel(message: Message):
    if  message.from_user.id in admins:
        await message.answer('эта панель доступна только админестратору')