package com.mojtaba.worker

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Bundle
import android.text.InputType
import android.view.Gravity
import android.widget.*
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import com.mojtaba.worker.agent.MasterAgentCoordinator
import com.mojtaba.worker.voice.VoicePlayer
import com.mojtaba.worker.voice.VoiceRecorder
import kotlinx.coroutines.*

class MainActivity : ComponentActivity() {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)
    private val permissionLauncher =
        registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { }
    private lateinit var recorder: VoiceRecorder
    private val player = VoicePlayer()
    private var recordingFile: java.io.File? = null
    private var isRecording = false
    private var isSending = false
    private lateinit var masterAgent: MasterAgentCoordinator
    private lateinit var messages: TextView
    private lateinit var scroll: ScrollView
    private lateinit var input: EditText
    private lateinit var send: Button
    private lateinit var voice: Button
    private lateinit var clear: Button
    private lateinit var settings: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        recorder = VoiceRecorder(this)
        masterAgent = MasterAgentCoordinator(this)
        requestDevicePermissions()
        setContentView(buildUi())
    }

    private fun requestDevicePermissions() {
        val requested = listOf(Manifest.permission.RECORD_AUDIO)
            .filter { ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED }
        if (requested.isNotEmpty()) permissionLauncher.launch(requested.toTypedArray())
    }

    private fun appendMessage(text: String) {
        messages.append(text)
        scroll.post { scroll.fullScroll(ScrollView.FOCUS_DOWN) }
    }

    private fun buildUi(): LinearLayout {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(32, 32, 32, 24)
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
        }

        val title = TextView(this).apply {
            text = "کارگر مجتبی"
            textSize = 26f
            setTextColor(Color.BLACK)
            gravity = Gravity.CENTER
        }
        root.addView(title, LinearLayout.LayoutParams(-1, -2))

        val status = TextView(this).apply {
            text = "آماده به کار"
            textSize = 14f
            setTextColor(Color.DKGRAY)
            gravity = Gravity.CENTER
        }
        root.addView(status, LinearLayout.LayoutParams(-1, -2))

        val topRow = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
        }
        settings = Button(this).apply { text = "تنظیمات سرویس" }
        clear = Button(this).apply { text = "پاک‌سازی" }
        topRow.addView(settings, LinearLayout.LayoutParams(0, -2, 1f))
        topRow.addView(clear, LinearLayout.LayoutParams(0, -2, 1f))
        root.addView(topRow)

        scroll = ScrollView(this)
        messages = TextView(this).apply {
            text = "دستیار آماده است. درخواست خود را بنویسید یا با صدا بگویید."
            textSize = 17f
            setTextColor(Color.DKGRAY)
            gravity = Gravity.RIGHT
            textDirection = android.view.View.TEXT_DIRECTION_RTL
            setPadding(0, 24, 0, 24)
        }
        scroll.addView(messages)
        root.addView(scroll, LinearLayout.LayoutParams(-1, 0, 1f))

        val row = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            layoutDirection = android.view.View.LAYOUT_DIRECTION_RTL
        }
        input = EditText(this).apply {
            hint = "چه کاری برایتان انجام بدهم؟"
            setSingleLine(true)
            inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_FLAG_CAP_SENTENCES
            imeOptions = android.view.inputmethod.EditorInfo.IME_ACTION_SEND
            textDirection = android.view.View.TEXT_DIRECTION_RTL
            gravity = Gravity.RIGHT
        }
        send = Button(this).apply { text = "اجرا" }
        voice = Button(this).apply { text = "🎤 پیام صوتی" }

        row.addView(send, LinearLayout.LayoutParams(-2, -2))
        row.addView(voice, LinearLayout.LayoutParams(-2, -2))
        row.addView(input, LinearLayout.LayoutParams(0, -2, 1f))
        root.addView(row)

        clear.setOnClickListener {
            messages.text = "دستیار آماده است. درخواست خود را بنویسید یا با صدا بگویید."
        }

        settings.setOnClickListener { showApiSettings() }

        voice.setOnClickListener {
            try {
                if (!isRecording) {
                    if (ContextCompat.checkSelfPermission(
                            this,
                            Manifest.permission.RECORD_AUDIO
                        ) != PackageManager.PERMISSION_GRANTED
                    ) {
                        permissionLauncher.launch(arrayOf(Manifest.permission.RECORD_AUDIO))
                        return@setOnClickListener
                    }
                    recordingFile = recorder.start()
                    isRecording = true
                    voice.text = "⏹ توقف ضبط"
                    status.text = "در حال ضبط صدا…"
                } else {
                    val file = recorder.stop()
                    recordingFile = file
                    isRecording = false
                    voice.text = "🎤 پیام صوتی"
                    status.text = "در حال پردازش…"

                    player.play(file)
                    appendMessage("\n\nشما: 🎤 پیام صوتی")
                    scope.launch {
                        try {
                            val result = masterAgent.submitVoice(file, input.text.toString().trim())
                            appendMessage("\nدستیار: " + result.message)
                        } catch (e: Exception) {
                            appendMessage("\nخطا در پردازش صدا: " + (e.message ?: "خطای ناشناخته"))
                        } finally {
                            status.text = "آماده به کار"
                        }
                    }
                }
            } catch (e: Exception) {
                appendMessage("\nخطای صوتی: " + (e.message ?: "خطا"))
                status.text = "آماده به کار"
                resetVoiceButton()
            }
        }

        send.setOnClickListener { submitRequest() }
        input.setOnEditorActionListener { _, actionId, event ->
            val sendAction = actionId == android.view.inputmethod.EditorInfo.IME_ACTION_SEND
            val enterKey =
                event?.keyCode == android.view.KeyEvent.KEYCODE_ENTER &&
                    event.action == android.view.KeyEvent.ACTION_DOWN
            if (sendAction || enterKey) {
                submitRequest()
                true
            } else {
                false
            }
        }
        return root
    }

    private fun showApiSettings() {
        val inputField = EditText(this).apply {
            hint = "https://example.com"
            setSingleLine(true)
            inputType = InputType.TYPE_CLASS_TEXT or InputType.TYPE_TEXT_VARIATION_URI
            setText(masterAgent.getApiBaseUrl())
        }
        AlertDialog.Builder(this)
            .setTitle("تنظیم سرویس")
            .setMessage("نشانی HTTPS سرویس کارگر مجتبی را وارد کنید. برای کارکرد آفلاین می‌توانید خالی بگذارید.")
            .setView(inputField)
            .setNegativeButton("انصراف", null)
            .setNeutralButton("پاک کردن") { _, _ ->
                masterAgent.setApiBaseUrl("")
            }
            .setPositiveButton("ذخیره") { _, _ ->
                val url = inputField.text.toString().trim()
                if (url.isEmpty() || url.startsWith("https://")) {
                    masterAgent.setApiBaseUrl(url)
                    appendMessage("\nتنظیمات سرویس ذخیره شد.")
                } else {
                    appendMessage("\nخطا: نشانی سرویس باید با HTTPS شروع شود.")
                }
            }
            .show()
    }

    private fun submitRequest() {
        if (isSending) return
        val request = input.text.toString().trim()
        if (request.isEmpty()) return
        input.setText("")
        isSending = true
        statusView("در حال پردازش…")
        setControlsEnabled(false)
        appendMessage("\n\nشما: $request")
        scope.launch {
            try {
                val result = masterAgent.submit(request)
                appendMessage("\nدستیار: " + result.message)
            } catch (e: Exception) {
                appendMessage("\nخطا: " + (e.message ?: "پردازش ناموفق بود"))
            } finally {
                isSending = false
                setControlsEnabled(true)
                statusView("آماده به کار")
            }
        }
    }

    private fun statusView(value: String) {
        val root = window.decorView.findViewById<TextView>(android.R.id.content)
        // The visible status label is updated through the title hierarchy on the main thread.
        val content = root as? android.view.ViewGroup ?: return
        findFirstTextView(content)?.let { tv ->
            if (tv !== messages) tv.text = value
        }
    }

    private fun findFirstTextView(view: android.view.ViewGroup): TextView? {
        for (index in 0 until view.childCount) {
            val child = view.getChildAt(index)
            if (child is TextView && child !== messages) return child
            if (child is android.view.ViewGroup) {
                val nested = findFirstTextView(child)
                if (nested != null) return nested
            }
        }
        return null
    }

    private fun setControlsEnabled(enabled: Boolean) {
        send.isEnabled = enabled
        input.isEnabled = enabled
        clear.isEnabled = enabled
        settings.isEnabled = enabled
        if (!isRecording) voice.isEnabled = enabled
    }

    private fun resetVoiceButton() {
        isRecording = false
        voice.text = "🎤 پیام صوتی"
    }

    override fun onDestroy() {
        player.stop()
        recorder.cancel()
        recordingFile?.delete()
        scope.cancel()
        super.onDestroy()
    }
}
