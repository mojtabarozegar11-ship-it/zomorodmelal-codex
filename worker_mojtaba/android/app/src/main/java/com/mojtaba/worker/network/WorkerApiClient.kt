package com.mojtaba.worker.network

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

data class WorkerResponse(val rawJson: String) {
    fun message(): String {
        val json = JSONObject(rawJson)
        val execution = json.optJSONObject("execution")
        return execution?.optString("message")?.takeIf { it.isNotBlank() }
            ?: json.optString("message").takeIf { it.isNotBlank() }
            ?: json.optString("status", "پاسخ دریافت شد.")
    }
}

class WorkerApiClient(private val baseUrl: String) {
    suspend fun sendTask(request: String): WorkerResponse = withContext(Dispatchers.IO) {
        require(baseUrl.isNotBlank()) { "Worker API URL تنظیم نشده است." }
        require(!baseUrl.contains("YOUR_WORKER_API_HOST")) { "Worker API URL هنوز پیکربندی نشده است." }
        require(request.isNotBlank()) { "درخواست خالی است." }
        require(runCatching { URL(baseUrl) }.isSuccess) { "Worker API URL نامعتبر است." }

        val connection = (URL(baseUrl.trimEnd('/') + "/v1/tasks").openConnection() as HttpURLConnection)
        try {
            connection.requestMethod = "POST"
            connection.setRequestProperty("Accept", "application/json")
            connection.setRequestProperty("Content-Type", "application/json; charset=utf-8")
            connection.connectTimeout = 10_000
            connection.readTimeout = 60_000
            connection.doOutput = true

            val body = JSONObject().put("request", request).toString()
            connection.outputStream.use { it.write(body.toByteArray(Charsets.UTF_8)) }

            val responseCode = connection.responseCode
            val stream = if (responseCode in 200..299) {
                connection.inputStream
            } else {
                connection.errorStream
            }

            val response = stream?.bufferedReader(Charsets.UTF_8)?.use { it.readText() } ?: ""
            if (responseCode !in 200..299) {
                throw IllegalStateException("Worker API HTTP $responseCode: $response")
            }
            WorkerResponse(response)
        } finally {
            connection.disconnect()
        }
    }
}
