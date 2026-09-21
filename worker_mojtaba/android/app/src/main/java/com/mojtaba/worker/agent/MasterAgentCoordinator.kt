package com.mojtaba.worker.agent

import android.content.Context
import com.mojtaba.worker.BuildConfig
import com.mojtaba.worker.network.WorkerApiClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class MasterAgentCoordinator(private val context: Context) {
    private val engine = MasterAgentEngine(context.filesDir)
    private val api = WorkerApiClient(BuildConfig.WORKER_API_BASE_URL)

    suspend fun submit(goal: String): AgentResult = withContext(Dispatchers.IO) {
        val clean = goal.trim()
        require(clean.isNotEmpty()) { "درخواست خالی است." }
        runCatching {
            val remote = api.sendTask(clean)
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
            val remote = api.sendVoice(file, request)
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