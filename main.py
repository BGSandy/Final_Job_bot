import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

TOKEN = "8521212878:AAHzq9i2b9rneukr6Ak_j47rPjBrQTdee90"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Quiz(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()

def get_kb(options):
    buttons = [[types.KeyboardButton(text=opt)] for opt in options]
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Начать тест")],
        [types.KeyboardButton(text="💡 О проекте")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Привет! Я расширенный бот-профориентатор. Готов найти твое призвание?", reply_markup=keyboard)

@dp.message(F.text == "💡 О проекте")
async def about(message: types.Message):
    await message.answer("Проект 'CareerNavigator' использует систему анализа интересов по 4 векторам: Технологии, Творчество, Социум и Аналитика.")

@dp.message(F.text == "Начать тест")
async def start_quiz(message: types.Message, state: FSMContext):
    await state.set_state(Quiz.q1)
    await state.update_data(it=0, creative=0, social=0, logic=0)
    await message.answer("1. Чем бы ты предпочел заниматься в свободное время?", 
                         reply_markup=get_kb(["Чинить/разбирать гаджеты", "Рисовать/монтировать видео", "Общаться в большой компании", "Разгадывать головоломки"]))

@dp.message(Quiz.q1)
async def q1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "Чинить" in message.text: data['it'] += 1
    elif "Рисовать" in message.text: data['creative'] += 1
    elif "Общаться" in message.text: data['social'] += 1
    else: data['logic'] += 1
    
    await state.update_data(data)
    await state.set_state(Quiz.q2)
    await message.answer("2. Какой школьный предмет тебе ближе?", 
                         reply_markup=get_kb(["Информатика", "Литература/ИЗО", "Обществознание", "Математика"]))

@dp.message(Quiz.q2)
async def q2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "Информатика" in message.text: data['it'] += 1
    elif "Литература" in message.text: data['creative'] += 1

    elif "Обществознание" in message.text: data['social'] += 1
    else: data['logic'] += 1
    
    await state.update_data(data)
    await state.set_state(Quiz.q3)
    await message.answer("3. В какой атмосфере тебе комфортнее работать?", 
                         reply_markup=get_kb(["Наедине с компьютером", "В мастерской/студии", "В центре событий с людьми", "В тихом офисе с графиками"]))

@dp.message(Quiz.q3)
async def q3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "компьютером" in message.text: data['it'] += 1
    elif "студии" in message.text: data['creative'] += 1
    elif "людьми" in message.text: data['social'] += 1
    else: data['logic'] += 1
    
    await state.update_data(data)
    await state.set_state(Quiz.q4)
    await message.answer("4. Что для тебя важнее всего в работе?", 
                         reply_markup=get_kb(["Создать работающий механизм", "Выразить идею", "Помочь кому-то", "Найти истину/ошибку"]))

@dp.message(Quiz.q4)
async def q4(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "механизм" in message.text: data['it'] += 1
    elif "идею" in message.text: data['creative'] += 1
    elif "Помочь" in message.text: data['social'] += 1
    else: data['logic'] += 1
    
    await state.update_data(data)
    await state.set_state(Quiz.q5)
    await message.answer("5. Если бы ты писал книгу, о чем бы она была?", 
                         reply_markup=get_kb(["О технологиях будущего", "О чувствах и искусстве", "О жизни великих людей", "О тайнах Вселенной и числах"]))

@dp.message(Quiz.q5)
async def q5(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if "технологиях" in message.text: data['it'] += 1
    elif "чувствах" in message.text: data['creative'] += 1
    elif "людей" in message.text: data['social'] += 1
    else: data['logic'] += 1

    res = sorted(data.items(), key=lambda x: x[1], reverse=True)[0][0]
    
    results = {
        "it": "Твой путь — IT и инженерия. Обрати внимание на профессии: Разработчик, Системный администратор, Специалист по кибербезопасности.",
        "creative": "Твоя стихия — Творчество. Тебе подойдут: Графический дизайнер, Геймдизайнер, Арт-директор или Видеомонтажер.",
        "social": "Ты рожден работать с людьми. Твои сферы: Психология, Педагогика, Маркетинг или PR-менеджмент.",
        "logic": "Твой мозг настроен на анализ. Идеальные профессии: Аналитик данных, Финансист, Ученый или Тестировщик (QA)."
    }

    await message.answer(f"Результаты теста готовы!\n\n{results[res]}", 
                         reply_markup=get_kb(["Начать тест"]))
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
