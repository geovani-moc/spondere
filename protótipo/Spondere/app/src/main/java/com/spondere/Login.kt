package com.spondere

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import androidx.appcompat.app.AppCompatActivity
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.spondere.entity.User
import com.spondere.network.Authenticate
import com.spondere.network.DecodeToken
import com.spondere.util.Connection
import com.spondere.util.LoadingDialog
import com.spondere.util.Preferences
import com.spondere.network.User as UserDB

class Login : AppCompatActivity() {
    private lateinit var button_login: Button
    private lateinit var editText_userName: EditText
    private lateinit var editText_password: EditText
    private val TAG = "tela_login"
    private lateinit var tokenDecoded:DecodeToken
    private lateinit var preferences:Preferences
    private lateinit var userPreferences:Preferences
    private lateinit var loadingDialog: LoadingDialog
    private lateinit var user:User
    private lateinit var userDB:UserDB
    val mapper = jacksonObjectMapper()
    private lateinit var token: String
    private var experies:Long = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        readPreferences()
        isLoged()
        loadObjects()
    }

    private fun isLoged(){
        var password:String? = null
        var username:String? = null
        try {
            password = preferences.loadData(getString(R.string.password))
            username = preferences.loadData(getString(R.string.user_name))
        }catch (e:Exception){
            Log.e(TAG, "Erro no login automático: $e")
        }finally {
            if (username.isNullOrBlank() || password.isNullOrBlank()) return

            val userJson = userPreferences.loadData(getString(R.string.user_preference))
            if (userJson.isNullOrEmpty()) return
            user = mapper.readValue(userJson, User::class.java)

            when {
                user.professor -> {
                    intent = Intent(this, ProfessorHome::class.java)
                    startActivity(intent)
                }
                user.student -> {
                    intent = Intent(this, StudentHome::class.java)
                    startActivity(intent)
                }
                else -> {
                    return
                }
            }
        }
    }

    private fun readPreferences(){
        preferences = Preferences(getString(R.string.settings_login), this)
        userPreferences = Preferences(getString(R.string.user_preference), this)
    }

    private fun loadObjects(){
        button_login = findViewById(R.id.button_loginButton)
        editText_password = findViewById(R.id.editText_password)
        editText_userName = findViewById(R.id.editText_userName)
        loadingDialog = LoadingDialog(this)
    }

    fun initLogin(view: View) {
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return
        }
        val username = editText_userName.text.toString().trim()
        val password = editText_password.text.toString()

        if (username.isEmpty()) {
            editText_userName.error = "Campo obrigatório."
            return@initLogin
        } else if (password.isEmpty()) {
            editText_password.error = "Campo obrigatório."
            return@initLogin
        }

        Thread(Runnable {
            runOnUiThread{loadingDialog.startLoadingDialog()}
            makeLogin(username, password)
        }).start()
    }

    private fun makeLogin(username:String, password:String){
        var detail = ""
        try {
            val (tempToken, tempDetail) = Authenticate(this).loginJWT(username, password)
            token = tempToken
            detail = tempDetail
        }catch (e: Exception) {
            Log.e(TAG, "$e")
            runOnUiThread{
                loadingDialog.dismissDialog()
                dialogError("Falha de conexão.")
            }
        }

        if (detail == "u001"){
            runOnUiThread{
                loadingDialog.dismissDialog()
                editText_userName.error = "O usuário pode estar incorreto."
                editText_password.error = "A senha pode estar incorreta."
            }
            return
        }

        if (token.isNullOrBlank()){
            runOnUiThread{
                loadingDialog.dismissDialog()
                dialogError("Falha de conexão.")
            }
            return@makeLogin
        }
        tokenDecoded = DecodeToken(this, token)

        if (tokenDecoded.isValidToken(username)){
            preferences.saveData(getString(R.string.password), password)
            preferences.saveData(getString(R.string.user_name), username)
            experies = tokenDecoded.expires
            preferences.saveData(getString(R.string.token), token)
            preferences.saveData(getString(R.string.expires), experies.toString())
            initApp(username, password)
        }

    }

    private fun initApp(username:String, password:String){
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return
        }
        userDB = UserDB(this, token)

        val result  = try {
            user = userDB.read()
            var userJson = mapper.writeValueAsString(user)
            userPreferences.saveData(getString(R.string.user_preference), userJson)
            true
        }catch (e: Exception) {
            Log.e(TAG, "$e")
            runOnUiThread{
                loadingDialog.dismissDialog()
                dialogError("Erro de conexão, não foi possível sincronizar informações de usuário.")
            }
            false
        }
        if (!result) return

        when {
            user.professor -> {
                intent = Intent(this, ProfessorHome::class.java)
                startActivity(intent)
            }
            user.student -> {
                intent = Intent(this, StudentHome::class.java)
                startActivity(intent)
            }
            else -> {
                runOnUiThread {
                    loadingDialog.dismissDialog()
                    dialogError("Seu tipo de usuário não é suportado.")
                }
                return
            }
        }
    }

    private fun dialogError(message:String){
        MaterialAlertDialogBuilder(this)
            .setTitle("Erro")
            .setMessage(message)
            .setPositiveButton("OK"
            ) { dialog, which -> dialog?.dismiss() }
            .show()
    }
}