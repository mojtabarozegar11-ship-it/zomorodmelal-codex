package com.mojtaba.worker.agent

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class MasterAgentCoordinator(context: Context) {
    private val engine = MasterAgentEngine(context)

    suspend fun submit(goal: String): AgentResult = withContext(Dispatchers.Default) {
        engine.submit(goal)
    }

    suspend fun cycle(goal: String? = null): AgentResult = withContext(Dispatchers.Default) {
        engine.runCycle(goal)
    }

    fun status() = engine.status()
}
