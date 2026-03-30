# MusicUncensor

Приложение для скачивания расцензуренных версий треков из Spotify.

(**Приложение не будет работать без "ускорителя интернета"**)
---

## 🚀 Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/ADVENCHER4/MusicUncensor.git
cd MusicUncensor
```

---

### 2. Создание виртуального окружения

```bash
python -m venv venv
```

Активация:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

---

### 3. Установка зависимостей

```bash
python -m pip install -r requirements.txt
```

---

## ⚙️ Настройка Spotify API

Для работы приложения необходимо создать приложение в Spotify for Developers. (**Не будет работать без "ускорителя интернета"**)

---

### 1. Создание приложения

1. Перейди на Spotify for Developers
2. Войди в свой аккаунт Spotify
3. Нажми **"Create App"**
4. Заполни:

   * **App name** — любое название
   * **App description** — описание (можно любое)

---

### 2. Получение данных

После создания ты получишь:

* `Client ID`
* `Client Secret`

---

### 3. Настройка Redirect URI

В настройках приложения добавь:

```text
https://127.0.0.1/callback
```

---

### 4. Заполнение конфигурационного файла

При первом запуске приложение создаст файл настроек.

Заполни его:

```ini
[SPOTIFY]
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
REDIRECT_URI=https://127.0.0.1/callback
SCOPE=user-library-read

[OS]
FOLDER_PATH=./songs
```

---

## ▶️ Запуск

```bash
python main.py
```
