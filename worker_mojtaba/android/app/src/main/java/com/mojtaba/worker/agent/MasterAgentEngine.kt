package com.mojtaba.worker.agent

import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.util.concurrent.atomic.AtomicLong

data class AgentResult(
    val status: String,
    val message: String,
    val data: JSONObject
)

class MasterAgentEngine(private val rootDir: File) {
    private val stateFile = File(rootDir, "master_agent_state.json")
    private val missionFile = File(rootDir, "master_agent_missions.json")
    private val sequence = AtomicLong(loadState().optLong("sequence", 0L))

    @Synchronized
    fun status(): JSONObject {
        val state = loadState()
        return JSONObject(state.toString()).apply {
            put("runtime", "zomorodmelal-android-local")
            put("version", "1.0.0")
            put("execution_mode", "device_local_safe")
            put("owner_approval_required", true)
            put("real_world_execution", false)
        }
    }

    @Synchronized
    fun submit(goal: String): AgentResult {
        val clean = goal.trim()
        require(clean.isNotEmpty()) { "درخواست خالی است." }
        val id = sequence.incrementAndGet()
        val mission = JSONObject()
            .put("id", id)
            .put("goal", clean)
            .put("status", "planned")
            .put("created_at", System.currentTimeMillis())
            .put("phase", "observe")
            .put("owner_approval_required", true)
            .put("real_world_execution", false)

        val queue = loadMissions()
        queue.put(mission)
        saveMissions(queue)

        val currentState = loadState()
        val state = currentState
            .put("sequence", id)
            .put("last_goal", clean)
            .put("last_mission_id", id)
            .put("phase", "next_goal")
            .put("cycles", currentState.optLong("cycles", 0L) + 1L)
        saveState(state)

        val response = JSONObject()
            .put("status", "planned")
            .put("message", "مأموریت محلی ثبت و برای اجرا در محیط امن آماده شد.")
            .put("mission_id", id)
            .put("goal", clean)
            .put("execution", JSONObject()
                .put("status", "sandbox_planned")
                .put("safe", true)
                .put("real_world_action", false))
            .put("safety", JSONObject()
                .put("sandbox_only", true)
                .put("generated_code_executed", false)
                .put("remote_site_write", false)
                .put("real_deployment", false)
                .put("owner_approval_required", true))
        return AgentResult("planned", response.getString("message"), response)
    }

    @Synchronized
    fun runCycle(goal: String? = null): AgentResult {
        if (!goal.isNullOrBlank()) return submit(goal)
        val queue = loadMissions()
        val current = if (queue.length() > 0) queue.getJSONObject(queue.length() - 1) else null
        val response = JSONObject(status().toString()).apply {
            put("cycle_action", "observe_diagnose_prioritize_plan_verify")
            put("current_mission", current ?: JSONObject.NULL)
            put("execution", JSONObject()
                .put("status", "sandbox_planned")
                .put("safe", true)
                .put("real_world_action", false))
        }
        return AgentResult("ready", "هسته محلی آماده است.", response)
    }

    @Synchronized
    private fun loadState(): JSONObject = runCatching {
        if (stateFile.exists()) JSONObject(stateFile.readText()) else JSONObject()
    }.getOrElse { JSONObject() }

    private fun saveState(value: JSONObject) {
        rootDir.mkdirs()
        stateFile.writeText(value.toString(2))
    }

    private fun loadMissions(): JSONArray = runCatching {
        if (missionFile.exists()) JSONArray(missionFile.readText()) else JSONArray()
    }.getOrElse { JSONArray() }

    private fun saveMissions(value: JSONArray) {
        rootDir.mkdirs()
        missionFile.writeText(value.toString(2))
    }
}
