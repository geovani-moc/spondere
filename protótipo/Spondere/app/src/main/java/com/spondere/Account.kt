package com.spondere

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.SystemClock
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.widget.*
import androidx.activity.result.contract.ActivityResultContracts
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.spondere.entity.User
import com.spondere.util.App
import com.spondere.util.Connection
import com.spondere.util.LoadingDialog
import com.spondere.util.Preferences
import java.io.ByteArrayOutputStream
import com.spondere.network.BiometryImage as BiometryDB

class Account : AppCompatActivity() {
    private val TAG = "tela_account"
    private val PERMISSION_CODE: Int = 1013
    private lateinit var userPreferences:Preferences
    private lateinit var preferences:Preferences
    private val mapper = jacksonObjectMapper()
    private lateinit var user:User
    private lateinit var imageView_biometryStatus:ImageView
    private lateinit var button_logout:Button
    private lateinit var button_registerPhotos:Button
    private lateinit var button_back:ImageButton
    private lateinit var button_refresh:Button
    private lateinit var editText_name:EditText
    private lateinit var editText_email:EditText
    private lateinit var textView_biometryStatus:TextView
    private lateinit var biometryDB:BiometryDB
    private lateinit var token:String
    private var biometryID = 0
    private var biometryError = ""
    private val app = App()
    private var imageByteArray:ByteArray? = null
    private lateinit var loadingDialog: LoadingDialog
    private var lastClickTime: Long = 0
    private var registerFaceImage = false
    private var addFaceImage = false

    private val registerCamera = registerForActivityResult(ActivityResultContracts.TakePicturePreview()) {
            image: Bitmap? ->
        if (image == null) {
            Log.v(TAG, "A imagem esta vazia.")
            return@registerForActivityResult
        }

        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return@registerForActivityResult
        }
        try {
            val out = ByteArrayOutputStream()
            image.compress(Bitmap.CompressFormat.JPEG, 95, out)
            imageByteArray = out.toByteArray()

            if (registerFaceImage){ createBiometry() }
            else if(addFaceImage){ addPhotosInBiometry()}

            textView_biometryStatus.text = "Imagem em análise, aguarde (atualize a página após alguns instantes)."

        }catch (e:Exception){
            Log.e(TAG, "Erro ao capturar imagem: ${e}.")
            Toast.makeText(this, "Erro ao capturar a imagem.", Toast.LENGTH_LONG).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_account)

