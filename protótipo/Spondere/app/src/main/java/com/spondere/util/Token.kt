package com.spondere.util

import android.content.Context
import android.util.Log
import com.spondere.R
import com.spondere.network.DecodeToken
import com.spondere.network.Authenticate
import java.util.*

class Token(val context: Context) {
    private val authenticate = Authenticate(context)
    private val TAG = "toke_renovação"
    private val preferences = Preferences(context.getString(R.string.settings_login), context)
    private val userName = preferences.loadData(context.getString(R.string.user_name))
    private val password = preferences.loadData(context.getString(R.string.password))

    private fun renewToken(): Boolean{
        if (userName == null || password == null) return false

        val (newToken, detail) = try {
             authenticate.loginJWT(userName, password)
        }catch (e: Exception){
            Log.e(TAG, "falha de autenticação: $e")
            Pair("","Erro de autenticação.")
        }
        if (detail.isNotBlank()) return false
        if (newToken.isBlank()) return false

        val tokenDecoded = DecodeToken(context, newToken)
        if (tokenDecoded.isValidToken(userName)){
            preferences.saveData(context.getString(R.string.token), newToken)
            preferences.saveData(context.getString(R.string.expires), tokenDecoded.expires.toString())
            return  true
        }

        return false
    }

    fun verify(token:String):Boolean{
        if (isExpired(token)){
            return if (renewToken()){
                Log.v(TAG, "Renovação de token realizada.")
                true
            }else{
                Log.v(TAG, "Erro na renovação de token.")
                App().logout(context)
                false
            }
        }
        return true
    }

    private fun isExpired(token: String):Boolean{
        var expires = (preferences.loadData(context.getString(R.string.expires)))?.toLong()
            ?: return true
        expires *= 1000
        val tokenExpires = Calendar.getInstance()
        tokenExpires.timeInMillis = expires
        val rightNow = Calendar.getInstance()
        rightNow.add(Calendar.DAY_OF_MONTH, 1)
        if (rightNow.time > tokenExpires.time) return true
        return false
    }
}