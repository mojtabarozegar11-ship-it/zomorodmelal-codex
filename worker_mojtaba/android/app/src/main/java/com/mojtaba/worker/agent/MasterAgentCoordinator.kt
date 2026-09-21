package com.mojtaba.worker.agent

import android.content.Context
import android.content.SharedPreferences
import com.mojtaba.worker.BuildConfig
import com.mojtaba.worker.network.WorkerApiClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class MasterAgentCoordinator(private val context: Context) {
    private val engine = MasterAgentEngine(context.filesDir)
    private val prefs: SharedPreferences = context.getSharedPreferences("worker_settings", Context.MODE_PRIVATE)

    private fun apiClient(): WorkerApiClient {
        val configured = prefs.getString("worker_api_base_url", BuildConfig.WORKER_API_BASE_URL).orEmpty()
        return WorkerApiClient(configured)
    }

    fun setApiBaseUrl(url: String) {
        prefs.edit().putString("worker_api_base_url", url.trim()).apply()
    }

    fun getApiBaseUrl(): String =
        prefs.getString("worker_api_base_url", BuildConfig.WORKER_API_BASE_URL).orEmpty()

    suspend fun submit(goal: String): AgentResult = withContext(Dispatchers.IO) {
        val clean = goal.trim()
        require(clean.isNotEmpty()) { "درخواست خالی است." }
        runCatching {
            val remote = apiClient().sendTask(clean)
            engine.recordRemoteSuccess(clean)
            AgentResult(
                status = "completed",
                message = remote.message(),
                data = JSONObjectBridge.fromRaw(remote.rawJson)
            )
        }.getOrElse {
            engine.recordRemoteFailure(clean, it.message ?: "خطای ارتباط با سرویس")
            engine.submit(clean)
        }
    }

    suspend fun submitVoice(file: java.io.File, request: String = ""): AgentResult = withContext(Dispatchers.IO) {
        runCatching {
            val remote = apiClient().sendVoice(file, request)
            AgentResult(
                status = "completed",
                message = remote.message(),
                data = JSONObjectBridge.fromRaw(remote.rawJson)
            )
        }.getOrElse {
            AgentResult(
                status = "error",
                message = it.message ?: "پردازش صوت ناموفق بود.",
                data = org.json.JSONObject().put("error", it.message ?: "unknown")
            )
        }
    }

    suspend fun cycle(goal: String? = null): AgentResult = withContext(Dispatchers.IO) {
        engine.runCycle(goal)
    }

    fun status() = engine.status()

    private object JSONObjectBridge {
        fun fromRaw(raw: String): org.json.JSONObject =
            runCatching { org.json.JSONObject(raw) }.getOrElse { org.json.JSONObject().put("raw", raw) }
    }
}