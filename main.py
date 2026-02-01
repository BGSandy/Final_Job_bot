import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramBadRequest

TOKEN = "8521212878:AAHzq9i2b9rneukr6Ak_j47rPjBrQTdee90"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

ADMIN_USER_ID = 6935205868

PICTURES = {
    "it": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJueGZueXF6eXJ6eXJ6eXJ6eXJ6eXJ6eXJ6eXJ6eXJ6eXJ6JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/SWoSkN6DxTszqIKEqv/giphy.gif",
    "creative": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnhzdWRlaWdnNDNrcGl6M2w5czg1czg1czg1czg1czg1czg1czg1czg1czg1czg1JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l4FGyzm3aD7w92G3N/giphy.gif",
    "social": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTFjMzg0Y2NtbWFnZmtzZmZzZmZzZmZzZmZzZmZzZmZzZmZzZmZzZmZzJmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKuWf3e9q65r50g/giphy.gif",
    "logic": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWU5YzF6ejRxNDdwdm1sdnZscHNnc2xicHlxOXA0dGRubzJ3djc0eCZjdD1n/l4FGx4tG43jK5uWbu/giphy.gif",
    "practice": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWJqbzUzd3lqZnZkdzJ0MXBocWkxcXJkNW4zZWpjd2g2bTRzdzZ2ZCZjdD1n/26uf3i48l7059fV3i/giphy.gif"
}

class Quiz(StatesGroup):
    q1, q2, q3, q4, q5, q6, q7, q8, q9, q10 = State(), State(), State(), State(), State(), State(), State(), State(), State(), State()
    q11, q12, q13, q14, q15 = State(), State(), State(), State(), State()
    feedback_mode = State()

def main_kb():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="🚀 Начать тест")],
        [types.KeyboardButton(text="💡 О проекте")],
        [types.KeyboardButton(text="💬 Обратная связь")],
        [types.KeyboardButton(text="/help")],
        [types.KeyboardButton(text="🗑️ Очистить чат")]
    ], resize_keyboard=True)

def ans_kb():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="А"), types.KeyboardButton(text="Б"), types.KeyboardButton(text="В"), types.KeyboardButton(text="Г"), types.KeyboardButton(text="Д")],
        [types.KeyboardButton(text="❌ Отменить тест"), types.KeyboardButton(text="🗑️ Очистить чат")],
        [types.KeyboardButton(text="💬 Обратная связь")]
    ], resize_keyboard=True)

ABOUT_TEXT = (
    "🤖 *CareerNavigator* — это инновационный бот-помощник для выбора будущей профессии.\n\n"
    "🎯 *Цель проекта:* Помочь подросткам и студентам определиться с направлением развития в мире современных технологий и медиа.\n\n"
    "📊 *Как это работает?*\n"
    "Тест состоит из 15 вопросов, разработанных на основе методик профориентации. Бот анализирует ваши ответы по 5 ключевым категориям:\n"
    "1️⃣ *IT и Технологии* — создание цифровых продуктов.\n"
    "2️⃣ *Творчество* — визуальное искусство и медиа.\n"
    "3️⃣ *Социум* — работа с людьми и психология.\n"
    "4️⃣ *Аналитика* — логика, финансы и наука.\n"
    "5️⃣ *Практика* — инженерия и реальное производство.\n\n"
    "✨ В конце вы получите не только сферу, но и список профессий будущего!"
)

HELP_TEXT = (
    "🤖 *CareerNavigator: Команды*\n\n"
    "🚀 */start* - Начать или перезапустить бот.\n"
    "📝 *Начать тест* - Запустить профориентационный тест.\n"
    "💡 *О проекте* - Узнать больше о том, как работает бот.\n"
    "❌ *Отменить тест* - Прервать тестирование в любой момент.\n"
    "🗑️ *Очистить чат* - Удалить все сообщения из чата (которые бот ещё может удалить).\n"
    "💬 *Обратная связь* - Отправить свои предложения или замечания разработчику бота.\n"
    "❓ */help* - Показать это сообщение со списком команд.\n\n"
    "Тестируйте и находите свое призвание!"
)

FEEDBACK_PROMPT = "Пожалуйста, напишите ваше сообщение для обратной связи. Мы ценим каждое мнение! Чтобы вернуться в главное меню без отправки, нажмите '❌ Отменить тест'."
FEEDBACK_CONFIRMATION_USER = "Спасибо за вашу обратную связь! Мы обязательно рассмотрим ваше предложение."

