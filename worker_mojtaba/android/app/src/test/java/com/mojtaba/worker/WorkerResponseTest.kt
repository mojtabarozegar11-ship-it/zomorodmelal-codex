package com.mojtaba.worker

import com.mojtaba.worker.network.WorkerResponse
import org.junit.Assert.assertEquals
import org.junit.Test

class WorkerResponseTest {
    @Test
    fun executionMessageIsPreferred() {
        val response = WorkerResponse("""{"status":"planned","execution":{"message":"انجام شد"}}""")
        assertEquals("انجام شد", response.message())
    }

    @Test
    fun statusIsUsedWhenNoMessageExists() {
        val response = WorkerResponse("""{"status":"provider_configuration_required"}""")
        assertEquals("provider_configuration_required", response.message())
    }
}
