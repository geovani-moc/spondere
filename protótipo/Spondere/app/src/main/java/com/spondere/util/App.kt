package com.spondere.util

import android.content.Context
import com.spondere.R

class App() {
    private lateinit var preferences:Preferences
    private lateinit var userPreferences:Preferences

    fun logout(context: Context){
        preferences = Preferences(context.getString(R.string.settings_login), context)
        userPreferences = Preferences(context.getString(R.string.user_preference), context)

        preferences.saveData(context.getString(R.string.password), "")
        preferences.saveData(context.getString(R.string.user_name), "")
        preferences.saveData(context.getString(R.string.token), "")
        preferences.saveData(context.getString(R.string.expires), "")

        userPreferences.saveData(context.getString(R.string.user_preference), "")
        userPreferences.saveData(context.getString(R.string.disciplines), "")
        userPreferences.saveData(context.getString(R.string.groups), "")

    }

}