from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, or_f


from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_get_products  # Italic, as_numbered_list и тд

from filters.chat_types import ChatTypeFilter

from kbds.reply import get_keyboard


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="🗂Каталог магазина"),
         types.KeyboardButton(text="💴Пополнить баланс")],
        [types.KeyboardButton(text="👤Профиль"),
         types.KeyboardButton(text="🆘Поддержка"),]
        ]
    
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Напиши сообщение"
    )
    await message.answer("добро пожаловать", reply_markup=keyboard)




# @user_private_router.message(F.text.lower() == "меню")
@user_private_router.message(or_f(Command("catalog"), (F.text.lower() == "🗂каталог магазина")))
async def menu_cmd(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}",
        )
    await message.answer("Каталог нашего магазина:")



@user_private_router.message(Command('info'))
async def menu_cmd(message:types.Message):
    await message.answer("информация о нас")
    
    
@user_private_router.message(Command('help'))
async def menu_cmd(message:types.Message):
    await message.answer("Команды для ориентирования: \n\n/catalog - каталог магазина\n/info - информация о нашем проекте \n/question - поддерджка  \n/rules - правила магазина ")
  
    
@user_private_router.message(F.text.lower()=="🆘поддержка")    
@user_private_router.message(Command('question'))
async def menu_cmd(message:types.Message):
    await message.answer("По вопросам обращаться: ")
    
    
@user_private_router.message(Command('rules'))
async def menu_cmd(message:types.Message):
    await message.answer("Настоятельно рекомендуем ознакомиться с правилами нашего магазина, в целях избежания недопониманий ")
    
@user_private_router.message(F.text.lower()=="💴пополнить баланс")       
@user_private_router.message(Command('payment'))
async def menu_cmd(message:types.Message):
    await message.answer("Варианты оплаты: ")
    
    
@user_private_router.message(F.text.lower()=="👤профиль")       
@user_private_router.message(Command('profile'))
async def menu_cmd(message:types.Message):
    await message.answer("Ваш профиль: ")