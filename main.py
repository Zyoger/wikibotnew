import logging, wikipedia, re
from telegram import __version__ as TG_VER

wikipedia.set_lang("ru")

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import Update
from telegram.ext import Application, filters, CommandHandler, ContextTypes, MessageHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введи слово для поиска по Wikipedia. Случайная статья /random"
    )


async def article(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if getwiki(update.message.text) == False:
        await update.message.reply_text("Такой статьи нет в Wikipedia :(")
    else:
        await update.message.reply_text(getwiki(update.message.text))


async def randarticle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    link = ("https://ru.wikipedia.org/wiki/" + wikipedia.random(pages=1))
    await update.message.reply_text(link.replace(' ', '_'))


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not ('==' in x):
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2
    except Exception as e:
        return False


def main() -> None:
    application = Application.builder().token("token").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, article))
    application.add_handler(CommandHandler("random", randarticle))
    application.run_polling()


if __name__ == "__main__":
    main()
