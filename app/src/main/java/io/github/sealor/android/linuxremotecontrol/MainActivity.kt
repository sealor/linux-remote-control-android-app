package io.github.sealor.android.linuxremotecontrol

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import kotlin.text.Charsets.UTF_8

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        assets.open("uinput_api.py").use {
            Log.i("uinput-api-library", it.readBytes().toString(UTF_8))
        }
    }
}