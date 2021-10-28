package io.github.sealor.android.linuxremotecontrol

import com.jcraft.jsch.ChannelExec
import com.jcraft.jsch.ChannelShell
import com.jcraft.jsch.JSch
import org.apache.sshd.server.SshServer
import org.apache.sshd.server.auth.password.PasswordAuthenticator
import org.apache.sshd.server.auth.pubkey.PublickeyAuthenticator
import org.apache.sshd.server.keyprovider.SimpleGeneratorHostKeyProvider
import org.apache.sshd.server.session.ServerSession
import org.apache.sshd.server.shell.ProcessShellCommandFactory
import org.apache.sshd.server.shell.ProcessShellFactory
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Assertions.assertEquals
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import java.io.*

class JSchLearningTest {

    private var sshd: SshServer? = null

    @BeforeEach
    fun setUp() {
        val sshd = SshServer.setUpDefaultServer()
        sshd.port = 0
        sshd.keyPairProvider = SimpleGeneratorHostKeyProvider()
        sshd.publickeyAuthenticator = PublickeyAuthenticator { username, key, session -> false }
        sshd.passwordAuthenticator =
            PasswordAuthenticator { username: String?, password: String?, serverSession: ServerSession? ->
                username.equals("test") && password.equals("test")
            }
        sshd.commandFactory = ProcessShellCommandFactory()
        sshd.shellFactory = ProcessShellFactory("not relevant", "/bin/bash")
        sshd.start()
        this.sshd = sshd
    }

    @AfterEach
    fun tearDown() {
        this.sshd!!.stop()
    }

    @Test
    fun testSshShellChannel() {
        val port = sshd!!.port

        val session = JSch().getSession("test", "localhost", port)
        session.setPassword("test")
        session.setConfig("StrictHostKeyChecking", "no");
        session.connect()

        val channel = session.openChannel("shell") as ChannelShell
        val pis = PipedInputStream()
        channel.inputStream = pis
        val pos = PipedOutputStream()
        channel.outputStream = pos
        val pes = PipedOutputStream()
        channel.setExtOutputStream(pes)
        channel.connect()

        val stdinWriter = BufferedWriter(OutputStreamWriter(PipedOutputStream(pis)))
        stdinWriter.write("echo Hello World\n")
        stdinWriter.flush()

        val stdoutReader = BufferedReader(InputStreamReader(PipedInputStream(pos)))
        val stdoutLine = stdoutReader.readLine()

        stdinWriter.write("echo ERROR >&2\n")
        stdinWriter.flush()

        val stderrReader = BufferedReader(InputStreamReader(PipedInputStream(pes)))
        val stderrLine = stderrReader.readLine()

        channel.disconnect()
        session.disconnect()

        assertEquals("Hello World", stdoutLine);
        assertEquals("ERROR", stderrLine);
    }

    @Test
    fun testSshExecChannel() {
        val port = sshd!!.port

        val session = JSch().getSession("test", "localhost", port)
        session.setPassword("test")
        session.setConfig("StrictHostKeyChecking", "no");
        session.connect()

        val channel = session.openChannel("exec") as ChannelExec
        channel.setCommand("sh -c 'echo Hello World; echo ERROR >&2'")
        val pos = PipedOutputStream()
        channel.outputStream = pos
        val pes = PipedOutputStream()
        channel.setErrStream(pes)
        channel.connect()

        val stdoutReader = BufferedReader(InputStreamReader(PipedInputStream(pos)))
        val stdoutLine = stdoutReader.readLine()

        val stderrReader = BufferedReader(InputStreamReader(PipedInputStream(pes)))
        val stderrLine = stderrReader.readLine()

        channel.disconnect()
        session.disconnect()

        assertEquals("Hello World", stdoutLine);
        assertEquals("ERROR", stderrLine);
    }
}
