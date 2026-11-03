document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("demoSubmit");
    const note = document.getElementById("formNote");
    const type = document.getElementById("leadType");

    if (button && note && type) {
        button.addEventListener("click", () => {
            note.textContent = `درخواست «${type.value}» آماده ارسال است. اتصال نهایی به CRM/API در مرحله یکپارچه‌سازی انجام می‌شود.`;
        });
    }
});
