package com.mojtaba.worker

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Bundle
import android.view.Gravity
import android.widget.*
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import com.mojtaba.worker.network.WorkerApiClient
import kotlinx.coroutines.*
import com.mojtaba.worker.voice.VoicePlayer
import com.mojtaba.worker.voice.VoiceRecorder

private const val WORKER_API_BASE_URL = BuildConfig.WORKER_API_BASE_URL

class MainActivity : ComponentActivity() {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)
    private val permissionLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { }
    private lateinit var recorder: VoiceRecorder
    private val player = VoicePlayer()
    private var recordingFile: java.io.File? = null
    private var isRecording = false
    private var isSending = false
    private lateinit var messages: TextView
    private lateinit var scroll: ScrollView
    private lateinit var input: EditText
    private lateinit var send: Button
    private lateinit var voice: Button
    private lateinit var clear: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        recorder = VoiceRecorder(this)
        requestDevicePermissions()
        setContentView(buildUi())
    }

    private fun requestDevicePermissions() {
        val requested = listOf(Manifest.permission.CAMERA, Manifest.permission.RECORD_AUDIO)
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
            setPadding(32, 32, 32, 24)
        }
        val title = TextView(this).apply {
            text = "کارگر مجتبی"
            textSize = 28f
            setTextColor(Color.BLACK)
            gravity = Gravity.CENTER
        }
        root.addView(title, LinearLayout.LayoutParams(-1, -2))

        scroll = ScrollView(this)
        messages = TextView(this).apply {
            text = "کارگر مجتبی آماده است."
            textSize = 17f
            setTextColor(Color.DKGRAY)
            setPadding(0, 24, 0, 24)
        }
        scroll.addView(messages)
        root.addView(scroll, LinearLayout.LayoutParams(-1, 0, 1f))

        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        input = EditText(this).apply { hint = "چه کاری انجام بدهم؟"; setSingleLine(true); imeOptions = android.view.inputmethod.EditorInfo.IME_ACTION_SEND }
        send = Button(this).apply { text = "ارسال" }
        voice = Button(this).apply { text = "🎤 پیام صوتی" }
        clear = Button(this).apply { text = "پاک کردن" }
        row.addView(input, LinearLayout.LayoutParams(0, -2, 1f))
        row.addView(send, LinearLayout.LayoutParams(-2, -2))
        row.addView(voice, LinearLayout.LayoutParams(-2, -2))
        row.addView(clear, LinearLayout.LayoutParams(-2, -2))
        root.addView(row)

        clear.setOnClickListener {
            messages.text = "کارگر مجتبی آماده است."
            scroll.post { scroll.fullScroll(ScrollView.FOCUS_DOWN) }
        }

        val client = WorkerApiClient(WORKER_API_BASE_URL)
        voice.setOnClickListener {
            try {
                if (!isRecording) {
                    if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                        permissionLauncher.launch(arrayOf(Manifest.permission.RECORD_AUDIO)); return@setOnClickListener
                    }
                    recordingFile = recorder.start()
                    isRecording = true
                    voice.text = "⏹ توقف ضبط"
                } else {
                    val file = recorder.stop()
                    recordingFile = file
                    isRecording = false
                    voice.text = "🔊 پخش پیام صوتی"
                    player.play(file)
                    appendMessage("\n\nشما: 🎤 پیام صوتی")
                    scope.launch {
                        try {
                            val result = withContext(Dispatchers.IO) { client.sendVoice(file) }
                            appendMessage("\nکارگر: " + result.message())
                        } catch (e: Exception) {
                            appendMessage("\nخطای ارسال صوت: " + (e.message ?: "اتصال برقرار نشد"))
                        }
                    }
                }
            } catch (e: Exception) { appendMessage("\nخطای صوتی: " + (e.message ?: "خطا")) }
        }

        send.setOnClickListener { submitRequest(client) }
        input.setOnEditorActionListener { _, actionId, event ->
            val sendAction = actionId == android.view.inputmethod.EditorInfo.IME_ACTION_SEND
            val enterKey = event?.keyCode == android.view.KeyEvent.KEYCODE_ENTER && event.action == android.view.KeyEvent.ACTION_DOWN
            if (sendAction || enterKey) { submitRequest(client); true } else false
        }
        return root
    }

    private fun resetVoiceButton() {
        isRecording = false
        voice.text = "🎤 پیام صوتی"
    }

    private fun submitRequest(client: WorkerApiClient) {
        if (isSending) return
        val request = input.text.toString().trim()
        if (request.isEmpty()) return
        input.setText("")
        isSending = true
        setControlsEnabled(false)
        appendMessage("\n\nشما: $request")
        scope.launch {
            try {
                val result = withContext(Dispatchers.IO) { client.sendTask(request) }
                appendMessage("\nکارگر: " + result.message())
            } catch (e: Exception) {
                appendMessage("\nخطا: " + (e.message ?: "اتصال برقرار نشد"))
            } finally {
                isSending = false
                setControlsEnabled(true)
            }
        }
    }

    private fun setControlsEnabled(enabled: Boolean) {
        send.isEnabled = enabled
        input.isEnabled = enabled
        clear.isEnabled = enabled
        if (!isRecording) voice.isEnabled = enabled
    }

    override fun onDestroy() {
        player.stop()
        recorder.cancel()
        resetVoiceButton()
        recordingFile?.delete()
        scope.cancel()
        super.onDestroy()
    }
}
