package com.spondere.network

import android.content.Context
import android.util.Base64
import com.spondere.R
import org.json.JSONObject

class DecodeToken(private val context: Context, private val token:String) {
    private val TAG = "decode_token"

    var username = ""
        private set
    var expires:Long = 0
        private set

    fun isValidToken(userName:String):Boolean{
        if (!isToken()) return false

        val claims = token.split(".")
        //header = 0, playloads = 1, signuture = 2
        val playloads = String(Base64.decode(claims[1], Base64.URL_SAFE))

        val json = JSONObject(playloads)
        if (!json.has(context.getString(R.string.user_name))) return false
        if (!json.has(context.getString(R.string.expires))) return false

        username = json.getString(context.getString(R.string.user_name))
        expires = json.getDouble(context.getString(R.string.expires)).toLong()

        if (this.username == userName) return true
        return false
    }

    fun isToken():Boolean{
        if(token.isNotEmpty()) return true
        return false
    }
}