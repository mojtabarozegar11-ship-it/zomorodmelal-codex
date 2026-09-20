package com.mojtaba.worker.scheduler

import android.content.Context
import androidx.work.*
import java.util.UUID
import java.util.concurrent.TimeUnit

object WorkerTaskScheduler {
    fun schedulePeriodic(context: Context, taskId: String, intervalHours: Long): UUID {
        require(intervalHours >= 1)
        val request = PeriodicWorkRequestBuilder<ApiTaskWorker>(
            intervalHours, TimeUnit.HOURS
        ).setInputData(workDataOf("task_id" to taskId))
         .setConstraints(Constraints.Builder().setRequiredNetworkType(NetworkType.CONNECTED).build())
         .build()
        WorkManager.getInstance(context).enqueueUniquePeriodicWork(
            "worker-task-$taskId", ExistingPeriodicWorkPolicy.UPDATE, request
        )
        return request.id
    }

    fun cancel(context: Context, taskId: String) {
        WorkManager.getInstance(context).cancelUniqueWork("worker-task-$taskId")
    }
}
