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

private const val WORKER_API_BASE_URL = BuildConfig.WORKER_API_BASE_URL

class MainActivity : ComponentActivity() {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main.immediate)
    private val permissionLauncher = registerForActivityResult(ActivityResultContracts.RequestMultiplePermissions()) { }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestDevicePermissions()
        setContentView(buildUi())
    }

    private fun requestDevicePermissions() {
        val requested = listOf(Manifest.permission.CAMERA, Manifest.permission.RECORD_AUDIO)
            .filter { ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED }
        if (requested.isNotEmpty()) permissionLauncher.launch(requested.toTypedArray())
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

        val scroll = ScrollView(this)
        val messages = TextView(this).apply {
            text = "کارگر مجتبی آماده است."
            textSize = 17f
            setTextColor(Color.DKGRAY)
            setPadding(0, 24, 0, 24)
        }
        scroll.addView(messages)
        root.addView(scroll, LinearLayout.LayoutParams(-1, 0, 1f))

        val row = LinearLayout(this).apply { orientation = LinearLayout.HORIZONTAL }
        val input = EditText(this).apply { hint = "چه کاری انجام بدهم؟"; singleLine = true }
        val send = Button(this).apply { text = "ارسال" }
        row.addView(input, LinearLayout.LayoutParams(0, -2, 1f))
        row.addView(send, LinearLayout.LayoutParams(-2, -2))
        root.addView(row)

        val client = WorkerApiClient(WORKER_API_BASE_URL)
        send.setOnClickListener {
            val request = input.text.toString().trim()
            if (request.isEmpty()) return@setOnClickListener
            input.setText("")
            send.isEnabled = false
            messages.append("\n\nشما: $request")
            scope.launch {
                try {
                    val result = withContext(Dispatchers.IO) { client.sendTask(request) }
                    messages.append("\nکارگر: " + result.message())
                } catch (e: Exception) {
                    messages.append("\nخطا: " + (e.message ?: "اتصال برقرار نشد"))
                } finally {
                    send.isEnabled = true
                }
            }
        }
        return root
    }

    override fun onDestroy() {
        scope.cancel()
        super.onDestroy()
    }
}
