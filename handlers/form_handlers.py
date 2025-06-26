import asyncio
from create_bot import bot
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
import re
from aiogram.fsm.state import State, StatesGroup

from keyboards.inline_kbs import check_data

def extract_number(text):
    match = re.search(r'\b(\d+)\b', text)
    if match:
        return int(match.group(1))
    else:
        return None

      
class Form(StatesGroup):
    name = State()
    grade = State()
    direction = State()
    check_state = State()

    
questionnaire_router = Router()


@questionnaire_router.message(F.text == '📝 Заполнить анкету')
async def start_questionnaire_process(message: Message, state: FSMContext):
    await message.answer('Как к Вам обращаться?')
    await state.set_state(Form.name)

    
@questionnaire_router.message(F.text, Form.name)
async def capture_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Супер! В каком ты классе?')
    await state.set_state(Form.grade)

    
@questionnaire_router.message(F.text, Form.grade)
async def capture_age(message: Message, state: FSMContext):
    check_grade = extract_number(message.text)

    if not check_grade or not (1 <= check_grade <= 11):
        await message.reply('Пожалуйста, введите корректный класс (число от 1 до 11).')
        return
    await state.update_data(grade=check_grade)
    await message.answer('Класс! Укажите чем хотите заниматься:')
    await state.set_state(Form.direction)


@questionnaire_router.message(F.text, Form.direction)
async def capture_direction(message: Message, state: FSMContext):
    await state.update_data(direction=message.text)
    data = await state.get_data()
    await message.answer(f'{data.get("name")}\nученик/ученица {data.get("grade")} класса\nРешил(а) изучать: {data.get("direction")}', reply_markup=check_data()) 

    await state.set_state(Form.check_state)


@questionnaire_router.callback_query(F.data == 'correct', Form.check_state)
async def start_questionnaire_process(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if(callback.from_user.username):
        msg_text = (f'Пользователь: @{callback.from_user.username} ждет обслуживания!\nОбращайтесь как: <b>{data.get("name")}</b>\n{data.get("grade")} класс\nНаправление: {data.get("direction")}')
    else:
        user_link = f"tg://user?id={callback.from_user.id}"
        msg_text = (f'Пользователь: {user_link} ждет обслуживания!\nОбращайтесь как: <b>{data.get("name")}</b>\n{data.get("grade")} класс\nНаправление: {data.get("direction")}')

    try:  
        await bot.send_message(1953572824, msg_text) 
        await callback.message.answer('Информация направлена адменистратору, вам напишут в ближайшее время')
    except:  
        await callback.message.answer('Произошла техническая ошибка! напишите нашему админестратору: @migifex')
    await state.clear()


@questionnaire_router.callback_query(F.data == 'incorrect', Form.check_state)
async def start_questionnaire_process(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Заполни анкету с начала:')
    await callback.message.answer('Как к Вам обращаться?')
    await state.set_state(Form.name)
