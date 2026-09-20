package com.mojtaba.worker.network

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.File
import java.net.HttpURLConnection
import java.net.URI
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

private const val VOICE_BOUNDARY = "WorkerMojtabaBoundary"
private const val TASK_PATH = "/v1/tasks"
private const val VOICE_PATH = "/v1/voice"

class WorkerApiClient(private val baseUrl: String) {
    private fun configuredBaseUrl(): String {
        require(baseUrl.isNotBlank()) { "Worker API URL تنظیم نشده است." }
        require(!baseUrl.contains("YOUR_WORKER_API_HOST")) { "Worker API URL هنوز پیکربندی نشده است." }
        require(runCatching { URL(baseUrl) }.isSuccess) { "Worker API URL نامعتبر است." }
        val parsed = URI(baseUrl)
        require(parsed.scheme == "https") { "Worker API فقط از HTTPS پشتیبانی می‌کند." }
        require(parsed.userInfo.isNullOrBlank()) { "Worker API URL نباید شامل اطلاعات کاربری باشد." }
        require(parsed.fragment.isNullOrBlank()) { "Worker API URL نباید fragment داشته باشد." }
        return baseUrl.trimEnd('/')
    }

    suspend fun sendVoice(file: File, request: String = ""): WorkerResponse = withContext(Dispatchers.IO) {
        val apiBaseUrl = configuredBaseUrl()
        require(file.exists() && file.length() > 0L) { "فایل صوتی خالی یا نامعتبر است." }

        val boundary = VOICE_BOUNDARY
        val connection = (URL(apiBaseUrl + VOICE_PATH).openConnection() as HttpURLConnection)
        try {
            connection.requestMethod = "POST"
            connection.setRequestProperty("Accept", "application/json")
            connection.setRequestProperty("Content-Type", "multipart/form-data; boundary=$boundary")
            connection.connectTimeout = 10_000
            connection.readTimeout = 60_000
            connection.doOutput = true

            connection.outputStream.use { output ->
                fun writeText(value: String) = output.write(value.toByteArray(Charsets.UTF_8))
                writeText("--$boundary\r\nContent-Disposition: form-data; name=\"request\"\r\n\r\n$request\r\n")
                writeText("--$boundary\r\nContent-Disposition: form-data; name=\"audio\"; filename=\"" + file.name + "\"\r\nContent-Type: audio/mp4\r\n\r\n")
                file.inputStream().use { it.copyTo(output) }
                writeText("\r\n--$boundary--\r\n")
            }

            val responseCode = connection.responseCode
            val stream = if (responseCode in 200..299) connection.inputStream else connection.errorStream
            val response = stream?.bufferedReader(Charsets.UTF_8)?.use { it.readText() } ?: ""
            if (responseCode !in 200..299) throw IllegalStateException("Worker API HTTP $responseCode: $response")
            WorkerResponse(response)
        } finally {
            connection.disconnect()
        }
    }

    suspend fun sendTask(request: String): WorkerResponse = withContext(Dispatchers.IO) {
        val apiBaseUrl = configuredBaseUrl()
        require(request.isNotBlank()) { "درخواست خالی است." }

        val connection = (URL(apiBaseUrl + TASK_PATH).openConnection() as HttpURLConnection)
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
            val stream = if (responseCode in 200..299) connection.inputStream else connection.errorStream
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
