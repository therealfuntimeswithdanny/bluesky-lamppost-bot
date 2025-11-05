# Lamppost Bluesky AI Image Bot

A simple Bluesky bot that listens for mentions of **`@lamppost.madebydanny.uk`**, generates an image using a Cloudflare Worker AI API, and replies back with the image.

Powered by:

* Python
* Cloudflare Worker/Lamppost API (Stable Diffusion)
* Bluesky Firehose streaming
* MBD CDN

---

## ✨ Features

✅ Listens for mentions on Bluesky
✅ Extracts the prompt from the post
✅ Calls Lamppost API `/api/generate`
✅ Uploads the image to Bluesky (altq.net)
✅ Replies with the generated image

---

## 📦 Requirements

Python 3.10+ recommended.

Install dependencies:

```bash
pip install atproto requests websockets python-dotenv
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```
BLUESKY_USERNAME=you.bsky.social
BLUESKY_PASSWORD=xxxx-xxxx-xxxx-xxxx
BOT_HANDLE=lamppost.madebydanny.uk
WORKER_URL=https://lamppost-api.madebydanny.uk/api/generate
```

> **Important:** The Bluesky password must be an **App Password**, not your main login.

You can generate one in:
**Bluesky → Settings → App Passwords**

---

## 🚀 Running the Bot

```bash
python bot.py
```

The bot will connect to the Bluesky firehose and start listening for mentions.

Leave the script running on a server, Raspberry Pi, or VPS.

---

## 🧠 Usage

Simply mention the bot with a prompt:

```
Make a cool futuristic city @lamppost.madebydanny.uk
```

The bot will reply with:

* A generated image
* The prompt used

---

## 🧰 Cloudflare Worker (AI Generator)

This bot expects your worker to return JSON:

```json
{ "url": "https://ai-cdn.madebydanny.uk/ai-content/image.png" }
```

The Worker stores images in R2 and returns MBD CDN URL.

---

## 🐳 Docker Support (Optional)

Add a Dockerfile:

```bash
docker build -t lamppost-bot .
docker run --env-file .env lamppost-bot
```

---

## 🔐 Security Tips

* Never commit your `.env` to GitHub
* Rotate app passwords occasionally
* Restrict generation limits if you go public

---

## 🤝 Contributing

Pull requests welcome!
You can add:

* Moderation filters
* Rate limits
* Better prompt parsing
* Admin commands

---

## 📄 License

MIT — free to use, modify, and deploy.

---
