package com.mojtaba.worker.agent

import androidx.test.core.app.ApplicationProvider
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class MasterAgentEngineTest {
    @Test
    fun submitCreatesSafeLocalMission() {
        val context = ApplicationProvider.getApplicationContext<android.content.Context>()
        val engine = MasterAgentEngine(context)
        val result = engine.submit("تست محلی")
        assertEquals("planned", result.status)
        assertTrue(result.data.getJSONObject("safety").getBoolean("sandbox_only"))
        assertTrue(!result.data.getJSONObject("execution").getBoolean("real_world_action"))
    }
}
