import os
import logging
import sys

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

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
autonomous_cycle = AutonomousCycle(PROJECT_ROOT)


def is_owner(update: Update) -> bool:
    user = update.effective_user
    return user is not None and user.id == OWNER_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    await update.message.reply_text("🧠 Master Agent فعال شد.\n\n👑 مالک\n🔐 تأیید مالک: فعال\n🛡️ Execution Controller: فعال\n\nدستورها:\n/goal متن هدف\n/cycle [هدف] اجرای چرخه امن\n/status وضعیت سیستم\n/tasks اهداف\n/approvals تأییدها\n/help راهنما")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    await update.message.reply_text("📚 راهنما\n\n/goal ثبت هدف\n/cycle [هدف] چرخه امن و ساخت بسته\n/status وضعیت\n/tasks اهداف\n/approvals درخواست‌های تأیید")


async def cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    goal_text = " ".join(context.args).strip()
    if not goal_text:
        stored = autonomous_cycle.master.state.get("goals", [])
        goal_text = stored[-1]["text"] if stored else "ساخت و توسعه سایت شرکت"
    try:
        result = autonomous_cycle.run(goal_text)
        report, safety = result["report"], result["safety"]
        package, approval = result.get("package"), result.get("approval_request")
        completed = "، ".join(report["completed"]) or "—"; pending = "، ".join(report["pending"]) or "—"
        package_text = (f"\n📦 بسته: {package['package_id']}\n🔐 درخواست تأیید: {approval['id']}\n⏳ تأیید مالک برای انتقال لازم است." if package and approval else "\n📦 بسته ساخته نشد؛ چرخه نیازمند بررسی است.")
        await update.message.reply_text(f"🧠 چرخه امن\n\n🎯 هدف: {goal_text}\n🔄 چرخه: {report['cycle']}\n📍 مرحله: {report['phase']}\n\n✅ انجام‌شده: {completed}\n⏳ باقی‌مانده: {pending}\n🔐 تأیید مالک: فعال\n🛡️ Sandbox: فعال\n🚫 تغییر واقعی قبل از تأیید: {'مجاز' if safety['real_changes_allowed'] else 'غیرمجاز'}{package_text}")
    except Exception as exc:
        logging.exception("Autonomous cycle failed")
        await update.message.reply_text(f"⛔ چرخه اجرا نشد.\n\nخطا: {exc}")


async def goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("❗ مثال:\n/goal ساخت و توسعه سایت شرکت"); return
    plan = planner.create_plan(text)
    item = autonomous_cycle.master.set_goal(text)
    plan_text = "\n".join(f"{i}. {action}" for i, action in enumerate(plan["actions"], 1))
    approval = gateway.request("goal_execution", f"اجرای هدف شماره {item['id']}: {text}", metadata={"goal_id": item["id"], "goal": text})
    await update.message.reply_text(f"🎯 هدف شماره {item['id']} ثبت و در Core ذخیره شد.\n\n{text}\n\n🔐 درخواست تأیید شماره {approval['id']} ساخته شد.\n\n🧠 برنامه Planner:\n{plan_text}\n\n⏳ وضعیت: در انتظار تأیید مالک.\nℹ️ برای ساخت بسته تغییر کنترل‌شده /cycle را اجرا کنید.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    s = autonomous_cycle.master.status()
    await update.message.reply_text(f"🧠 وضعیت Master Agent\n\n🟢 سیستم: فعال\n🎯 اهداف ثبت‌شده در Core: {s.get('goals', 0)}\n🔄 چرخه‌ها: {s['cycles']}\n🔐 تأیید مالک: فعال\n🛡️ Execution Controller: فعال\n📦 Change Package: فعال\n🔄 Autonomous Cycle: فعال\n🧪 اجرای کد تولیدشده: غیرفعال\n🧬 خودسازی: کنترل‌شده")


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    stored = autonomous_cycle.master.state.get("goals", [])
    if not stored: await update.message.reply_text("📋 هنوز هدفی ثبت نشده است."); return
    await update.message.reply_text("📋 اهداف ذخیره‌شده:\n\n" + "\n".join(f"#{x['id']} — {x['status']}\n{x['text']}\n" for x in stored))


async def approvals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update): return
    waiting = gateway.get_waiting()
    if not waiting: await update.message.reply_text("📭 درخواست تأیید در انتظار وجود ندارد."); return
    for item in waiting:
        metadata=item.get("metadata") or {}; package_line=f"📦 بسته: {metadata['package_id']}\n" if metadata.get("package_id") else ""
        message=f"🔐 درخواست تأیید مالک\n\n🆔 {item['id']}\n⚙️ {item['action']}\n📝 {item.get('reason','')}\n{package_line}\nآیا اجازه اجرا می‌دهید?"
        keyboard=[[InlineKeyboardButton("✅ تأیید",callback_data=f"approve:{item['id']}"),InlineKeyboardButton("❌ رد",callback_data=f"reject:{item['id']}")]]
        await update.message.reply_text(message,reply_markup=InlineKeyboardMarkup(keyboard))


