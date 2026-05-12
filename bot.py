import os
import logging
import random
import requests
from urllib.parse import quote
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, filters, ContextTypes
)

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

# ─────────────────────────────────────────────
#  CINEMATIC STYLES
# ─────────────────────────────────────────────
STYLES = {
    "epic": {
        "label": "⚡ Epic Blockbuster",
        "suffix": (
            "epic cinematic scene, dramatic stormy sky, god rays, "
            "ultra-wide angle lens, IMAX quality, Hollywood blockbuster, "
            "explosive atmosphere, 8K ultra HD, award-winning cinematography"
        ),
    },
    "noir": {
        "label": "🌑 Dark Noir",
        "suffix": (
            "dark noir cinematic, deep shadows, high contrast, "
            "rain-soaked streets, moody atmosphere, 1940s film noir, "
            "chiaroscuro lighting, black and white with subtle tones"
        ),
    },
    "golden": {
        "label": "🌅 Golden Hour",
        "suffix": (
            "golden hour magic, warm amber light, lens flare, "
            "bokeh background, soft cinematic glow, dreamlike atmosphere, "
            "filmic grain, Kodak Portra 400 color grading"
        ),
    },
    "scifi": {
        "label": "🚀 Sci-Fi Futuristic",
        "suffix": (
            "sci-fi cinematic, neon lights, cyberpunk city, "
            "holographic elements, futuristic technology, deep space background, "
            "volumetric fog, Blade Runner 2049 aesthetic, ultra realistic"
        ),
    },
    "fantasy": {
        "label": "🧙 Epic Fantasy",
        "suffix": (
            "fantasy cinematic, magical realm, ethereal lighting, "
            "ancient ruins, mystical creatures, particle effects, "
            "Lord of the Rings scale, breathtaking landscape, epic scope"
        ),
    },
    "horror": {
        "label": "👁️ Psychological Horror",
        "suffix": (
            "horror cinematic, eerie atmosphere, fog and mist, "
            "isolated location, ominous shadows, unsettling composition, "
            "desaturated color palette, suspenseful mood"
        ),
    },
    "romance": {
        "label": "💫 Cinematic Romance",
        "suffix": (
            "romantic cinematic moment, soft warm bokeh, "
            "pastel color grading, emotional depth, intimate composition, "
            "dreamy atmosphere, shallow depth of field, film photography"
        ),
    },
    "war": {
        "label": "💥 War Epic",
        "suffix": (
            "war epic cinematic, battlefield atmosphere, "
            "smoke and dust, dramatic action, desaturated tones, "
            "Saving Private Ryan realism, intense composition, 4K gritty detail"
        ),
    },
}

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def style_keyboard():
    buttons = []
    items = list(STYLES.items())
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i][1]["label"], callback_data=f"style_{items[i][0]}")]
        if i + 1 < len(items):
            row.append(InlineKeyboardButton(items[i + 1][1]["label"], callback_data=f"style_{items[i + 1][0]}"))
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)

def build_image_url(prompt: str, style_key: str = "epic") -> str:
    style = STYLES.get(style_key, STYLES["epic"])
    full_prompt = f"{prompt}, {style['suffix']}"
    seed = random.randint(1, 999999)
    encoded = quote(full_prompt)
    return (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width=1920&height=1080&model=flux&seed={seed}&nologo=true&enhance=true"
    )

# ─────────────────────────────────────────────
#  COMMANDS
# ─────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name or "Creator"
    text = (
        f"✦ ✦ ✦  C I N E M A T I C  A I  ✦ ✦ ✦\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Welcome, {user}. 🎬\n\n"
        f"You've entered the world's most powerful\n"
        f"FREE cinematic image generator.\n\n"
        f"🔥  Powered by FLUX AI Model\n"
        f"🎥  Hollywood-grade visual output\n"
        f"⚡  Instant generation · No cost · No limits\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"HOW TO USE:\n\n"
        f"① Type /style → Choose your cinematic style\n"
        f"② Describe your scene in words\n"
        f"③ Receive your masterpiece\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📽️  EXAMPLE PROMPTS:\n\n"
        f'▸ "A lone warrior standing in the rain"\n'
        f'▸ "Futuristic city at midnight"\n'
        f'▸ "Ancient temple swallowed by jungle"\n'
        f'▸ "A girl watching the sunset on a cliff"\n\n'
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Type /style to choose your style & start creating ✨"
    )
    await update.message.reply_text(text)


