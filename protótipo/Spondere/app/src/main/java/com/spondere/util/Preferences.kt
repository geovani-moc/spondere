package com.spondere.util

import android.content.Context
import com.spondere.entity.User

class Preferences(name:String, context: Context) {
    private val context = context
    private val name = name

    public fun saveData(key: String, value:String){
        val sharedPreferences = context.getSharedPreferences(name, Context.MODE_PRIVATE)
        val editor = sharedPreferences.edit()
        editor.apply{
            putString(key, value)
        }.apply()
    }
    public fun loadData(key: String): String? {
        val sharedPreferences = context.getSharedPreferences(name, Context.MODE_PRIVATE)

        return sharedPreferences.getString(key, null)
    }
}