QUESTIONS = [
    "1. Что тебе интереснее изучать?\nА) Языки программирования\nБ) Историю искусств\nВ) Психологию общения\nГ) Математические модели\nД) Устройство механизмов",
    "2. Твой идеальный выходной?\nА) Хакатон или видеоигры\nБ) Поход на выставку или рисунок\nВ) Волонтерство или общение\nГ) Головоломки или чтение\nД) Ремонт техники или сборка моделей",
    "3. Какую суперсилу ты бы выбрал?\nА) Понимать код любого уровня\nБ) Создавать миры силой мысли\nВ) Исцелять и вдохновлять людей\nГ) Видеть скрытые закономерности\nД) Управлять материей и металлом",
    "4. В какой школе ты бы учился?\nА) Кибер-технологий\nБ) Дизайна и медиа\nВ) Педагогики и медицины\nГ) Чистой науки и логики\nД) Архитектуры и ремесла",
    "5. Что тебя больше раздражает?\nА) Медленный софт/интернет\nБ) Безвкусное оформление\nВ) Конфликты в коллективе\nГ) Логические ошибки в данных\nД) Когда сломанная вещь не чинится",
    "6. Какую соцсеть ты бы развивал?\nА) Платформу для разработчиков\nБ) Визуальную галерею / Pinterest\nВ) Блог о помощи и психологии\nГ) Инфографику и научные факты\nД) Канал о мастерстве и путешествиях",
    "7. Твой самый ценный навык?\nА) Алгоритмическое мышление\nБ) Креативный подход\nВ) Умение слушать\nГ) Внимание к деталям\nД) Практическая хватка",
    "8. Что важнее в работе?\nА) Новизна технологий\nБ) Визуальный восторг\nВ) Счастье окружающих\nГ) Точность прогнозов\nД) Долговечность продукта",
    "9. Твоя роль в команде?\nА) Архитектор решений\nБ) Генератор идей\nВ) Миротворец / Организатор\nГ) Аналитик рисков\nД) Тот, кто делает руками",
    "10. Какую книгу ты выберешь?\nА) Будущее нейросетей\nБ) Тайны великих художников\nВ) Психология влияния\nГ) Теория вероятностей\nД) Справочник инженера",
    "11. Что тебя вдохновляет?\nА) Чистая работа программы\nБ) Гармония цветов и форм\nВ) Успех друга по твоему совету\nГ) Красивая математическая правда\nД) Работающий механизм",
    "12. Где ты хочешь работать?\nА) Крупная ИТ-корпорация\nБ) Креативное агентство\nВ) Образовательный центр\nГ) Исследовательский центр\nД) Высокотехнологичный завод",
    "13. Твое отношение к задачам?\nА) Ищу самый быстрый алгоритм\nБ) Ищу самый красивый способ\nВ) Ищу решение, выгодное всем\nГ) Сначала всё просчитываю\nД) Сразу приступаю к делу",
    "14. Идеальный проект — это...?\nА) Полезное приложение\nБ) Красивая выставка/фильм\nВ) Благотворительная акция\nГ) Экономический план\nД) Построенный дом или робот",
    "15. Твой главный девиз?\nА) Автоматизируй всё!\nБ) Твори без границ!\nВ) Помогай и созидай!\nГ) Истина в цифрах!\nД) Строй на века!"
]

async def save_message_id(state: FSMContext, message_id: int):
    data = await state.get_data()
    message_ids = data.get('message_ids', [])
    message_ids.append(message_id)
    await state.update_data(message_ids=message_ids)

@dp.message(Command("start"))
async def start(m: types.Message, state: FSMContext):
    await state.update_data(message_ids=[m.message_id])

    inline_kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Подробнее о боте", callback_data="show_about_inline")],
        [types.InlineKeyboardButton(text="Проект на GitHub", url="https://github.com/YourGitHubLinkHere")] # ВСТАВЬ СВОЮ ССЫЛКУ!
    ])
    
    bot_message = await m.answer(
        "Привет! Я *CareerNavigator* — твой помощник в выборе профессии.\n"
        "Нажми на кнопку ниже, чтобы узнать о проекте или сразу начать тест.\n\n"
        "Было сделано: @BGChester", 
        reply_markup=inline_kb, 
        parse_mode="Markdown"
    )
    await save_message_id(state, bot_message.message_id)

    bot_message = await m.answer("Основные команды доступны на клавиатуре:", reply_markup=main_kb())
    await save_message_id(state, bot_message.message_id)

