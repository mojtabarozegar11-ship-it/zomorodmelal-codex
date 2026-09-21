package com.mojtaba.worker.agent

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.rules.TemporaryFolder

class MasterAgentEngineTest {
    @get:Rule
    val tempFolder = TemporaryFolder()

    @Test
    fun submitCreatesSafeLocalMission() {
        val result = MasterAgentEngine(tempFolder.root).submit("تست محلی")
        assertEquals("planned", result.status)
        assertTrue(result.data.getJSONObject("safety").getBoolean("sandbox_only"))
        assertFalse(result.data.getJSONObject("execution").getBoolean("real_world_action"))
        assertTrue(
            MasterAgentEngine(tempFolder.root).status()
                .getString("runtime") == "zomorodmelal-android-local"
        )
    }
}