async def style_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🎨  CHOOSE YOUR CINEMATIC STYLE\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Select the mood & genre below.\n"
        "Your chosen style will apply to every image\n"
        "until you switch it again.\n\n"
        "👇  Tap to select:"
    )
    await update.message.reply_text(text, reply_markup=style_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖  CINEMATIC AI — HELP CENTER\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "COMMANDS:\n"
        "▸ /start    →  Welcome screen\n"
        "▸ /style    →  Choose cinematic style\n"
        "▸ /current  →  See your active style\n"
        "▸ /help     →  This help menu\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "PRO TIPS FOR BEST RESULTS:\n\n"
        "✔  Be specific with your scene description\n"
        "✔  Mention time of day (dawn, midnight, dusk)\n"
        "✔  Add emotions (lonely, triumphant, peaceful)\n"
        "✔  Include environment details\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "EXAMPLE (Detailed):\n"
        '"A lone detective standing under a flickering\n'
        ' streetlamp on a rainy cobblestone street,\n'
        ' cigarette smoke curling into the cold air"\n\n'
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "The more detail you give → the better the image ✨"
    )
    await update.message.reply_text(text)


async def current_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
    style_key = context.user_data.get("style", "epic")
    style = STYLES[style_key]
    text = (
        f"🎬  YOUR ACTIVE STYLE\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Current: {style['label']}\n\n"
        f"Type /style to switch styles ✦"
    )
    await update.message.reply_text(text)


# ─────────────────────────────────────────────
#  CALLBACK — Style selection
# ─────────────────────────────────────────────
async def style_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    style_key = query.data.replace("style_", "")
    context.user_data["style"] = style_key
    style = STYLES.get(style_key, STYLES["epic"])
    text = (
        f"✅  STYLE ACTIVATED\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{style['label']}\n\n"
        f"Your images will now be generated\n"
        f"in this cinematic style.\n\n"
        f"Now describe your scene and I'll\n"
        f"create your masterpiece. 🎬✨"
    )
    await query.edit_message_text(text)


# ─────────────────────────────────────────────
#  MESSAGE — Generate image
# ─────────────────────────────────────────────
async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text.strip()
    style_key = context.user_data.get("style", "epic")
    style = STYLES[style_key]

    loading_msg = await update.message.reply_text(
        f"⚙️  GENERATING YOUR MASTERPIECE\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Style:  {style['label']}\n"
        f"Scene:  {user_prompt[:60]}{'...' if len(user_prompt) > 60 else ''}\n\n"
        f"⏳ Processing with FLUX AI...\n"
        f"This may take 15–30 seconds."
    )

    image_url = build_image_url(user_prompt, style_key)

    try:
        response = requests.get(image_url, timeout=120)
        if response.status_code == 200:
            caption = (
                f"✦  CINEMATIC AI  ✦\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🎬  Style: {style['label']}\n"
                f"📝  Scene: {user_prompt[:80]}{'...' if len(user_prompt) > 80 else ''}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"⚡ Powered by FLUX AI Model\n"
                f"🔁 Send another description to create more ✨"
            )
            await update.message.reply_photo(
                photo=response.content,
                caption=caption
            )
        else:
            await update.message.reply_text(
                "❌  GENERATION FAILED\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "The AI server returned an error.\n"
                "Please try again with a different description."
            )
    except requests.exceptions.Timeout:
        await update.message.reply_text(
            "⏱️  REQUEST TIMED OUT\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "The server is busy right now.\n"
            "Please wait 10 seconds and try again."
        )
    except Exception as e:
        logger.error(f"Image generation error: {e}")
        await update.message.reply_text(
            "⚠️  UNEXPECTED ERROR\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Something went wrong on our end.\n"
            "Please try again shortly."
        )
    finally:
        try:
            await loading_msg.delete()
        except Exception:
            pass


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("style", style_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("current", current_style))
    app.add_handler(CallbackQueryHandler(style_callback, pattern="^style_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    logger.info("✦ Cinematic AI Bot is running...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
  
