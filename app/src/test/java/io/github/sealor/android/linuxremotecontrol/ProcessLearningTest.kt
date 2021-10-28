package io.github.sealor.android.linuxremotecontrol

import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.Test
import java.io.BufferedReader
import java.io.BufferedWriter
import java.io.InputStreamReader
import java.io.OutputStreamWriter

class ProcessLearningTest {

    @Test
    fun testRunProcess() {
        val process = Runtime.getRuntime().exec("sh")
        val stdinWriter = BufferedWriter(OutputStreamWriter(process.outputStream))
        val stdoutReader = BufferedReader(InputStreamReader(process.inputStream))
        val stderrReader = BufferedReader(InputStreamReader(process.errorStream))

        stdinWriter.write("echo Hello World\n")
        stdinWriter.flush()
        val stdoutLine = stdoutReader.readLine()

        stdinWriter.write("echo ERROR >&2\n")
        stdinWriter.flush()
        val stderrLine = stderrReader.readLine()

        stdinWriter.write("exit\n")
        stdinWriter.flush()
        process.waitFor()

        assertEquals("Hello World", stdoutLine)
        assertEquals("ERROR", stderrLine)
    }
}