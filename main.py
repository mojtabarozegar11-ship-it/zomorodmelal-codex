import os
import logging
import sys

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from approval.approval_gateway import ApprovalGateway
from autonomous_core.autonomous_cycle import AutonomousCycle
from controller.change_package_executor import ChangePackageExecutor
from execution.execution_controller import ExecutionController
from planner.planner import Planner

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

goals = []
gateway = ApprovalGateway()
executor = ExecutionController()
package_executor = ChangePackageExecutor()
planner = Planner()
autonomous_cycle = AutonomousCycle()


def is_owner(update: Update) -> bool:
    user = update.effective_user
    return user is not None and user.id == OWNER_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return
    await update.message.reply_text(
        "🧠 Master Agent فعال شد.\n\n👑 سلام مالک\n🔐 تأیید مالک: فعال\n🛡️ Execution Controller: فعال\n\n"
        "دستورها:\n/goal متن هدف\n/cycle اجرای چرخه امن و ساخت بسته\n/status وضعیت سیستم\n/tasks اهداف\n/approvals درخواست‌های تأیید\n/help راهنما"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return
    await update.message.reply_text(
        "📚 راهنما\n\n/goal ثبت هدف\n/cycle چرخه امن Master Agent و ایجاد بسته تأیید\n/status وضعیت\n/tasks اهداف\n/approvals درخواست‌های تأیید\n/help راهنما"
    )


async def cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return
    try:
        result = autonomous_cycle.run()
        report = result["report"]
        safety = result["safety"]
        package = result.get("package")
        approval = result.get("approval_request")
        completed = "، ".join(report["completed"]) or "—"
        pending = "، ".join(report["pending"]) or "—"
        package_text = (
            f"\n📦 بسته تغییر: {package['package_id']}\n🔐 درخواست تأیید: {approval['id']}\n"
            "⏳ برای انتقال به محیط اصلی، تأیید مالک لازم است."
            if package and approval else
            "\n📦 بسته تأییدشدنی ساخته نشد؛ چرخه نیازمند اصلاح/بررسی است."
        )
        await update.message.reply_text(
            "🧠 چرخه امن Master Agent\n\n"
            f"🔄 چرخه: {report['cycle']}\n📍 مرحله: {report['phase']}\n\n"
            f"✅ انجام‌شده: {completed}\n⏳ باقی‌مانده: {pending}\n"
            f"🔐 تأیید مالک: {'فعال' if report['owner_approval_required'] else 'غیرفعال'}\n"
            f"🛡️ Sandbox: {'فعال' if safety['sandbox_only'] else 'غیرفعال'}\n"
            f"🚫 تغییر واقعی قبل از تأیید: {'مجاز' if safety['real_changes_allowed'] else 'غیرمجاز'}"
            f"{package_text}"
        )
    except Exception as exc:
        logging.exception("Autonomous cycle failed")
        await update.message.reply_text(f"⛔ چرخه اجرا نشد.\n\nخطا: {exc}")


async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return
    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("❗ مثال:\n/goal ساخت و توسعه سایت شرکت")
        return
    goal_id = len(goals) + 1
    plan = planner.create_plan(text)
    goals.append({"id": goal_id, "text": text, "status": "WAITING_APPROVAL", "plan": plan})
    plan_text = "\n".join(f"{i}. {action}" for i, action in enumerate(plan["actions"], 1))
    approval = gateway.request("goal_execution", f"اجرای هدف شماره {goal_id}: {text}")
    await update.message.reply_text(
        f"🎯 هدف شماره {goal_id} ثبت شد.\n\n{text}\n\n"
        f"🔐 درخواست تأیید شماره {approval['id']} ساخته شد.\n\n"
        f"🧠 برنامه پیشنهادی Planner:\n{plan_text}\n\n⏳ وضعیت: در انتظار تأیید مالک.\n"
        "ℹ️ این درخواست تا زمانی که به بسته تغییر مشخص متصل نشود، اجرای واقعی ندارد."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return
    await update.message.reply_text(
        "🧠 وضعیت Master Agent\n\n🟢 سیستم: فعال\n"
        f"🎯 اهداف: {len(goals)}\n🔐 تأیید مالک: فعال\n🛡️ Execution Controller: فعال\n"
        "📦 Change Package: فعال\n🔄 Autonomous Cycle: فعال\n"
        "🧪 اجرای کد تولیدشده: غیرفعال\n🧬 خودسازی: کنترل‌شده"
    )


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return
    if not goals:
        await update.message.reply_text("📋 هنوز هدفی ثبت نشده است.")
        return
    await update.message.reply_text(
        "📋 اهداف:\n\n" + "\n".join(f"#{item['id']} — {item['status']}\n{item['text']}\n" for item in goals)
    )


async def approvals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update):
        return
    waiting = [item for item in gateway.get_all() if item.get("status") == "waiting_approval"]
    if not waiting:
        await update.message.reply_text("📭 درخواست تأیید در انتظار وجود ندارد.")
        return
    for item in waiting:
        metadata = item.get("metadata") or {}
        package_line = f"📦 بسته: {metadata['package_id']}\n" if metadata.get("package_id") else ""
        message = (
            "🔐 درخواست تأیید مالک\n\n"
            f"🆔 شماره: {item['id']}\n⚙️ اقدام: {item['action']}\n"
            f"📝 دلیل: {item.get('reason', '')}\n{package_line}\nآیا اجازه اجرا می‌دهید؟"
        )
        keyboard = [[InlineKeyboardButton("✅ تأیید", callback_data=f"approve:{item['id']}"), InlineKeyboardButton("❌ رد", callback_data=f"reject:{item['id']}")]]
        await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(keyboard))


