package com.mojtaba.worker.scheduler

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.mojtaba.worker.BuildConfig
import com.mojtaba.worker.network.WorkerApiClient

class ApiTaskWorker(appContext: Context, params: WorkerParameters) :
    CoroutineWorker(appContext, params) {
    override suspend fun doWork(): Result {
        val taskId = inputData.getString("task_id") ?: return Result.failure()
        return try {
            WorkerApiClient(BuildConfig.WORKER_API_BASE_URL)
                .sendTask("اجرای وظیفه زمان‌بندی‌شده: $taskId")
            Result.success()
        } catch (_: Exception) {
            Result.retry()
        }
    }
}
