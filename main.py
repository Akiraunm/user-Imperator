from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '7517468931:AAF1o3lDyMhFI5Gye7yB3YiOWAO02BtuJvw'

computers = {}

def generate_computers():
    global computers
    id_counter = 1

    for _ in range(80):
        computers[id_counter] = {
            "photo": "https://braintwister.design/uploads/posts/2018-05/1527064497_004.jpg",
            "price": "800 тг/час",
            "category": "Общий зал"
        }
        id_counter += 1

    for _ in range(30):
        computers[id_counter] = {
            "photo": "https://request.ru/wp-content/uploads/2021/05/2021-05-29_17-54-52.png",
            "price": "1200 тг/час",
            "category": "Сильвер"
        }
        id_counter += 1

    for _ in range(10):
        computers[id_counter] = {
            "photo": "https://p1.zoon.ru/preview/VxYSbkv3V-DSbBnIQVUnOw/630x384x85/1/5/e/original_5fabe102cabcc704fc13e642_64954d5e19e959.30207577.jpg",
            "price": "1500 тг/час",
            "category": "VIP"
        }
        id_counter += 1

generate_computers()

admin_phone = "+77789798674"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Номер компьютера", callback_data="show_computers")],
        [InlineKeyboardButton("Стоимость", callback_data="show_prices")],
        [InlineKeyboardButton("Номер администратора", callback_data="show_admin")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет, добро пожаловать в компьютерный клуб, user: Imperator!", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        if query.data == "show_computers":
            keyboard = [
                [InlineKeyboardButton("Общий зал", callback_data="category_Общий зал")],
                [InlineKeyboardButton("Сильвер", callback_data="category_Сильвер")],
                [InlineKeyboardButton("VIP", callback_data="category_VIP")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("Выберите категорию:", reply_markup=reply_markup)

        elif query.data.startswith("category_"):
            category = query.data.split("_")[1]
            filtered_computers = {k: v for k, v in computers.items() if v["category"] == category}

            keyboard = []
            comp_ids = list(filtered_computers.keys())
            for i in range(0, len(comp_ids), 5):
                row = [InlineKeyboardButton(f"{comp_ids[j]}", callback_data=f"computer_{comp_ids[j]}") for j in range(i, min(i+5, len(comp_ids)))]
                keyboard.append(row)

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"Категория: {category}\nВыберите номер компьютера:", reply_markup=reply_markup)

        elif query.data.startswith("computer_"):
            comp_id = int(query.data.split("_")[1])
            if comp_id in computers:
                keyboard = [
                    [InlineKeyboardButton("Фото", callback_data=f"photo_{comp_id}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await query.edit_message_text(
                    f"Компьютер {comp_id} ({computers[comp_id]['category']}): {computers[comp_id]['price']}",
                    reply_markup=reply_markup
                )
            else:
                if query.message:
                    await query.message.reply_text("Ошибка: Компьютер не найден.")

        elif query.data.startswith("photo_"):
            comp_id = int(query.data.split("_")[1])
            if comp_id in computers:
                await query.message.reply_photo(
                    photo=computers[comp_id]["photo"],
                    caption=f"Компьютер {comp_id} ({computers[comp_id]['category']})"
                )
            else:
                if query.message:
                    await query.message.reply_text("Ошибка: Компьютер не найден.")

        elif query.data == "show_prices":
            price_summary = {
                "Общий зал 800 тг/час": 0,
                "Сильвер 1200 тг/час": 0,
                "VIP 1500 тг/час": 0,
            }
            for comp in computers.values():
                price_summary[f"{comp['category']} {comp['price']}"] += 1
            prices = "\n".join([f"{price}" for price in price_summary.keys()])
            await query.edit_message_text(f"Стоимость:\n{prices}")

        elif query.data == "show_admin":
            await query.edit_message_text(f"Связаться с администратором: {admin_phone}")

    except Exception as e:
        if query.message:
            await query.message.reply_text(f"Произошла ошибка: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))

    app.run_polling()

if __name__ == "__main__":
    main()
