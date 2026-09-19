package com.mojtaba.worker.voice

import java.io.File

/**
 * Transport boundary for uploading recorded voice and downloading synthesized replies.
 * A concrete HTTPS/API implementation can be injected later without coupling the UI
 * to a particular provider.
 */
interface VoiceMessageTransport {
    suspend fun uploadVoice(file: File): String
    suspend fun downloadVoice(messageId: String, destination: File): File
}
