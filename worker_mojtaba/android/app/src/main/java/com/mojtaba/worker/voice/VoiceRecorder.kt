package com.mojtaba.worker.voice

import android.content.Context
import android.media.MediaRecorder
import java.io.File

class VoiceRecorder(private val context: Context) {
    private var recorder: MediaRecorder? = null
    private var output: File? = null

    fun start(): File {
        check(recorder == null) { "recording_in_progress" }
        val file = File.createTempFile("worker_voice_", ".m4a", context.cacheDir)
        MediaRecorder(context).also { r ->
            r.setAudioSource(MediaRecorder.AudioSource.MIC)
            r.setOutputFormat(MediaRecorder.OutputFormat.MPEG_4)
            r.setAudioEncoder(MediaRecorder.AudioEncoder.AAC)
            r.setOutputFile(file.absolutePath)
            r.prepare()
            r.start()
            recorder = r
        }
        output = file
        return file
    }

    fun stop(): File {
        val r = recorder ?: error("recording_not_started")
        val file = output ?: error("recording_file_missing")
        r.stop()
        r.release()
        recorder = null
        output = null
        return file
    }

    fun cancel() {
        recorder?.runCatching { stop() }?.onFailure { release() }
        recorder = null
        output?.delete()
        output = null
    }
}