        readPreferences()
        loadObjects()
        setObjects()
    }

    private fun loadObjects(){
        button_logout = findViewById(R.id.button_logout)
        editText_name = findViewById(R.id.editText_name)
        editText_email = findViewById(R.id.editText_email)
        textView_biometryStatus = findViewById(R.id.textView_biometryStatus)
        button_registerPhotos = findViewById(R.id.button_registerPhotos)
        imageView_biometryStatus = findViewById(R.id.imageView_biometryStatus1)
        button_back = findViewById(R.id.button_back)
        button_refresh = findViewById(R.id.button_refresh)
        loadingDialog = LoadingDialog(this)
    }

    private fun readPreferences(){
        preferences = Preferences(getString(R.string.settings_login), this)
        userPreferences = Preferences(getString(R.string.user_preference), this)
        token = preferences.loadData(getString(R.string.token)).toString()

        val userJson = userPreferences.loadData(getString(R.string.user_preference))
        if (userJson.isNullOrEmpty()){
            app.logout(this)
            Toast.makeText(this, "Dados de usuários vazios, faça login novamente.", Toast.LENGTH_LONG).show()
            intent = Intent(this, Login::class.java)
            startActivity(intent)
            finishAffinity()
        }
        user = mapper.readValue(userJson, User::class.java)
        biometryDB = BiometryDB(this, token)

    }

    private fun setObjects(){
        editText_name.setText(user.fullName)
        editText_email.setText(user.email)
        button_logout.setOnClickListener(listener)
        button_registerPhotos.setOnClickListener(listener)
        button_back.setOnClickListener(listener)
        button_refresh.setOnClickListener(listener)

        val permission: Array<String> = getListPermissions()
        requestPermissions(permission, PERMISSION_CODE)

        Thread(Runnable {
            if(user.student){
                val result = getValidBiometryID()
                biometryID = result.first
                biometryError = result.second
                runOnUiThread { button_registerPhotos.isEnabled = true }

                if (biometryID > 0){
                    registerFaceImage = false
                    addFaceImage = true
                    runOnUiThread {
                        if (
                            biometryError.isNullOrBlank()){textView_biometryStatus.text = "Biometria ativa e válida."
                            imageView_biometryStatus.setImageResource(R.drawable.icon_is_present_foreground)
                        }
                        else{
                            textView_biometryStatus.text = "Biometria inválida. \nCausa: ${biometryError}."
                            imageView_biometryStatus.setImageResource(R.drawable.icon_is_not_present_foreground)
                        }
                    }
                }else{
                    runOnUiThread {
                        textView_biometryStatus.text = "Não foi localizar uma biometria válida."
                        imageView_biometryStatus.setImageResource(R.drawable.ic_info)
                    }
                    registerFaceImage = true
                    addFaceImage = false
                }
            }else{
                runOnUiThread {
                    textView_biometryStatus.text = "Este usuário não necessita de cadastro biométrico."
                    button_registerPhotos.isEnabled = false
                    imageView_biometryStatus.setImageResource(R.drawable.ic_info)
                }
                registerFaceImage = false
                addFaceImage = false

            }
        }).start()
    }

    private val listener = View.OnClickListener { view ->
        when(view.id){
            R.id.button_logout -> {
                app.logout(this)
                intent = Intent(this, Login::class.java)
                startActivity(intent)
                finishAffinity()
            }
            R.id.button_registerPhotos -> {
                if ( SystemClock.elapsedRealtime() - lastClickTime < 1000) return@OnClickListener
                lastClickTime = SystemClock.elapsedRealtime()
                guideRegisterPhotoDialog()
            }
            R.id.button_back -> {
                if ( SystemClock.elapsedRealtime() - lastClickTime < 1000) return@OnClickListener
                lastClickTime = SystemClock.elapsedRealtime()
                onBackPressed()
            }
            R.id.button_refresh -> {
                if ( SystemClock.elapsedRealtime() - lastClickTime < 1000) return@OnClickListener
                lastClickTime = SystemClock.elapsedRealtime()

                refresh()
            }
        }
    }

    private fun getValidBiometryID():Pair<Int, String>{
        if(!this::user.isInitialized) return Pair(0, "")
        if (user.id!! <= 0) return Pair(0, "")
        val result = try {
            biometryDB.checkStatus(user.id!!)
        }catch (e:Exception){
            Log.e(TAG, "Erro ao requisitar o status da biometria: $e")
            Pair(0, "")
        }
        return result
    }

    private fun registerPhoto(){
        if (!checkPermissionsDenied()) {
            registerCamera.launch(null)
        } else{
            Toast.makeText(this, "É necessário o acesso à câmera.", Toast.LENGTH_SHORT).show()
            val permission: Array<String> = getListPermissions()
            requestPermissions(permission, PERMISSION_CODE)
        }
    }

    private fun createBiometry() {
        Thread(Runnable{
            if (imageByteArray == null) return@Runnable
            if (!Connection().isOnline(this)){
                runOnUiThread { dialogError(getString(R.string.error_connect)) }
                return@Runnable
            }
            try {
                runOnUiThread { loadingDialog.startLoadingDialog() }
                val images = arrayListOf(imageByteArray!!)
                biometryID = biometryDB.create(user.id!!, images)
                runOnUiThread { Toast.makeText(this, "Sua foto está em análise.", Toast.LENGTH_SHORT).show() }
            }catch (e:Exception){
                Log.e(TAG, "Erro ao enviar foto para a criação de dados biométricos: $e")
            }finally {
                runOnUiThread { loadingDialog.dismissDialog() }
            }
        }).start()
    }

    private fun addPhotosInBiometry() {
        Thread(Runnable {
            if (imageByteArray == null) return@Runnable
            if (!Connection().isOnline(this)){
                runOnUiThread { dialogError(getString(R.string.error_connect)) }
                return@Runnable
            }
            try {
                runOnUiThread { loadingDialog.startLoadingDialog() }
                val images = arrayListOf(imageByteArray!!)
                biometryDB.addPhotoInValidBiometry(biometryID, images)
                runOnUiThread { Toast.makeText(this, "Sua foto está em análise.", Toast.LENGTH_LONG).show() }
            }catch (e:Exception){
                Log.e(TAG, "Erro ao enviar foto para adição de dados biométricos: $e" )
            }finally {
                runOnUiThread { loadingDialog.dismissDialog() }
            }
        }).start()
    }

    private fun dialogError(message:String){
        MaterialAlertDialogBuilder(this)
            .setTitle("Erro")
            .setMessage(message)
            .setPositiveButton("OK"
            ) { dialog, which -> dialog?.dismiss() }
            .show()
    }

    private fun refresh(){
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return
        }
        Thread(Runnable {
            imageByteArray = null

            if(user.student){
                val result = getValidBiometryID()
                biometryID = result.first
                biometryError = result.second
            }
            runOnUiThread{
                setObjects()
                Toast.makeText(this, "Informações atualizadas", Toast.LENGTH_SHORT).show()
            }
        }).start()
    }

    private fun checkPermissionsDenied():Boolean{
        if (checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_DENIED) return true
        return false
    }

    private fun getListPermissions(): Array<String> {

        return arrayOf(
            Manifest.permission.CAMERA
        )
    }

    private fun guideRegisterPhotoDialog(){
        val userKey = "${user.id}_hide_guide_send_photo"
        val showGuide = userPreferences.loadData(userKey)
        if (!showGuide.isNullOrBlank() && showGuide == "true"){
            registerPhoto()
            return
        }

        val tutorial = MaterialAlertDialogBuilder(this)
        val layoutView = LayoutInflater.from(this).inflate(R.layout.biometry_tutorial, null)

        tutorial.setView(layoutView)
            .setTitle("Atenção")
            .setCancelable(true)
            .setNeutralButton("Não exibir novamente") { dialog, which ->
                userPreferences.saveData(userKey, "true")
                registerPhoto()
            }
            .setPositiveButton("OK"){ dialog, which ->
                registerPhoto()
               Log.i(TAG,"continuar exibindo guia")
            }.show()
    }
}
