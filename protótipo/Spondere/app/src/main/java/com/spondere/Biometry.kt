package com.spondere

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.location.Location
import android.location.LocationManager
import android.os.Bundle
import android.os.SystemClock
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.Toolbar
import androidx.core.view.isVisible
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.spondere.entity.AcademicClass
import com.spondere.entity.Frequency
import com.spondere.entity.User
import com.spondere.util.App
import com.spondere.util.Connection
import com.spondere.util.LoadingDialog
import com.spondere.util.Preferences
import java.io.ByteArrayOutputStream
import java.text.SimpleDateFormat
import java.util.*
import com.spondere.network.AcademicClass as ClassDB
import com.spondere.network.BiometryImage as BiometryDB
import com.spondere.network.Frequency as FrequencyDB

class Biometry : AppCompatActivity() {
    private var academicClass: AcademicClass? = null
    private lateinit var textView_className: TextView
    private lateinit var imageView_frequencyStatus: ImageView
    private lateinit var textView_classDescription: TextView
    private lateinit var textView_schedule: TextView
    private lateinit var textView_attendanceDescription: TextView
    private lateinit var button_takePicture: Button
    private lateinit var token:String
    private lateinit var preferences:Preferences
    private val PERMISSION_CODE: Int = 1000
    private var TAG = "biometry"
    private var classID:Int? = null
    private val databaseTimePattern = "yyyy-MM-dd'T'HH:mm:ssZ"
    private val displayTimePattern = "dd/MM/yyyy HH:mmZ"
    private lateinit var classDB: ClassDB
    private var latitude:Double = 0.0
    private var longitude:Double = 0.0
    private lateinit var username:String
    private lateinit var userPreferences:Preferences
    private lateinit var user:User
    private val mapper = jacksonObjectMapper()
    private lateinit var biometryDB:BiometryDB
    private lateinit var frequencyDB:FrequencyDB
    private lateinit var toolbar: Toolbar
    private val app = App()
    private var autoTakePhoto = false
    private lateinit var locationManager:LocationManager
    private var location:Location? = null
    private lateinit var loadingDialog: LoadingDialog
    private var lastClickTime: Long = 0
    private var studentAlreadyPresent = false

