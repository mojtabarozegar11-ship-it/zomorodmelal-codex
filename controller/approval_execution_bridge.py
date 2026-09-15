import os
import sys


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from approval.approval_gateway import ApprovalGateway
from execution.execution_controller import ExecutionController


class ApprovalExecutionBridge:

    def __init__(self):
        self.approval = ApprovalGateway()
        self.execution = ExecutionController()

    def execute_approved(
        self,
        request_id,
        files=None
    ):
        # درخواست باید وجود داشته باشد
        request = self.approval.get(request_id)

        if not request:
            return {
                "success": False,
                "status": "request_not_found",
                "request_id": request_id
            }

        # فقط وضعیت ثبت‌شده در Approval Gateway معتبر است
        if not self.approval.is_approved(request_id):
            return {
                "success": False,
                "status": "approval_required",
                "request_id": request_id,
                "message": "تأیید معتبر مالک وجود ندارد."
            }

        # اجرای کنترل‌شده
        return self.execution.execute(
            request_id=request_id,
            action=request["action"],
            approved=True,
            files=files
        )


if __name__ == "__main__":

    bridge = ApprovalExecutionBridge()

    print("🔐 Approval → Execution Bridge")
    print("=" * 45)

    request = bridge.approval.request(
        action="bridge_test",
        reason="تست اتصال تأیید مالک به Execution Controller"
    )

    print("\n📋 درخواست:")
    print(request)

    print("\n🚫 قبل از تأیید:")

    result = bridge.execute_approved(
        request["id"]
    )

    print(result)

    print("\n🛑 تست بدون تأیید انجام شد.")
