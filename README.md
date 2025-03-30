# SMS Gateway CLI

CLI HTTP-клиента для отправки sms-сообщений

# Установка

1. Клонируйте репозиторий и перейдите в него
```bash
git clone https://github.com/prNikson/python-test
cd python-test
```

2. Для проверки можно использовать mock-сервер prism (https://github.com/stoplightio/prism/releases)
```bash
prism-cli-linux mock sms-platform.yaml 
```

3. Для запуска понадобится установка одной внешней библиотеки toml:
```bash
pip install toml
```
4. Запустите программу
```bash
cd src
python main.py sender recepient message
```
В репозитории две ветки:
1. Клиент, реализованный на socket -> ветка master
2. Клиент, реализованный на asyncio -> ветка asyncio_version