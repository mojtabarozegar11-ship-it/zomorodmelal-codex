package com.mojtaba.worker

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { WorkerChat() }
    }
}

@Composable
fun WorkerChat() {
    var text by remember { mutableStateOf("") }
    var messages by remember { mutableStateOf(listOf("کارگر مجتبی آماده است.")) }
    Column(Modifier.fillMaxSize().padding(16.dp)) {
        Text("کارگر مجتبی", style = MaterialTheme.typography.headlineMedium)
        Spacer(Modifier.height(16.dp))
        messages.forEach { Text(it, Modifier.padding(vertical = 4.dp)) }
        Spacer(Modifier.weight(1f))
        Row(Modifier.fillMaxWidth()) {
            OutlinedTextField(text, { text = it }, Modifier.weight(1f), placeholder = { Text("چه کاری انجام بدهم؟") })
            Spacer(Modifier.width(8.dp))
            Button(onClick = { if (text.isNotBlank()) { messages = messages + "شما: $text"; text = "" } }) { Text("ارسال") }
        }
    }
}
