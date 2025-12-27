# page_analyzer

## Статус

[![Actions Status](https://github.com/SlowKingg/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/SlowKingg/python-project-83/actions)
[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=SlowKingg_python-project-83)](https://sonarcloud.io/summary/new_code?id=SlowKingg_python-project-83)


[Деплой](https://python-project-83-yg5l.onrender.com)

## Описание

Page Analyzer — небольшое веб-приложение на Flask, которое сохраняет переданные URL, запускает их проверки и хранит результаты. При проверке оно забирает HTTP-код ответа, заголовок страницы, первый заголовок `h1` и содержимое мета-тега `description`, чтобы быстро оценить базовую SEO-подготовку страницы. Данные сохраняются в PostgreSQL, последние проверки видны в интерфейсе.

## Технологии

- Flask + Gunicorn
- PostgreSQL (через psycopg2)
- Requests и BeautifulSoup4 для скачивания и парсинга страниц
- Babel для i18n
- Ruff для линтинга

## Как запустить локально

1. Установите зависимости: `make install` (используется uv).
2. Задайте переменную окружения `DATABASE_URL` (например, в `.env`) вида `postgresql://USER:PASSWORD@HOST:PORT/DBNAME`.
3. Инициализируйте базу: `make db-init` (использует `database.sql`).
4. Запустите dev-сервер: `make dev` и откройте `http://localhost:5000`.

## Запуск в продакшене

- Выполните `make start PORT=8000` для запуска Gunicorn локально.
- Для Render используется `make render-start`; переменные окружения должны быть заданы на стороне хостинга.
