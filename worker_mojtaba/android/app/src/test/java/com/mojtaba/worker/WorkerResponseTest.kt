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
    fun blankRequestIsRejected() {
        val url = "https://example.com"
        val client = com.mojtaba.worker.network.WorkerApiClient(url)
        val thrown = org.junit.Assert.assertThrows(IllegalArgumentException::class.java) {
            kotlinx.coroutines.runBlocking { client.sendTask("   ") }
        }
        assertEquals("درخواست خالی است.", thrown.message)
    }

    @Test
    fun placeholderUrlIsRejected() {
        val client = com.mojtaba.worker.network.WorkerApiClient("https://YOUR_WORKER_API_HOST")
        val thrown = org.junit.Assert.assertThrows(IllegalArgumentException::class.java) {
            kotlinx.coroutines.runBlocking { client.sendTask("سلام") }
        }
        assertEquals("Worker API URL هنوز پیکربندی نشده است.", thrown.message)
    }

    @Test
    fun blankBaseUrlIsRejected() {
        val client = com.mojtaba.worker.network.WorkerApiClient("   ")
        val thrown = org.junit.Assert.assertThrows(IllegalArgumentException::class.java) {
            kotlinx.coroutines.runBlocking { client.sendTask("سلام") }
        }
        assertEquals("Worker API URL تنظیم نشده است.", thrown.message)
    }

    @Test
    fun invalidBaseUrlIsRejected() {
        val client = com.mojtaba.worker.network.WorkerApiClient("not-a-url")
        val thrown = org.junit.Assert.assertThrows(IllegalArgumentException::class.java) {
            kotlinx.coroutines.runBlocking { client.sendTask("سلام") }
        }
        assertEquals("Worker API URL نامعتبر است.", thrown.message)
    }

    @Test
    fun statusIsUsedWhenNoMessageExists() {
        val response = WorkerResponse("""{"status":"provider_configuration_required"}""")
        assertEquals("provider_configuration_required", response.message())
    }
}
