# Copyright (c) 2025 Matvii Jarosh
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from MK_ROBOT1000 import *

BOT_TOKEN = '7987119484:AAGXYvNMCDZsBatbahxBK3O_OMWJ-Y6lehA'


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        text = update.message.text
        bad_words = check_sentence_for_bad_words(text)

        if bad_words:
            reply_lines = ["🚫 *Знайдено погані слова!*"]

            for original_word, bad_word_matched, severity in bad_words:
                line = f"• `{original_word}` → схоже на `{bad_word_matched}` (⚠️ рівень {severity})"
                reply_lines.append(line)

            reply_text = "\n".join(reply_lines)

            await update.message.reply_text(
                reply_text,
                parse_mode="Markdown"
            )


if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))

    print("Бот запущено!")
    app.run_polling()
