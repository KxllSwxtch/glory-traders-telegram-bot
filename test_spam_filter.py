#!/usr/bin/env python3
"""
Тестирование спам-фильтра
"""

from spam_filter import SpamFilter
from telebot.types import Message, User


def create_test_message(text: str, user_id: int = 12345, is_bot: bool = False):
    """Создает тестовое сообщение"""
    message = Message(
        message_id=1,
        from_user=User(id=user_id, is_bot=is_bot, first_name="Test"),
        date=1234567890,
        chat=None,
        content_type="text",
        options={},
        json_string=""
    )
    message.text = text
    return message


def test_spam_filter():
    """Тестирует спам-фильтр"""
    filter_instance = SpamFilter()

    print("🔍 Тестирование спам-фильтра...")
    print()

    # Тест 1: Сообщения от ботов
    print("1. Тест сообщений от ботов:")
    bot_message = create_test_message("Привет!", user_id=99999, is_bot=True)
    result = filter_instance.should_ignore_message(bot_message)
    print(f"   Сообщение от бота: {'ЗАБЛОКИРОВАНО' if result else 'ПРОПУЩЕНО'} ✅" if result else " ❌")

    # Тест 2: Криптовалютный спам
    print("\n2. Тест криптовалютного спама:")
    spam_messages = [
        "🚀 Private FOXY token airdrop is LIVE! Only for this group 👉 t.me/FOXYLOYAL. Don't miss your chance!",
        "FREE BITCOIN AIRDROP! Claim now: t.me/scamgroup",
        "Guaranteed profit! Double your investment in 24 hours!",
        "Join our mining pool for free tokens",
    ]

    for spam_text in spam_messages:
        message = create_test_message(spam_text, user_id=12345)
        result = filter_instance.should_ignore_message(message)
        print(f"   '{spam_text[:50]}...': {'ЗАБЛОКИРОВАНО' if result else 'ПРОПУЩЕНО'} {'✅' if result else '❌'}")

    # Тест 3: Нормальные сообщения
    print("\n3. Тест нормальных сообщений:")
    normal_messages = [
        "Привет, хочу рассчитать стоимость автомобиля",
        "/start",
        "Расчёт",
        "https://encar.com/some-car-listing",
        "Спасибо за помощь!",
    ]

    for normal_text in normal_messages:
        message = create_test_message(normal_text, user_id=54321)
        result = filter_instance.should_ignore_message(message)
        print(f"   '{normal_text}': {'ЗАБЛОКИРОВАНО' if result else 'ПРОПУЩЕНО'} {'❌' if result else '✅'}")

    # Тест 4: Белый список
    print("\n4. Тест белого списка:")
    filter_instance.add_to_whitelist(99999)
    whitelisted_message = create_test_message("🚀 Even spam from whitelisted user", user_id=99999)
    result = filter_instance.should_ignore_message(whitelisted_message)
    print(f"   Спам от пользователя в белом списке: {'ЗАБЛОКИРОВАНО' if result else 'ПРОПУЩЕНО'} {'❌' if result else '✅'}")

    # Тест 5: Черный список
    print("\n5. Тест черного списка:")
    filter_instance.add_to_blacklist(11111)
    blacklisted_message = create_test_message("Нормальное сообщение", user_id=11111)
    result = filter_instance.should_ignore_message(blacklisted_message)
    print(f"   Нормальное сообщение от заблокированного: {'ЗАБЛОКИРОВАНО' if result else 'ПРОПУЩЕНО'} {'✅' if result else '❌'}")

    # Тест 6: Rate limiting
    print("\n6. Тест ограничения частоты сообщений:")
    test_user_id = 77777
    for i in range(12):  # Отправляем больше лимита (10)
        message = create_test_message(f"Сообщение {i+1}", user_id=test_user_id)
        result = filter_instance.should_ignore_message(message)
        if i < 10:
            print(f"   Сообщение {i+1}: {'ЗАБЛОКИРОВАНО' if result else 'ПРОПУЩЕНО'} {'❌' if result else '✅'}")
        else:
            print(f"   Сообщение {i+1} (превышение лимита): {'ЗАБЛОКИРОВАНО' if result else 'ПРОПУЩЕНО'} {'✅' if result else '❌'}")

    print("\n🎉 Тестирование завершено!")


if __name__ == "__main__":
    test_spam_filter()