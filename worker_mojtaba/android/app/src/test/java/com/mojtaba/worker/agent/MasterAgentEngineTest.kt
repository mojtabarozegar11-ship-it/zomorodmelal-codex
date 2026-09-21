package com.mojtaba.worker.agent

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class MasterAgentEngineTest {
    @Test
    fun submitCreatesSafeLocalMission() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        val result = MasterAgentEngine(context).submit("تست محلی")
        assertEquals("planned", result.status)
        assertTrue(result.data.getJSONObject("safety").getBoolean("sandbox_only"))
        assertFalse(result.data.getJSONObject("execution").getBoolean("real_world_action"))
        assertTrue(engineStatusIsLocal(context))
    }

    private fun engineStatusIsLocal(context: Context): Boolean =
        MasterAgentEngine(context).status().getString("runtime") == "zomorodmelal-android-local"
}
