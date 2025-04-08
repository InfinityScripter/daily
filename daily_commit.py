#!/usr/bin/env python3

import os
import datetime
import random
import subprocess
import time

# Конфигурация
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(REPO_PATH, 'data.txt')

def run_command(command):
    """Выполнить команду и вернуть результат"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('utf-8').strip(), stderr.decode('utf-8').strip(), process.returncode

def make_commit():
    """Создать коммит с текущей датой"""
    # Получаем текущую дату и время
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Создаем или обновляем файл с данными
    with open(DATA_FILE, 'a') as f:
        f.write(f"Обновление от {timestamp}\n")
    
    # Добавляем файл в git
    stdout, stderr, code = run_command(f"cd {REPO_PATH} && git add {DATA_FILE}")
    if code != 0:
        print(f"Ошибка при добавлении файла: {stderr}")
        return False
    
    # Создаем коммит
    commit_message = f"Ежедневное обновление {timestamp}"
    stdout, stderr, code = run_command(f"cd {REPO_PATH} && git commit -m \"{commit_message}\"")
    if code != 0:
        print(f"Ошибка при создании коммита: {stderr}")
        return False
    
    # Отправляем изменения в удаленный репозиторий
    stdout, stderr, code = run_command(f"cd {REPO_PATH} && git push")
    if code != 0:
        print(f"Ошибка при отправке изменений: {stderr}")
        return False
    
    print(f"Успешно создан коммит: {commit_message}")
    return True

def main():
    # Проверяем, настроен ли удаленный репозиторий
    stdout, stderr, code = run_command(f"cd {REPO_PATH} && git remote -v")
    if not stdout:
        print("Удаленный репозиторий не настроен. Пожалуйста, настройте его вручную:")
        print("git remote add origin https://github.com/InfinityScripter/daily.git")
        return
    
    # Делаем коммит
    make_commit()

if __name__ == "__main__":
    main()