import requests as r 

from OnePieceBot import SUPPORT_CHAT, WEBSS_API, dispatcher
from OnePieceBot.modules.disable import DisableAbleCommandHandler
import OnePieceBot.modules.reverse as REVERSE_MOD
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, run_async

@run_async
def web_ss(update: Update, context: CallbackContext):
  chat_id = update.effective_chat.id
  msg = update.effective_message
  msg_id = update.effective_message.message_id
  args = context.args
  bot = context.bot
  query = " ".join(args)
  if not query:
    msg.reply_text("Please enter a url query to take a screenshot")
    return
  else:
    rep = msg.reply_text(
      "<code>Generating...</code>", parse_mode=ParseMode.HTML)
    res = r.get(
      f"https://screenshotapi.net/api/v1/screenshot?token={WEBSS_API}&url={query}&full_page=true&output=json&fail_on_error=true"
    ).json()
    #print(res)
    if not res.get("success"):
      msg.reply_text(
        f"Something went wrong please contact @{SUPPORT_CHAT}\nForward this message to the support chat")
    else: 
      if not res.get("screenshot"):
        msg.reply_text("Nothing could be generated\nTry again later")
        return
      else:
        ss = res.get("screenshot")
        url = res.get("url")
        caption = f"Screenshot of your [query]({url})"
        bot.send_document(
          chat_id,
          document=ss,
          filename='Screenshot',
          caption=caption,
          reply_to_message_id=msg_id,
          timeout=60)
    rep.delete()

__mod_name__ = 'Search'

__help__ = REVERSE_MOD.help_mod[0]
__help__ += '''
\nThis command helps with taking of screenshots of webpages
• `/snip <url>`*:* Try `/snip github.com` for better knowing this command
'''

WEBSS_HANDLER = DisableAbleCommandHandler("snip", web_ss)
dispatcher.add_handler(WEBSS_HANDLER)
