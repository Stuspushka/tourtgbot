from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🗓 Однодневки")],
        [KeyboardButton(text="📆 Группы")],
    ],
    resize_keyboard=True
)

oneday_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить однодневку")],
        [KeyboardButton(text="✏️ Обновить однодневку")],
        [KeyboardButton(text="🗑 Удалить однодневку")],
        [KeyboardButton(text="📋 Показать однодневки")],
        [KeyboardButton(text="🔙 Назад в меню")]
    ],
    resize_keyboard=True
)

longtour_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Добавить группу")],
        [KeyboardButton(text="✏️ Редактировать группу")],
        [KeyboardButton(text="🗑 Удалить группу")],
        [KeyboardButton(text="📋 Показать группы")],
        [KeyboardButton(text="🔙 Назад в меню")]
    ],
    resize_keyboard=True
)

cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True,
    one_time_keyboard=True
)

confirm_longtour_delete_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_delete"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_delete")
        ]
    ]
)

confirm_oneday_delete_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_oneday_delete"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_oneday_delete")
        ]
    ]
)

def edit_oneday_fields_keyboard(booking_id: str) -> InlineKeyboardMarkup:
    editable_fields = {
        "fio": "👤 ФИО",
        "phone": "📞 Телефон",
        "operator": "🏢 Оператор",
        "direction": "📍 Направление",
        "date": "📅 Дата тура",
        "paydate": "💳 Дата доплаты"
    }

    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"edit_oneday:{field}:{booking_id}")]
        for field, label in editable_fields.items()
    ]
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_edit")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def edit_longtour_fields_keyboard(name: str) -> InlineKeyboardMarkup:
    editable_fields = {
        "customer": "👤 Клиент",
        "phone": "📞 Телефон",
        "direction": "🧭 Направление",
        "p_count": "👥 Кол-во",
        "bus": "🚌 Автобус",
        "locations": "📍 Места",
        "date": "📅 Дата тура",
        "total": "💰 Сумма"
    }

    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"edit_longtour:{field}:{name}")]
        for field, label in editable_fields.items()
    ]

    buttons.append([
        InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_longtour_edit")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)