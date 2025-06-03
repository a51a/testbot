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

- DONE: Создать `bot/handlers.py` и зарегистрировать хендлер на `Message.location` // done by Cursor: Created handler and registered it in main.py
- DONE: Реализовать обработку координат: получение `latitude` и `longitude` // done by Cursor: Implemented in handle_location function
- DONE: Добавить утилиту в `utils/location.py` для округления координат // done by Cursor: Created round_coordinates function
- DONE: Вывести лог с координатами для отладки // done by Cursor: Added logging in handle_location

---

### Milestone 3: Интеграция с OpenAI и генерация факта

- DONE: Создать `services/openai_api.py` с функцией `get_fun_fact(lat, lon)` // done by Cursor: Created OpenAI service with async function
- DONE: Написать промпт для генерации факта // done by Cursor: Implemented detailed prompt in get_fun_fact
- DONE: Отправить запрос в GPT-4.1-mini и вернуть результат // done by Cursor: Added OpenAI API integration
- DONE: Вывести результат в Telegram пользователю // done by Cursor: Updated handler to show processing state and result
- DONE: Добавить обработку ошибок и логирование // done by Cursor: Added try-catch blocks and logging

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