async def approval_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query=update.callback_query
    if query is None: return
    if query.from_user.id != OWNER_ID: await query.answer("⛔ فقط مالک اجازه دارد.",show_alert=True); return
    await query.answer()
    try: action, request_id_text=query.data.split(":"); request_id=int(request_id_text)
    except (ValueError,AttributeError): await query.edit_message_text("❌ درخواست نامعتبر است."); return
    request=gateway.get(request_id)
    if request is None: await query.edit_message_text("❌ درخواست پیدا نشد."); return
    if request["status"] != "waiting_approval": await query.edit_message_text(f"ℹ️ درخواست {request_id} قبلاً تعیین تکلیف شده است."); return
    if action == "reject": gateway.reject(request_id); await query.edit_message_text(f"❌ درخواست {request_id} رد شد.\nهیچ اجرایی انجام نشد."); return
    if action != "approve": await query.edit_message_text("❌ اقدام نامعتبر است."); return
    metadata=request.get("metadata") or {}; package_id=metadata.get("package_id")
    approved=gateway.approve(request_id)
    if not approved: await query.edit_message_text("❌ تأیید انجام نشد."); return
    if request["action"] == "change_package_deploy" and package_id:
        try: result=package_executor.execute(package_id,request_id)
        except Exception as exc: logging.exception("Package promotion failed"); await query.edit_message_text(f"⛔ تأیید ثبت شد اما انتقال متوقف شد.\n\nخطا: {exc}"); return
        if result.get("success"): await query.edit_message_text(f"✅ درخواست {request_id} تأیید و بسته منتقل شد.\n\n📦 {package_id}\n💾 Backup: {result['backup_path']}\n📁 فایل‌ها: {', '.join(result['promoted_files']) or '—'}\n🛡️ کد تولیدشده اجرا نشد.")
        else: await query.edit_message_text(f"⛔ انتقال انجام نشد.\n\nوضعیت: {result.get('status')}")
        return
    await query.edit_message_text(f"✅ درخواست {request_id} تأیید شد؛ اما بسته تغییر ندارد.\n⛔ اجرای واقعی انجام نشد.")


def main():
    if not TOKEN: raise RuntimeError("TELEGRAM_BOT_TOKEN تنظیم نشده است.")
    if OWNER_ID == 0: raise RuntimeError("OWNER_ID تنظیم نشده است.")
    app=Application.builder().token(TOKEN).build()
    for command,handler in (("start",start),("help",help_command),("cycle",cycle),("goal",goal),("status",status),("tasks",tasks),("approvals",approvals)): app.add_handler(CommandHandler(command,handler))
    app.add_handler(CallbackQueryHandler(approval_callback))
    print("🧠 Master Agent Telegram Bot is running..."); print("🔐 Owner Approval: ACTIVE"); print("📦 Change Package Promotion: ACTIVE")
    app.run_polling()


if __name__ == "__main__": main()
