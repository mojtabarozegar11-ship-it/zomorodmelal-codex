package com.mojtaba.worker

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.mojtaba.worker.network.WorkerApiClient
import kotlinx.coroutines.launch

private const val WORKER_API_BASE_URL = BuildConfig.WORKER_API_BASE_URL

class MainActivity : ComponentActivity() {
    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { _ -> }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestDevicePermissions()
        setContent { WorkerChat() }
    }

    private fun requestDevicePermissions() {
        val requested = listOf(Manifest.permission.CAMERA, Manifest.permission.RECORD_AUDIO)
            .filter { ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED }
        if (requested.isNotEmpty()) permissionLauncher.launch(requested.toTypedArray())
    }
}

@Composable
fun WorkerChat() {
    var text by remember { mutableStateOf("") }
    var messages by remember { mutableStateOf(listOf("کارگر مجتبی آماده است.")) }
    var busy by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    val client = remember { WorkerApiClient(WORKER_API_BASE_URL) }

    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text("کارگر مجتبی", style = MaterialTheme.typography.headlineMedium)
        Spacer(Modifier.height(16.dp))
        messages.forEach { Text(it, Modifier.padding(vertical = 4.dp)) }
        Spacer(Modifier.weight(1f))
        Row(Modifier.fillMaxWidth()) {
            OutlinedTextField(
                value = text,
                onValueChange = { text = it },
                modifier = Modifier.weight(1f),
                enabled = !busy,
                placeholder = { Text("چه کاری انجام بدهم؟") }
            )
            Spacer(Modifier.width(8.dp))
            Button(
                enabled = text.isNotBlank() && !busy,
                onClick = {
                    val request = text.trim()
                    text = ""
                    messages = messages + "شما: $request"
                    busy = true
                    scope.launch {
                        try {
                            val result = client.sendTask(request)
                            messages = messages + "کارگر: " + result.message()
                        } catch (e: Exception) {
                            messages = messages + "خطا: " + (e.message ?: "اتصال برقرار نشد")
                        } finally {
                            busy = false
                        }
                    }
                }
            ) { Text(if (busy) "..." else "ارسال") }
        }
    }
}
