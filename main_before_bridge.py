import os
import logging
import sys

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from approval.approval_gateway import ApprovalGateway
from execution.execution_controller import ExecutionController


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

goals = []

gateway = ApprovalGateway()
executor = ExecutionController()


def is_owner(update: Update) -> bool:
    user = update.effective_user
    return user is not None and user.id == OWNER_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    await update.message.reply_text(
        "🧠 Master Agent فعال شد.\n\n"
        "👑 سلام مالک\n"
        "🔐 تأیید مالک: فعال\n"
        "🛡️ Execution Controller: فعال\n\n"
        "دستورها:\n"
        "/goal متن هدف\n"
        "/status وضعیت سیستم\n"
        "/tasks اهداف\n"
        "/approvals درخواست‌های تأیید\n"
        "/help راهنما"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    await update.message.reply_text(
        "📚 راهنما\n\n"
        "/start شروع\n"
        "/goal ثبت هدف\n"
        "/status وضعیت\n"
        "/tasks اهداف\n"
        "/approvals درخواست‌های تأیید\n"
        "/help راهنما"
    )


async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    text = " ".join(context.args).strip()

    if not text:
        await update.message.reply_text(
            "❗ مثال:\n"
            "/goal ساخت و توسعه سایت شرکت"
        )
        return

    goal_id = len(goals) + 1

    goals.append({
        "id": goal_id,
        "text": text,
        "status": "WAITING_APPROVAL"
    })

    await update.message.reply_text(
        f"🎯 هدف شماره {goal_id} ثبت شد.\n\n"
        f"{text}\n\n"
        "🔐 در انتظار تأیید مالک."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    await update.message.reply_text(
        "🧠 وضعیت Master Agent\n\n"
        "🟢 سیستم: فعال\n"
        f"🎯 اهداف: {len(goals)}\n"
        "🔐 تأیید مالک: فعال\n"
        "🛡️ Execution Controller: فعال\n"
        "⛔ اجرای خودکار: غیرفعال\n"
        "🧬 خودسازی: کنترل‌شده"
    )


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    if not goals:
        await update.message.reply_text(
            "📋 هنوز هدفی ثبت نشده است."
        )
        return

    message = "📋 اهداف:\n\n"

    for item in goals:
        message += (
            f"#{item['id']} — {item['status']}\n"
            f"{item['text']}\n\n"
        )

    await update.message.reply_text(message)


async def approvals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return

    requests = gateway.get_all()

    waiting = [
        item for item in requests
        if item.get("status") == "waiting_approval"
    ]

    if not waiting:
        await update.message.reply_text(
            "📭 درخواست تأیید در انتظار وجود ندارد."
        )
        return

    for item in waiting:

        message = (
            "🔐 درخواست تأیید مالک\n\n"
            f"🆔 شماره: {item['id']}\n"
            f"⚙️ اقدام: {item['action']}\n"
            f"📝 دلیل: {item.get('reason', '')}\n\n"
            "آیا اجازه اجرا می‌دهید؟"
        )

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ تأیید",
                    callback_data=f"approve:{item['id']}"
                ),
                InlineKeyboardButton(
                    "❌ رد",
                    callback_data=f"reject:{item['id']}"
                )
            ]
        ]

        await update.message.reply_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def approval_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    if query is None:
        return

    if query.from_user.id != OWNER_ID:
        await query.answer(
            "⛔ فقط مالک اجازه دارد.",
            show_alert=True
        )
        return

    await query.answer()

    try:
        action, request_id_text = query.data.split(":")
        request_id = int(request_id_text)
    except (ValueError, AttributeError):
        await query.edit_message_text(
            "❌ درخواست نامعتبر است."
        )
        return

    if action == "reject":

        success = gateway.reject(request_id)

        if success:
            await query.edit_message_text(
                f"❌ درخواست {request_id} رد شد.\n"
                "هیچ اجرایی انجام نشد."
            )
        else:
            await query.edit_message_text(
                "❌ درخواست پیدا نشد."
            )

        return

    if action == "approve":

        success = gateway.approve(request_id)

        if not success:
            await query.edit_message_text(
                "❌ تأیید انجام نشد."
            )
            return

        requests = gateway.get_all()

        request = next(
            (
                item for item in requests
                if item["id"] == request_id
            ),
            None
        )

        if request is None:
            await query.edit_message_text(
                "❌ درخواست پیدا نشد."
            )
            return

        # فعلاً فقط اقدام آزمایشی مجاز است.
        if request["action"] != "self_improvement_cycle":

            await query.edit_message_text(
                f"✅ درخواست {request_id} تأیید شد.\n\n"
                "⛔ اجرای این نوع اقدام هنوز فعال نشده است.\n"
                "درخواست فقط ثبت شد."
            )
            return

        result = executor.execute(
            request_id,
            request["action"]
        )

        if result.get("success"):

            await query.edit_message_text(
                f"✅ درخواست {request_id} تأیید و اجرا شد.\n\n"
                "🛡️ Execution Controller: موفق\n"
                "💾 Backup: ایجاد شد\n"
                "🧪 اجرای واقعی تغییرات: فعلاً غیرفعال"
            )

        else:

            await query.edit_message_text(
                f"⛔ اجرای درخواست {request_id} متوقف شد.\n\n"
                f"دلیل: {result.get('reason', 'unknown')}"
            )


def main():

    if not TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN تنظیم نشده است."
        )

    if OWNER_ID == 0:
        raise RuntimeError(
            "OWNER_ID تنظیم نشده است."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("goal", goal)
    )

    app.add_handler(
        CommandHandler("status", status)
    )

    app.add_handler(
        CommandHandler("tasks", tasks)
    )

    app.add_handler(
        CommandHandler("approvals", approvals)
    )

    app.add_handler(
        CallbackQueryHandler(approval_callback)
    )

    print("🧠 Master Agent Telegram Bot is running...")
    print("🔐 Owner Approval: ACTIVE")
    print("🛡️ Execution Controller: ACTIVE")

    app.run_polling()


if __name__ == "__main__":
    main()
