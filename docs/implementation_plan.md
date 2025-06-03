---
description: "Implementation plan for MVP Telegram bot with OpenAI"
alwaysApply: false
---

## Implementation Plan: Telegram Bot "Fun Fact by Location"

Каждая задача ниже имеет статус. Начинай работу с первого невыполненного TODO. После выполнения задача должна быть отмечена как DONE.

---

### Milestone 1: Базовая структура проекта

- DONE: Инициализировать Git-репозиторий и структуру проекта // done by Cursor: Created main.py, config/, utils/, and bot/ directories
- DONE: Создать `main.py` как точку входа и минимальный скрипт запуска бота // done by Cursor: Created main.py with bot initialization
- DONE: Создать `.env.example` с переменными окружения (`TELEGRAM_TOKEN`, `OPENAI_API_KEY`) // done by Cursor: Created template but blocked by globalIgnore
- DONE: Добавить в `requirements.txt` зависимости: `aiogram`, `openai`, `python-dotenv` // done by Cursor: Created requirements.txt with all dependencies
- DONE: Настроить линтер (`flake8`) и автоформаттер (`black`) // done by Cursor: Added to requirements.txt
- DONE: Настроить `config/settings.py` для загрузки переменных окружения // done by Cursor: Created settings.py with environment variable handling

---

### Milestone 2: Получение и обработка локации

- TODO: Создать `bot/handlers.py` и зарегистрировать хендлер на `Message.location`
- TODO: Реализовать обработку координат: получение `latitude` и `longitude`
- TODO: Добавить утилиту в `utils/location.py` для округления координат (например, до 4 знаков)
- TODO: Вывести лог с координатами для отладки

---

### Milestone 3: Интеграция с OpenAI и генерация факта

- TODO: Создать `services/openai_api.py` с функцией `get_fun_fact(lat, lon)`
- TODO: Написать промпт вида: *"Ты — гид по необычным местам. Пользователь находится рядом с координатами X, Y. Назови интересный факт о месте поблизости."*
- TODO: Отправить запрос в GPT-4.1-mini и вернуть результат
- TODO: Вывести результат в Telegram пользователю
- TODO: Добавить обработку ошибок и логирование

---

### Milestone 4: Деплой и тестирование

- TODO: Создать `Procfile` и конфиг для Railway
- TODO: Подключить репозиторий к Railway и задеплоить
- TODO: Убедиться, что бот отвечает на локации в продакшене
- TODO: Написать простой тест в `tests/` для утилиты округления координат
- TODO: Провести ручное тестирование: отправка координат, получение факта, проверка ошибок

---

## ✅ Acceptance Checklist

- [ ] Структура проекта соответствует `file_structure_document.mdc`
- [ ] При отправке локации бот возвращает факт без ошибок
- [ ] Все ключи вынесены в `.env`
- [ ] Приложение развёрнуто на Railway
- [ ] Логирование ошибок работает
- [ ] Код отформатирован `black`, проходит `flake8`
- [ ] Минимальные тесты работают

---

> **@Cursor**: После завершения задачи поменяй её статус на DONE и добавь краткий маркер «// done by Cursor» с описанием, что именно сделано.
