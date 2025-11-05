import os
import re
import io
import requests
from dotenv import load_dotenv
from atproto import Client, firehose

# === Load secrets ===
load_dotenv()

BOT_HANDLE = os.getenv("BOT_HANDLE")
WORKER_URL = os.getenv("WORKER_URL")
BLUESKY_USERNAME = os.getenv("BLUESKY_USERNAME")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")

if not all([BOT_HANDLE, WORKER_URL, BLUESKY_USERNAME, BLUESKY_PASSWORD]):
    raise SystemExit("❌ Missing environment variables in .env")

client = Client()
client.login(BLUESKY_USERNAME, BLUESKY_PASSWORD)

mention_regex = re.compile(rf"@{re.escape(BOT_HANDLE)}", re.IGNORECASE)

def generate_image(prompt: str):
    """Send prompt to worker and download png."""
    r = requests.post(WORKER_URL, json={"prompt": prompt})
    r.raise_for_status()

    img_url = r.json()["url"]
    img = requests.get(img_url)
    return img.content

def on_event(evt):
    if not isinstance(evt, firehose.models.AppBskyFeedPost):
        return

    post = evt
    text = post.record.text

    # Not mentioning us? Ignore
    if not mention_regex.search(text):
        return

    # Prompt = everything except mention
    prompt = mention_regex.sub("", text).strip()
    if not prompt:
        return

    print(f"✨ Generating image for prompt: {prompt}")

    try:
        img_bytes = generate_image(prompt)

        blob = client.upload_blob(io.BytesIO(img_bytes), "image/png")

        # Reply with image
        client.send_post(
            text=f"Here you go!\nPrompt: {prompt}",
            reply_to=post.uri,
            embed=client.models.AppBskyEmbedImages.Main(
                images=[
                    client.models.AppBskyEmbedImages.Image(
                        image=blob.blob,
                        alt=f"A generated image for: {prompt}",
                    )
                ]
            ),
        )
    except Exception as e:
        print(f"❌ Failed: {e}")

print(f"✅ Bot listening for @{BOT_HANDLE}...")
xrpc = firehose.FirehoseSubscribeRepos(on_event)
xrpc.start()