    private val PRESENT = 1
    private val FREQUENCY_NOT_BEGIN = 2
    private val NOT_PRESENT = 3

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_biometry)

        loadPermissions()
        readPreferences()
        loadObjects()
        setObjects()
        loadAppBar()
    }

    private val listener = View.OnClickListener { view ->
        when(view.id){
            R.id.button_takePicture -> {
                if ( SystemClock.elapsedRealtime() - lastClickTime < 1000) return@OnClickListener
                lastClickTime = SystemClock.elapsedRealtime()
                takePicture()
            }
        }
    }

    private fun readPreferences(){
        preferences = Preferences(getString(R.string.settings_login), this)
        userPreferences = Preferences(getString(R.string.user_preference), this)

        token = preferences.loadData(getString(R.string.token)).toString()
        username = preferences.loadData(getString(R.string.user_name)).toString()

        academicClass = intent.extras?.get(getString(R.string.academic_class)) as? AcademicClass
        classID = intent.extras?.get("classID") as? Int

        if (academicClass == null){
            autoTakePhoto = true
        }

        biometryDB = BiometryDB(this, token)
        classDB = ClassDB(this, token)
        frequencyDB = FrequencyDB(this, token)

        val userJson = userPreferences.loadData(getString(R.string.user_preference))
        if (userJson.isNullOrEmpty()){
            app.logout(this)
            Toast.makeText(this, "Dados de usuários vazios, faça login novamente.", Toast.LENGTH_LONG).show()
        }
        user = mapper.readValue(userJson, User::class.java)

        if (academicClass == null && classID == null) {
            Log.e(TAG, "Não existe informação da aula.")
            finish()
        }
        if (classID == null){
            classID = academicClass?.id
        }

        if (academicClass == null){
            if (!Connection().isOnline(this)){
                dialogError(getString(R.string.error_connect))
                return
            }
            try { academicClass = classDB.read(classID!!)
            }catch (e:Exception){
                Log.e(TAG, "Erro ao buscar a aula id:${classID}.\n $e")
            }
        }
    }

    private fun loadObjects(){
        textView_attendanceDescription = findViewById(R.id.textView_attendanceDescription)
        textView_classDescription = findViewById(R.id.textView_classDescription)
        textView_className = findViewById(R.id.textView_className)
        textView_schedule = findViewById(R.id.textView_schedule)
        button_takePicture = findViewById(R.id.button_takePicture)
        imageView_frequencyStatus = findViewById(R.id.imageView_frequencyStatus)
        loadingDialog = LoadingDialog(this)
        locationManager = applicationContext.getSystemService(LOCATION_SERVICE) as LocationManager
    }

    private fun setObjects(){
        button_takePicture.setOnClickListener(listener)
        if (academicClass == null) return
        textView_className.text = academicClass!!.titleClass
        textView_classDescription.text = academicClass!!.descriptionClass
        if (academicClass!!.beginDate.isNullOrBlank()) return
        if (academicClass!!.endDate.isNullOrBlank()) return

        val (year, month, day) = getDate(academicClass!!.beginDate!!, databaseTimePattern)
        val (beginHours, beginMinutes) = getTime(academicClass!!.beginDate!!, databaseTimePattern)
        val (hours, minutes) = getTime(academicClass!!.endDate!!, databaseTimePattern)

        var schedule = "Dia: ${day}/${month}/${year}"
        schedule = "$schedule \nHorário do início da aula:${beginHours}:${beginMinutes}"
        schedule = "$schedule \nHorário do fim da aula:${hours}:${minutes}"
        textView_schedule.text=schedule

        if(!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return
        }
        Thread(Runnable {
            try {
                runOnUiThread { loadingDialog.startLoadingDialog() }
                val (presence, buttonVisibility, status) = frequencyStatus()
                runOnUiThread {
                    textView_attendanceDescription.text = presence
                    button_takePicture.isEnabled = buttonVisibility
                    //button_takePicture.isVisible = buttonVisibility

                }
                when(status){
                    PRESENT -> imageView_frequencyStatus.setImageResource(R.drawable.icon_is_present_foreground)
                    NOT_PRESENT -> imageView_frequencyStatus.setImageResource(R.drawable.icon_is_not_present_foreground)
                    FREQUENCY_NOT_BEGIN -> imageView_frequencyStatus.setImageResource(R.drawable.ic_info)
                    else -> imageView_frequencyStatus.setImageResource(R.drawable.ic_info)
                }
            }
            catch (e:Exception){Log.e(TAG, "Erro ao buscar o status da frequência: $e")}
            finally { runOnUiThread { loadingDialog.dismissDialog() } }
            initBiometry()
        }).start()
    }

    private fun initBiometry(){
        if (academicClass == null) return
        if (!autoTakePhoto) return
        if (academicClass!!.blockedAttendance)return
        if (!academicClass!!.activeValidation) return
        if (academicClass!!.validationCode.isNullOrBlank()) return
        if (academicClass!!.validationCode!!.length != 10) return
        if (studentAlreadyPresent) {
            runOnUiThread { Toast.makeText(this,
                "Você já tem presença nesta aula.",
                Toast.LENGTH_LONG).show() }
            return
        }
        if (!checkPermissionsDenied()) {
            registerCamera.launch(null)
        } else{
            val permission: Array<String> = getListPermissions()
            runOnUiThread {
                Toast.makeText(this,
                    "Todas as permissões são necessárias para a validação.",
                    Toast.LENGTH_SHORT).show()
                requestPermissions(permission, PERMISSION_CODE)
                if (!academicClass!!.validationCode.isNullOrBlank()){
                    button_takePicture.isEnabled = true
                    button_takePicture.isVisible = true
                }
            }
        }
    }

    private fun frequencyStatus():Triple<String, Boolean, Int>{
        var presence = ""
        var buttonVisibility = false
        var status = -1

        try {
            val (id, failure) = frequencyDB.isPresent(academicClass!!.id, user.id!!)

            if (!academicClass!!.activeValidation) {
                presence = "A aula ainda não foi iniciada."
                buttonVisibility= false
                status = FREQUENCY_NOT_BEGIN
            }else if(academicClass!!.activeValidation && !academicClass!!.blockedAttendance) {
                if (id < 1){
                    presence= "Aula já iniciou, você ainda não tem frequência nesta aula. " +
                            "Caso tenha enviado foto para análise, verifique mais tarde. "
                    buttonVisibility= false
                    status = NOT_PRESENT
                }else if (id>0 && !failure.isNullOrBlank()){
                    if (biometricsIsEnable()){
                        presence= "Envie outra foto:\n$failure"
                        buttonVisibility= true
                        status = NOT_PRESENT
                    }else{
                        presence= "A aula já se encerrou e a sua tentativa falhou:\n$failure"
                        buttonVisibility= false
                        status = NOT_PRESENT
                    }
                }else if (id > 0 && failure.isNullOrBlank()){
                    presence= "A sua frequência está confirmada nesta aula. "
                    buttonVisibility= false
                    status = PRESENT
                }
            }else if(academicClass!!.activeValidation && academicClass!!.blockedAttendance){
                if (id > 0){
                    if(failure.isNullOrBlank()){
                        status = PRESENT
                        presence = "A sua frequência nesta aula foi confirmada. "
                    }else{
                        status = NOT_PRESENT
                        presence = "Aula já encerrou, você não tem frequência nesta aula. " +
                                "Sua tentativa de comprovação biométrica falhou e o " +
                                "horário para nova tentativa já se encerrou."
                    }
                    buttonVisibility= false
                }else{
                    presence= "A aula já encerrou e você não tem frequência nesta aula."
                    status = NOT_PRESENT
                    buttonVisibility= false
                }
            }else{
                presence= "Sem dados de sua frequência."
                buttonVisibility= false
                status = NOT_PRESENT
            }
        }catch (e:Exception){
            Log.e(TAG, "Nenhum dado de frequência encontrado: $e")
            presence = "Erro do servidor ao verificar a frequência."
            status = NOT_PRESENT
            //button_takePicture.isVisible = false
            button_takePicture.isEnabled = false
        }
        studentAlreadyPresent = (status == PRESENT)
        return Triple(presence, buttonVisibility, status)
    }

    private fun getDate(date:String, pattern:String):Triple<String, String, String>{
        val calendar = Calendar.getInstance()
        calendar.time = SimpleDateFormat(pattern).parse(date)

        val year = String.format("%04d", calendar.get(Calendar.YEAR))
        val month = String.format("%02d", calendar.get(Calendar.MONTH)+1)
        val day = String.format("%02d", calendar.get(Calendar.DAY_OF_MONTH))

        return Triple(year, month, day)
    }

    private fun getTime(date:String, pattern:String):Pair<String, String>{
        val calendar = Calendar.getInstance()
        calendar.time = SimpleDateFormat(pattern).parse(date)

        val hours:String = String.format("%02d", calendar.get(Calendar.HOUR_OF_DAY))
        val minutes:String = String.format("%02d", calendar.get(Calendar.MINUTE))

        return Pair(hours, minutes)
    }

    fun takePicture() {
        if (!biometricsIsEnable()){
            dialogError("A aula já passou do horário de encerramento.")
            button_takePicture.isEnabled = false
            return
        }
        if (!checkPermissionsDenied()) {
            button_takePicture.isEnabled = false
            //button_takePicture.isVisible = false
            registerCamera.launch(null)
        } else{
            Toast.makeText(this, "Todas as permissões são necessárias para a validação.", Toast.LENGTH_SHORT).show()
            val permission: Array<String> = getListPermissions()
            requestPermissions(permission, PERMISSION_CODE)
        }
    }

    private val registerCamera = registerForActivityResult(
        ActivityResultContracts.TakePicturePreview()
    ) { image: Bitmap? ->
        if (image == null) {
            Log.v(TAG, "A imagem está vazia.")
            return@registerForActivityResult
        }

        try {
            location = locationManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER)
            longitude = location?.longitude ?: 0.0
            latitude = location?.latitude ?: 0.0
        } catch(ex: SecurityException) {
            longitude = 0.0
            latitude = 0.0
            Log.d(TAG, "Erro a localização não está disponível")
        }
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return@registerForActivityResult
        }
        Thread(Runnable {
            try {
                runOnUiThread { loadingDialog.startLoadingDialog() }
                val out = ByteArrayOutputStream()
                image.compress(Bitmap.CompressFormat.JPEG, 95, out)
                val imageByteArray: ByteArray = out.toByteArray()
                val frequency = Frequency(
                    id = null, studentID = user.id!!, academicClassID = classID!!,
                    ManualAttendance = false, BLEAttendance = academicClass!!.validationByBLE,
                    QrCodeAttendance = academicClass!!.validationByQrCode,
                    validationCode = academicClass!!.validationCode!!, latitude = latitude,
                    longitude = longitude, photo = null, createDate = null, failure = null
                )

                val result = biometryDB.checkImage(imageByteArray, frequency)
                runOnUiThread {
                    Toast.makeText(this, result, Toast.LENGTH_LONG).show()
                    textView_attendanceDescription.text = "Imagem em análise, aguarde (atualize a página após alguns instantes)."
                    imageView_frequencyStatus.setImageResource(R.drawable.ic_info)
                }
            }catch (e:Exception){
                runOnUiThread {
                    Log.e(TAG, "Erro ao enviar imagem: $e")
                    Toast.makeText(this, "Erro ao enviar a imagem.", Toast.LENGTH_LONG).show()
                }
            }finally {
                runOnUiThread { loadingDialog.dismissDialog() }
            }
        }).start()
    }

    private fun loadAppBar(){
        toolbar = findViewById(R.id.topAppBar)
        toolbar.setOnMenuItemClickListener {menuItem ->
            when (menuItem.itemId) {
                R.id.edit -> {
                    if ( SystemClock.elapsedRealtime() - lastClickTime < 1000)
                        return@setOnMenuItemClickListener true
                    lastClickTime = SystemClock.elapsedRealtime()

                    intent = Intent(this, Account::class.java)
                    startActivity(intent)
                    true
                }
                R.id.refresh -> {
                    refreshInfos()
                    true
                }
                else -> false
            }
        }
    }

    private fun checkPermissionsDenied():Boolean{
        if (checkSelfPermission(Manifest.permission.CAMERA) == PackageManager.PERMISSION_DENIED) return true
        if (checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_DENIED) return true
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_DENIED) return true
        if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_DENIED) return true

        return false
    }

    private fun getListPermissions(): Array<String> {
        return arrayOf(
            Manifest.permission.CAMERA,
            Manifest.permission.ACCESS_COARSE_LOCATION,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
        )
    }

    private fun loadPermissions(){
        if (checkPermissionsDenied()) {
            val permission: Array<String> = getListPermissions()
            requestPermissions(permission, PERMISSION_CODE)
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

    private fun refreshInfos(){
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return
        }
        var academicClassID:Int  = -1
        if (classID != null){
            academicClassID = classID as Int
        }else if (academicClass != null){
            academicClassID = academicClass!!.id
        }

        Thread(Runnable {
            var updated = false
            try {
                runOnUiThread { loadingDialog.startLoadingDialog() }
                academicClass = classDB.read(academicClassID)

                runOnUiThread {
                    textView_className.text = academicClass!!.titleClass
                    textView_classDescription.text = academicClass!!.descriptionClass
                    if (academicClass!!.beginDate.isNullOrBlank()) { return@runOnUiThread }
                    if (academicClass!!.endDate.isNullOrBlank()) { return@runOnUiThread }

                    val (year, month, day) = getDate(academicClass!!.beginDate!!, databaseTimePattern)
                    val (beginHours, beginMinutes) = getTime(academicClass!!.beginDate!!, databaseTimePattern)
                    val (hours, minutes) = getTime(academicClass!!.endDate!!, databaseTimePattern)

                    var schedule = "Dia: ${day}/${month}/${year}"
                    schedule = "$schedule \nHorário do início da aula:${beginHours}:${beginMinutes}"
                    schedule = "$schedule \nHorário do fim da aula:${hours}:${minutes}"
                    textView_schedule.text=schedule
                }
                updated = true
            }catch (e:Exception){
                Log.e(TAG, "Erro ao buscar a aula id:${classID}.\n $e")
                updated = false
            }finally {
                runOnUiThread { loadingDialog.dismissDialog() }
            }
            if(updated){
                runOnUiThread {
                    Toast.makeText(this, "Informações atualizadas.", Toast.LENGTH_SHORT).show()
                }
            }
            try {
                val (presence, buttonVisibility, status) = frequencyStatus()
                runOnUiThread {
                    textView_attendanceDescription.text = presence
                    button_takePicture.isEnabled = buttonVisibility
                    //button_takePicture.isVisible = buttonVisibility
                    when(status){
                        PRESENT -> imageView_frequencyStatus.setImageResource(R.drawable.icon_is_present_foreground)
                        NOT_PRESENT -> imageView_frequencyStatus.setImageResource(R.drawable.icon_is_not_present_foreground)
                        FREQUENCY_NOT_BEGIN -> imageView_frequencyStatus.setImageResource(R.drawable.ic_info)
                        else -> imageView_frequencyStatus.setImageResource(R.drawable.ic_info)
                    }
                }
            }catch (e:Exception){
                Log.e(TAG, "Erro ao capturar o status da frequência: $e")
            }
        }).start()
    }

    private fun biometricsIsEnable():Boolean{
        if (academicClass!!.endDate.isNullOrBlank()) return false
        val dateFormat = SimpleDateFormat(databaseTimePattern)
        val rightNow = Calendar.getInstance()
        val result:Boolean = try {
            val endDate = dateFormat.parse(academicClass!!.endDate)
            endDate > rightNow.time
        }catch (e:Exception){
            Log.e(TAG, "Erro ao comparar datas: $e")
            false
        }
        return result
    }
}