async def approval_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query is None:
        return
    if query.from_user.id != OWNER_ID:
        await query.answer("⛔ فقط مالک اجازه دارد.", show_alert=True)
        return
    await query.answer()
    try:
        action, request_id_text = query.data.split(":")
        request_id = int(request_id_text)
    except (ValueError, AttributeError):
        await query.edit_message_text("❌ درخواست نامعتبر است.")
        return

    request = gateway.get(request_id)
    if request is None:
        await query.edit_message_text("❌ درخواست پیدا نشد.")
        return

    if action == "reject":
        result = gateway.reject(request_id)
        await query.edit_message_text(
            f"❌ درخواست {request_id} رد شد.\nهیچ اجرایی انجام نشد."
            if result else "❌ درخواست پیدا نشد."
        )
        return

    if action != "approve":
        await query.edit_message_text("❌ اقدام نامعتبر است.")
        return

    if request["status"] != "waiting_approval":
        await query.edit_message_text(f"ℹ️ درخواست {request_id} قبلاً تعیین تکلیف شده است.")
        return

    metadata = request.get("metadata") or {}
    package_id = metadata.get("package_id")

    approved = gateway.approve(request_id)
    if not approved:
        await query.edit_message_text("❌ تأیید انجام نشد.")
        return

    if request["action"] == "change_package_deploy" and package_id:
        try:
            result = package_executor.execute(package_id, request_id)
        except Exception as exc:
            logging.exception("Package promotion failed")
            await query.edit_message_text(
                f"⛔ درخواست {request_id} تأیید شد اما انتقال متوقف شد.\n\nخطا: {exc}"
            )
            return
        if result.get("success"):
            await query.edit_message_text(
                f"✅ درخواست {request_id} تأیید و بسته منتقل شد.\n\n"
                f"📦 بسته: {package_id}\n💾 Backup: {result['backup_path']}\n"
                f"📁 فایل‌ها: {', '.join(result['promoted_files']) or '—'}\n"
                "🛡️ کد تولیدشده اجرا نشد."
            )
        else:
            await query.edit_message_text(f"⛔ انتقال انجام نشد.\n\nوضعیت: {result.get('status')}")
        return

    if request["action"] == "self_improvement_cycle":
        result = executor.execute(request_id, request["action"])
        if result.get("success"):
            await query.edit_message_text(
                f"✅ درخواست {request_id} تأیید و مرحله کنترل‌شده انجام شد.\n\n"
                "🛡️ Execution Controller: موفق\n💾 Backup: ایجاد شد\n🧪 اجرای کد: غیرفعال"
            )
        else:
            await query.edit_message_text(f"⛔ اجرای درخواست متوقف شد.\n\nدلیل: {result.get('reason', result.get('message', 'unknown'))}")
        return

    await query.edit_message_text(
        f"✅ درخواست {request_id} تأیید شد؛ اما این درخواست به بسته تغییر تأییدشده متصل نیست.\n"
        "⛔ اجرای واقعی انجام نشد."
    )


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN تنظیم نشده است.")
    if OWNER_ID == 0:
        raise RuntimeError("OWNER_ID تنظیم نشده است.")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cycle", cycle))
    app.add_handler(CommandHandler("goal", goal))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("tasks", tasks))
    app.add_handler(CommandHandler("approvals", approvals))
    app.add_handler(CallbackQueryHandler(approval_callback))
    print("🧠 Master Agent Telegram Bot is running...")
    print("🔐 Owner Approval: ACTIVE")
    print("📦 Change Package Promotion: ACTIVE")
    app.run_polling()


if __name__ == "__main__":
    main()
