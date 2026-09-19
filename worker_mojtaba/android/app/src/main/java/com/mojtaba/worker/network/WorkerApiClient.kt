package com.mojtaba.worker.network

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

data class WorkerResponse(val rawJson: String)

class WorkerApiClient(private val baseUrl: String) {
    suspend fun sendTask(request: String): WorkerResponse = withContext(Dispatchers.IO) {
        val connection = (URL(baseUrl.trimEnd('/') + "/v1/tasks").openConnection() as HttpURLConnection)
        try {
            connection.requestMethod = "POST"
            connection.setRequestProperty("Content-Type", "application/json")
            connection.connectTimeout = 10_000
            connection.readTimeout = 60_000
            connection.doOutput = true
            val body = JSONObject().put("request", request).toString()
            connection.outputStream.use { it.write(body.toByteArray(Charsets.UTF_8)) }
            val stream = if (connection.responseCode in 200..299) connection.inputStream else connection.errorStream
            val response = stream.bufferedReader(Charsets.UTF_8).use { it.readText() }
            if (connection.responseCode !in 200..299) {
                throw IllegalStateException("Worker API HTTP ${connection.responseCode}: $response")
            }
            WorkerResponse(response)
        } finally {
            connection.disconnect()
        }
    }
}
