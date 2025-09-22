import re
import time
from typing import Dict, List, Set
from telebot.types import Message

class SpamFilter:
    def __init__(self):
        # Спам-паттерны для криптовалютных мошенничеств
        self.crypto_spam_patterns = [
            r'(?i)airdrop.*live',
            r'(?i)private.*token.*airdrop',
            r'(?i)don\'t miss.*chance',
            r'(?i)only for.*group',
            r'(?i)free.*crypto',
            r'(?i)claim.*token',
            r'(?i)limited.*time.*offer',
            r'(?i)pump.*dump',
            r'(?i)guaranteed.*profit',
            r'(?i)invest.*bitcoin',
            r'(?i)double.*investment',
            r'(?i)earn.*daily',
            r'(?i)mining.*pool',
            r'(?i)wallet.*verification',
            r'(?i)seed.*phrase',
            r'(?i)recovery.*phrase',
        ]

        # Подозрительные ключевые слова
        self.suspicious_keywords = [
            'airdrop', 'token', 'crypto', 'bitcoin', 'ethereum', 'bnb',
            'usdt', 'doge', 'shib', 'pump', 'moon', '🚀', 'investment',
            'profit', 'earn', 'free money', 'bonus', 'reward', 'mining',
            'wallet', 'metamask', 'binance', 'exchange', 'trading'
        ]

        # Подозрительные домены
        self.suspicious_domains = [
            't.me',
            'bit.ly',
            'tinyurl.com',
            'telegram.me',
            'telegram.dog',
        ]

        # Отслеживание частоты сообщений по пользователям
        self.user_message_count: Dict[int, List[float]] = {}
        self.rate_limit_window = 60  # секунд
        self.max_messages_per_window = 10

        # Черный список пользователей
        self.blacklisted_users: Set[int] = set()

        # Белый список пользователей (админы, проверенные пользователи)
        self.whitelisted_users: Set[int] = set()

        # Админы бота (добавьте ваш user_id сюда)
        self.admin_users: Set[int] = {
            # 123456789,  # Замените на ваш user_id
        }

    def is_bot_message(self, message: Message) -> bool:
        """Проверяет, является ли сообщение от бота"""
        if message.from_user and message.from_user.is_bot:
            return True
        return False

    def is_spam_message(self, message: Message) -> bool:
        """Основная функция проверки спама"""
        if not message.text:
            return False

        text = message.text.lower()

        # Проверка криптовалютных спам-паттернов
        for pattern in self.crypto_spam_patterns:
            if re.search(pattern, text):
                return True

        # Подсчет подозрительных ключевых слов
        suspicious_word_count = sum(1 for keyword in self.suspicious_keywords if keyword in text)
        if suspicious_word_count >= 3:  # Если 3+ подозрительных слова
            return True

        # Проверка подозрительных ссылок
        if self.contains_suspicious_links(text):
            return True

        return False

    def contains_suspicious_links(self, text: str) -> bool:
        """Проверяет наличие подозрительных ссылок"""
        # Ищем ссылки в тексте
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)

        for url in urls:
            for domain in self.suspicious_domains:
                if domain in url:
                    return True

        # Проверка на t.me ссылки (кроме официальных каналов)
        if 't.me/' in text and 'GLORYTRADERS' not in text.upper():
            return True

        return False

    def is_rate_limited(self, user_id: int) -> bool:
        """Проверка превышения лимита сообщений"""
        current_time = time.time()

        if user_id not in self.user_message_count:
            self.user_message_count[user_id] = []

        # Удаляем старые записи
        self.user_message_count[user_id] = [
            timestamp for timestamp in self.user_message_count[user_id]
            if current_time - timestamp < self.rate_limit_window
        ]

        # Добавляем текущее сообщение
        self.user_message_count[user_id].append(current_time)

        # Проверяем лимит
        return len(self.user_message_count[user_id]) > self.max_messages_per_window

    def add_to_blacklist(self, user_id: int):
        """Добавляет пользователя в черный список"""
        self.blacklisted_users.add(user_id)

    def add_to_whitelist(self, user_id: int):
        """Добавляет пользователя в белый список"""
        self.whitelisted_users.add(user_id)

    def is_blacklisted(self, user_id: int) -> bool:
        """Проверяет, находится ли пользователь в черном списке"""
        return user_id in self.blacklisted_users

    def is_whitelisted(self, user_id: int) -> bool:
        """Проверяет, находится ли пользователь в белом списке"""
        return user_id in self.whitelisted_users

    def is_admin(self, user_id: int) -> bool:
        """Проверяет, является ли пользователь админом"""
        return user_id in self.admin_users

    def add_admin(self, user_id: int):
        """Добавляет пользователя в админы"""
        self.admin_users.add(user_id)
        self.add_to_whitelist(user_id)  # Админы автоматически в белом списке

    def should_ignore_message(self, message: Message) -> bool:
        """Главная функция фильтрации - определяет, нужно ли игнорировать сообщение"""
        if not message.from_user:
            return True

        user_id = message.from_user.id

        # Админы и белый список проходят все проверки
        if self.is_admin(user_id) or self.is_whitelisted(user_id):
            return False

        # Черный список блокируется
        if self.is_blacklisted(user_id):
            return True

        # Игнорируем сообщения от ботов
        if self.is_bot_message(message):
            return True

        # Проверяем на спам
        if self.is_spam_message(message):
            # Автоматически добавляем в черный список за спам
            self.add_to_blacklist(user_id)
            return True

        # Проверяем превышение лимита
        if self.is_rate_limited(user_id):
            return True

        return False

    def get_spam_reason(self, message: Message) -> str:
        """Возвращает причину блокировки сообщения (для логирования)"""
        if not message.from_user:
            return "No user info"

        user_id = message.from_user.id

        if self.is_blacklisted(user_id):
            return "User blacklisted"

        if self.is_bot_message(message):
            return "Bot message"

        if self.is_spam_message(message):
            return "Spam content detected"

        if self.is_rate_limited(user_id):
            return "Rate limited"

        return "Unknown"

# Глобальный экземпляр фильтра
spam_filter = SpamFilter()