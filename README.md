# homework-selenium <!-- omit from toc -->

- [1. Установка зависимостей](#1-установка-зависимостей)
- [2. Запуск тестов](#2-запуск-тестов)

## 1. Установка зависимостей

Чтобы установить все зависимости используйте команду:

```bash
pip install -r requirements.txt
```

## 2. Запуск тестов

> [!IMPORTANT]  
> Для тестов обязательно использовать `Google Chrome`.
> Перед первым запуском тестов необходимо будет вручную авторизоваться в VK ID. Для этого используйте команду:

```bash
make auth
```

Данные авторизации будут сохранены локально в cookies.

Для повторных запусков тестов используйте команду:

```bash
make test
```

Для запуска только последних упавших тестов, используйте команду:

```bash
make test-failed
```

Для корректной работы в вашем аккаунте:

- не должно быть созданных лид-форм