@dp.callback_query(F.data == "show_about_inline")
async def process_callback_about_inline(call: types.CallbackQuery, state: FSMContext):
    bot_message = await call.message.answer(ABOUT_TEXT, parse_mode="Markdown")
    await save_message_id(state, bot_message.message_id)
    await call.answer()

@dp.message(Command("help"))
async def help_command(m: types.Message, state: FSMContext):
    await save_message_id(state, m.message_id)
    bot_message = await m.answer(HELP_TEXT, reply_markup=main_kb(), parse_mode="Markdown")
    await save_message_id(state, bot_message.message_id)

@dp.message(F.text == "💡 О проекте")
async def about(m: types.Message, state: FSMContext):
    await save_message_id(state, m.message_id)
    bot_message = await m.answer(ABOUT_TEXT, reply_markup=main_kb(), parse_mode="Markdown")
    await save_message_id(state, bot_message.message_id)

@dp.message(F.text.contains("Начать тест"))
async def run_quiz(m: types.Message, state: FSMContext):
    await save_message_id(state, m.message_id)
    await state.set_state(Quiz.q1)
    await state.update_data(it=0, creative=0, social=0, logic=0, practice=0)
    bot_message = await m.answer(QUESTIONS[0], reply_markup=ans_kb())
    await save_message_id(state, bot_message.message_id)

@dp.message(F.text == "❌ Отменить тест")
async def cancel(m: types.Message, state: FSMContext):
    await save_message_id(state, m.message_id)
    await state.clear()
    bot_message = await m.answer("Тест отменен. Возвращаемся в главное меню.", reply_markup=main_kb())
    await save_message_id(state, bot_message.message_id)

@dp.message(F.text == "🗑️ Очистить чат")
async def clear_chat(m: types.Message, state: FSMContext):
    current_chat_id = m.chat.id
    
    await save_message_id(state, m.message_id) 

    data = await state.get_data()
    message_ids_to_delete = data.get('message_ids', [])
    
    deleted_count = 0
    for msg_id in message_ids_to_delete:
        try:
            await bot.delete_message(chat_id=current_chat_id, message_id=msg_id)
            deleted_count += 1
        except TelegramBadRequest as e:
            if "message to delete not found" not in str(e).lower() and "message can't be deleted" not in str(e).lower():
                print(f"Ошибка при удалении сообщения {msg_id}: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при удалении сообщения {msg_id}: {e}")

    await state.update_data(message_ids=[])

    bot_message = await m.answer(
        f"🗑️ Удалено {deleted_count} недавних сообщений. "
        "Сообщения старше 48 часов, а также те, что были отправлены *после* нажатия кнопки 'Очистить чат' (включая это сообщение), удалить невозможно.", 
        reply_markup=main_kb()
    )
    await save_message_id(state, bot_message.message_id)

@dp.message(F.text == "💬 Обратная связь")
async def feedback_entry(m: types.Message, state: FSMContext):
    await save_message_id(state, m.message_id)
    await state.set_state(Quiz.feedback_mode)
    bot_message = await m.answer(FEEDBACK_PROMPT, reply_markup=types.ReplyKeyboardRemove())
    await save_message_id(state, bot_message.message_id)

@dp.message(Quiz.feedback_mode)
async def process_feedback(m: types.Message, state: FSMContext):
    await save_message_id(state, m.message_id)

    if m.text == "❌ Отменить тест":
        await state.clear()
        bot_message = await m.answer("Ввод обратной связи отменен. Возвращаемся в главное меню.", reply_markup=main_kb())
        await save_message_id(state, bot_message.message_id)
        return

    feedback_text = m.text
    user_info = f"Пользователь {m.from_user.full_name} (@{m.from_user.username}, ID: {m.from_user.id})"
    
    try:
        await bot.send_message(
            chat_id=ADMIN_USER_ID,
            text=f"Новая обратная связь от {user_info}:\n\n{feedback_text}"
        )
    except Exception as e:
        print(f"Ошибка при отправке обратной связи админу (ID: {ADMIN_USER_ID}): {e}")

    bot_message = await m.answer(FEEDBACK_CONFIRMATION_USER, reply_markup=main_kb())
    await save_message_id(state, bot_message.message_id)
    await state.clear()

