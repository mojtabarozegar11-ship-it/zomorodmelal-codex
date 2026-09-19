package com.mojtaba.worker.voice

import android.media.MediaPlayer
import java.io.File

class VoicePlayer {
    private var player: MediaPlayer? = null

    fun play(file: File) {
        stop()
        player = MediaPlayer().apply {
            setDataSource(file.absolutePath)
            setOnCompletionListener { stop() }
            prepare()
            start()
        }
    }

    fun stop() {
        player?.runCatching { stop() }
        player?.release()
        player = null
    }
}