async def handle_answer(m: types.Message, state: FSMContext, next_state, q_idx):
    if m.text in ["❌ Отменить тест", "🗑️ Очистить чат", "💬 Обратная связь"]:
        return

    await save_message_id(state, m.message_id)

    data = await state.get_data()
    ans = m.text.upper()
    if ans == "А": data['it'] += 1
    elif ans == "Б": data['creative'] += 1
    elif ans == "В": data['social'] += 1
    elif ans == "Г": data['logic'] += 1
    elif ans == "Д": data['practice'] += 1
    else:
        bot_message = await m.answer("Пожалуйста, выберите один из вариантов (А, Б, В, Г, Д) или нажмите 'Отменить тест'/'Очистить чат'/'Обратная связь'.")
        await save_message_id(state, bot_message.message_id)
        return

    await state.update_data(data)
    if next_state:
        await state.set_state(next_state)
        bot_message = await m.answer(QUESTIONS[q_idx], reply_markup=ans_kb())
        await save_message_id(state, bot_message.message_id)
    else:
        scores = {"it": data['it'], "creative": data['creative'], "social": data['social'], "logic": data['logic'], "practice": data['practice']}
        winner = max(scores, key=scores.get)
        
        professions = {
            "it": "🔹 Программист\n🔹 Data Scientist\n🔹 Кибербезопасник\n🔹 DevOps\n🔹 Разработчик ИИ",
            "creative": "🔹 Геймдизайнер\n🔹 Режиссер монтажа\n🔹 Иллюстратор\n🔹 Арт-менеджер\n🔹 UI/UX дизайнер",
            "social": "🔹 Психолог\n🔹 HR-директор\n🔹 Тьютор\n🔹 Конфликтолог\n🔹 Врач-терапевт",
            "logic": "🔹 Финансовый аналитик\n🔹 Криминалист\n🔹 Математик\n🔹 Аудитор\n🔹 Инвест-банкир",
            "practice": "🔹 Инженер робототехники\n🔹 Архитектор\n🔹 Пилот\n🔹 Технолог\n🔹 Биоинженер"
        }
        
        results = {
            "it": "💻 *IT и Технологии*",
            "creative": "🎨 *Творчество и Медиа*",
            "social": "🤝 *Социум и Психология*",
            "logic": "📈 *Аналитика и Наука*",
            "practice": "🛠️ *Инженерия и Практика*"
        }

        try:
            bot_message = await m.answer_animation(PICTURES[winner])
            await save_message_id(state, bot_message.message_id)
        except Exception:
            pass

        bot_message = await m.answer(f"🏆 *Твой идеальный путь:* {results[winner]}\n\n*Рекомендуемые профессии:*\n{professions[winner]}", reply_markup=main_kb(), parse_mode="Markdown")
        await save_message_id(state, bot_message.message_id)
        await state.clear()

@dp.message(Quiz.q1)
async def p1(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q2, 1)
@dp.message(Quiz.q2)
async def p2(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q3, 2)
@dp.message(Quiz.q3)
async def p3(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q4, 3)
@dp.message(Quiz.q4)
async def p4(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q5, 4)
@dp.message(Quiz.q5)
async def p5(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q6, 5)
@dp.message(Quiz.q6)
async def p6(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q7, 6)
@dp.message(Quiz.q7)
async def p7(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q8, 7)
@dp.message(Quiz.q8)
async def p8(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q9, 8)
@dp.message(Quiz.q9)
async def p9(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q10, 9)
@dp.message(Quiz.q10)
async def p10(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q11, 10)
@dp.message(Quiz.q11)
async def p11(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q12, 11)
@dp.message(Quiz.q12)
async def p12(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q13, 12)
@dp.message(Quiz.q13)
async def p13(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q14, 13)
@dp.message(Quiz.q14)
async def p14(m: types.Message, state: FSMContext): await handle_answer(m, state, Quiz.q15, 14)
@dp.message(Quiz.q15)
async def p15(m: types.Message, state: FSMContext): await handle_answer(m, state, None, 0)


async def main():
    bot_info = await bot.get_me()
    print(f"--- Бот запущен! ---")
    print(f"Имя бота: {bot_info.first_name}")
    print(f"Username: @{bot_info.username}")
    print(f"--------------------")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
