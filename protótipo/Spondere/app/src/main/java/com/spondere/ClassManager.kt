package com.spondere

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationManager
import android.os.Build
import android.os.Bundle
import android.os.SystemClock
import android.util.Log
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.Toolbar
import com.google.android.material.datepicker.CalendarConstraints
import com.google.android.material.datepicker.DateValidatorPointForward
import com.google.android.material.datepicker.MaterialDatePicker
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.google.android.material.timepicker.MaterialTimePicker
import com.google.android.material.timepicker.TimeFormat
import com.spondere.entity.AcademicClass
import com.spondere.entity.Group
import com.spondere.util.Connection
import com.spondere.util.LoadingDialog
import com.spondere.util.Preferences
import java.io.Serializable
import java.text.SimpleDateFormat
import java.util.*
import com.spondere.network.AcademicClass as AcademicClassDB

class ClassManager : AppCompatActivity() {
    private val PERMISSION_CODE = 1007
    private var academicClass:AcademicClass? = null
    private lateinit var group:Group
    private lateinit var button_saveClassInfo:Button
    private lateinit var editText_class:EditText
    private lateinit var editText_description: EditText
    private lateinit var button_status:Button
    private lateinit var button_beginAttendance:Button
    private lateinit var button_studentList:Button
    private lateinit var button_date:Button
    private lateinit var button_timeBegin: Button
    private lateinit var button_timeEnd:Button
    private lateinit var textView_date:TextView
    private lateinit var textView_timeBegin: TextView
    private lateinit var textView_timeEnd: TextView
    private lateinit var radioButtonBLE: RadioButton
    private lateinit var radioButtonQrCode: RadioButton
    private var newAcademicClass:Boolean = false
    private var ble = false
    private var qrcode = false
    private var longitude:Double = 0.0
    private var latitude:Double = 0.0
    private lateinit var preferences:Preferences
    private val databaseTimePattern = "yyyy-MM-dd'T'HH:mm:ssZ"
    private val displayTimePattern = "dd/MM/yyyy HH:mmZ"
    private val TAG = "tela_class"
    private lateinit var token:String
    private lateinit var academicClassDB:AcademicClassDB
    private lateinit var toolbar: Toolbar
    private lateinit var locationManager:LocationManager
    private var location:Location? = null
    private lateinit var loadingDialog: LoadingDialog
    private var lastClickTime: Long = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_class_manager)

        loadPermissions()
        readPreferences()
        loadObjects()
        setObjects()
        loadAppBar()
        loadAcademicClass()
    }

    override fun onRestart() {
        super.onRestart()
        refreshInfos()
    }

    private fun loadAcademicClass(){
        Thread(Runnable {
            if (!Connection().isOnline(this)){
                dialogError(getString(R.string.error_connect))
            }else {
                try {
                    runOnUiThread { loadingDialog.startLoadingDialog() }
                    if (academicClass!!.id > 0){
                        academicClass = academicClassDB.read(academicClass!!.id)
                        runOnUiThread { setObjects() }
                    }
                }catch (e:Exception) {
                    Log.e(TAG, "Erro ao atualizar a aula no onResume: $e")
                }finally {
                    runOnUiThread { loadingDialog.dismissDialog() }
                }
            }
            runOnUiThread { flowControl() }
        }).start()
    }

    private fun loadObjects(){
        button_saveClassInfo = findViewById(R.id.button_saveClassInfo)
        button_beginAttendance = findViewById(R.id.button_beginAttendance)
        button_status = findViewById(R.id.button_status)
        button_studentList = findViewById(R.id.button_studentsList)
        button_date = findViewById(R.id.button_date)
        button_timeBegin = findViewById(R.id.button_timeBegin)
        button_timeEnd = findViewById(R.id.button_timeEnd)
        editText_class = findViewById(R.id.editText_className)
        editText_description = findViewById(R.id.editText_description)
        textView_date = findViewById(R.id.textView_date)
        textView_timeEnd = findViewById(R.id.textView_timeEnd)
        textView_timeBegin = findViewById(R.id.textView_timeBegin)
        radioButtonBLE = findViewById(R.id.radioMethodBLE)
        radioButtonQrCode = findViewById(R.id.radioMethodQRCode)
        locationManager = applicationContext.getSystemService(LOCATION_SERVICE) as LocationManager
        loadingDialog = LoadingDialog(this)
    }

    private fun readPreferences(){
        academicClass = intent?.extras?.get(getString(R.string.academic_class)) as? AcademicClass
        group = intent.extras!!.get(getString(R.string.group)) as Group
        preferences = Preferences(getString(R.string.settings_login), this)
        token = preferences.loadData(getString(R.string.token)).toString()
        academicClassDB = AcademicClassDB(this, token)
    }

    @SuppressLint("SetTextI18n")
    private fun setObjects(){
        if (academicClass == null){
            newAcademicClass = true
            button_studentList.isEnabled = false
            ble = true
            qrcode = false
            radioButtonBLE.isChecked = ble
            radioButtonQrCode.isChecked = qrcode
            return@setObjects
        }

        ble = academicClass!!.validationByBLE
        qrcode = academicClass!!.validationByQrCode
        editText_class.setText(academicClass!!.titleClass)
        editText_description.setText(academicClass!!.descriptionClass)
        radioButtonBLE.isChecked = academicClass!!.validationByBLE
        radioButtonQrCode.isChecked = academicClass!!.validationByQrCode

        if (!academicClass!!.beginDate.isNullOrBlank()) {
            val (year, month, day) = getDate(academicClass!!.beginDate!!, databaseTimePattern)
            val (beginHours, beginMinutes) = getTime(academicClass!!.beginDate!!, databaseTimePattern)
            textView_date.text = "${day}/${month}/${year}"
            textView_timeBegin.text = "${beginHours}:${beginMinutes}"
        }
        if (!academicClass!!.endDate.isNullOrBlank()) {
            val (hours, minutes) = getTime(academicClass!!.endDate!!, databaseTimePattern)
            textView_timeEnd.text = "${hours}:${minutes}"
        }
    }

    private fun flowControl(){
        if (newAcademicClass || !academicClass!!.activeValidation){
            editText_class.isEnabled = true
            editText_description.isEnabled = true
            button_date.isEnabled = true
            button_timeBegin.isEnabled = true
            button_timeEnd.isEnabled = true
            radioButtonBLE.isEnabled = true
            radioButtonQrCode.isEnabled = false
            button_studentList.isEnabled = false
            button_status.isEnabled = false
            button_saveClassInfo.isEnabled = true
            button_beginAttendance.isEnabled = true
        }else if (!academicClass!!.blockedAttendance){
            editText_class.isEnabled = true
            editText_description.isEnabled = true
            button_date.isEnabled = false
            button_timeBegin.isEnabled = false
            button_timeEnd.isEnabled = false
            radioButtonBLE.isEnabled = false
            radioButtonQrCode.isEnabled = false
            button_studentList.isEnabled = true
            button_status.isEnabled = true
            button_saveClassInfo.isEnabled = true
            button_beginAttendance.isEnabled = false
        }else{
            editText_class.isEnabled = true
            editText_description.isEnabled = true
            button_date.isEnabled = false
            button_timeBegin.isEnabled = false
            button_timeEnd.isEnabled = false
            radioButtonBLE.isEnabled = false
            radioButtonQrCode.isEnabled = false
            button_studentList.isEnabled = true
            button_status.isEnabled = false
            button_saveClassInfo.isEnabled = true
            button_beginAttendance.isEnabled = false
        }
    }

    fun onRadioButtonClicked(view: View) {
        if (view is RadioButton) {
            val checked = view.isChecked

            when (view.getId()) {
                R.id.radioMethodBLE ->
                    if (checked) {
                        ble = true
                        qrcode = false
                    }
                R.id.radioMethodQRCode ->
                    if (checked) {
                        ble = false
                        qrcode = true
                    }
            }
        }
    }

    @SuppressLint("SimpleDateFormat")
    fun setDate(view: View) {
        val rightNow = Calendar.getInstance()
        val calendarConstraintBuilder = CalendarConstraints.Builder()
        calendarConstraintBuilder.setValidator(DateValidatorPointForward.now())

        val selectDate = MaterialDatePicker.Builder.datePicker()
            .setTitleText("Selecione a data da aula")
            .setSelection(MaterialDatePicker.todayInUtcMilliseconds())
            .setCalendarConstraints(calendarConstraintBuilder.build())
            .build()
        selectDate.show(supportFragmentManager, "ClassManager")

        selectDate.addOnPositiveButtonClickListener {
            val date = Date(it)
            val format = SimpleDateFormat("dd/MM/yyyy")

            var hour = String.format("%02d", rightNow.get(Calendar.HOUR_OF_DAY))
            var minute = String.format("%02d", rightNow.get(Calendar.MINUTE))

            format.timeZone = TimeZone.getTimeZone("GMT-0:00")
            textView_date.text = format.format(date)
            textView_timeBegin.text = "${hour}:${minute}"

            val maxHour = rightNow.get(Calendar.HOUR_OF_DAY)
            if (maxHour >= 22){
                textView_timeEnd.text = "23:59"
            }else{
                rightNow.add(Calendar.HOUR_OF_DAY, 2)
                hour = String.format("%02d", rightNow.get(Calendar.HOUR_OF_DAY))
                minute = String.format("%02d", rightNow.get(Calendar.MINUTE))
                textView_timeEnd.text = "${hour}:${minute}"
            }
        }
    }

    @SuppressLint("SetTextI18n")
    fun getTimeBegin(view: View) {
        val selectTimeBegin  = MaterialTimePicker.Builder()
            .setTitleText("Selecione o horário de início")
            .setTimeFormat(TimeFormat.CLOCK_24H)
            .build()

        selectTimeBegin.show(supportFragmentManager, "ClassManager")
        selectTimeBegin.addOnPositiveButtonClickListener {
            val pickedHour = String.format("%02d", selectTimeBegin.hour)
            val pickedMinute = String.format("%02d", selectTimeBegin.minute)
            textView_timeBegin.text = "${pickedHour}:${pickedMinute}"
            textView_timeEnd.text = ""
        }
    }

    private fun timeBeginIsValid(hour:Int, minute:Int):Boolean{
        if (!this::textView_date.isInitialized) return false
        if (textView_date.text.isNullOrBlank()) return false
        val rightNow = Calendar.getInstance()
        val currentHour:Int = rightNow.get(Calendar.HOUR_OF_DAY)
        val currentMinute:Int = rightNow.get(Calendar.MINUTE)
        val currentDay:Int = rightNow.get(Calendar.DAY_OF_MONTH)
        val currentMonth:Int = rightNow.get(Calendar.MONTH)
        val currentYear:Int = rightNow.get(Calendar.YEAR)

        var beginDay = -1
        var beginMonth = -1
        var beginYear = -1

        val isFormated = try {
            val format = SimpleDateFormat("dd/MM/yyyy")
            val time = format.parse(textView_date.text!! as String)
            val calendar = Calendar.getInstance()
            calendar.time = time
            beginDay = calendar.get(Calendar.DAY_OF_MONTH)
            beginMonth = calendar.get(Calendar.MONTH)
            beginYear = calendar.get(Calendar.YEAR)
            true
        }catch (e:Exception){
            Log.e(TAG, "Erro de conversão de datas: $e")
            false
        }
        if (!isFormated) return false
        if (beginYear > currentYear) return true
        if (beginMonth > currentMonth) return true
        if (beginDay > currentDay) return true
        if(currentHour > hour) return false
        if ((currentHour == hour) && (currentMinute > minute)) return false
        return true
    }

    @SuppressLint("SetTextI18n")
    fun getTimeEnd(view: View) {
        val selectTimeEnd  = MaterialTimePicker.Builder()
            .setTitleText("Selecione o horário de inicio")
            .setHour(2)
            .setMinute(0)
            .setTimeFormat(TimeFormat.CLOCK_24H)
            .build()

        selectTimeEnd.show(supportFragmentManager, "ClassManager")
        selectTimeEnd.addOnPositiveButtonClickListener {

            if(timeEndIsValid(selectTimeEnd.hour, selectTimeEnd.minute)){
                val pickedHour = String.format("%02d", selectTimeEnd.hour)
                val pickedMinute = String.format("%02d", selectTimeEnd.minute)
                textView_timeEnd.text = "${pickedHour}:${pickedMinute}"
            }else{
                dialogError("Horário inválido ou" +
                        "\no horário de início de aula ainda não foi informado.")
            }
        }
    }

    private fun timeEndIsValid(hour:Int, minute:Int):Boolean{
        if (!this::textView_timeBegin.isInitialized) return false
        if (textView_timeBegin.text.isNullOrBlank()) return false
        var beginHour = 0
        var beginMinute = 0

        val isFormated = try {
            val format = SimpleDateFormat("HH:mm")
            val time = format.parse(textView_timeBegin.text!! as String)
            val calendar = Calendar.getInstance()
            calendar.time = time
            beginHour = calendar.get(Calendar.HOUR_OF_DAY)
            beginMinute = calendar.get(Calendar.MINUTE)
            true
        }catch (e:Exception){
            Log.e(TAG, "Erro de conversão de datas: $e")
            false
        }

        if (!isFormated) return false
        if(beginHour > hour) return false
        if ((beginHour == hour) && (beginMinute > minute)) return false

        return timeBeginIsValid(hour, minute)
    }

    fun saveClass(view: View) {
        if ( SystemClock.elapsedRealtime() - lastClickTime < 1000) return
        lastClickTime = SystemClock.elapsedRealtime()

        Thread(Runnable {
            if (newAcademicClass) createClass()
            else if (classHasBeenUpdated()) updateClass()
            else runOnUiThread {
                Toast.makeText(this, "A aula já está salva.", Toast.LENGTH_SHORT).show()
            }
        }).start()
    }

    private fun createClass(){
        val createdClass = loadClasInfos() ?: return@createClass
        if (!Connection().isOnline(this)){
            runOnUiThread { dialogError(getString(R.string.error_connect)) }
            return
        }
        try {
            runOnUiThread { loadingDialog.startLoadingDialog() }
            val id = academicClassDB.createClass(createdClass)
            newAcademicClass = false
            createdClass.id = id
            academicClass = createdClass
            runOnUiThread {
                Toast.makeText(this, "A aula foi criada com sucesso.", Toast.LENGTH_SHORT).show()
            }
        }catch (e:Exception){
            Log.e(TAG,"Erro de conexão: $e.")
            newAcademicClass = true
            runOnUiThread {
                Toast.makeText(this, "Erro ao criar a aula.", Toast.LENGTH_SHORT).show()
            }
        }finally {
            runOnUiThread { loadingDialog.dismissDialog() }
        }
    }

    private fun updateClass(){
        val updadedClass = loadClasInfos() ?: return@updateClass
        if (!Connection().isOnline(this)){
            runOnUiThread { dialogError(getString(R.string.error_connect)) }
            return
        }

        try {
            runOnUiThread { loadingDialog.startLoadingDialog() }
            academicClass!!.id.also { updadedClass.id = it }
            if (academicClassDB.updateClass(updadedClass)){
                runOnUiThread {
                    Toast.makeText(this,
                        "A aula foi atualizada.",
                        Toast.LENGTH_SHORT).show()
                }
                academicClass = updadedClass
            }else{
                runOnUiThread {
                    Toast.makeText(this,
                        "Erro ao atualizar a aula. Tente mais tarde.",
                        Toast.LENGTH_SHORT).show()
                }
            }
        }catch (e:Exception){
            Log.e(TAG,"Erro de conexão: $e.")
        }finally {
            runOnUiThread { loadingDialog.dismissDialog() }
        }
    }

    fun beginFrequency(view: View) {
        if ( SystemClock.elapsedRealtime() - lastClickTime < 1000) return
        lastClickTime = SystemClock.elapsedRealtime()

        if (checkPermissionsDenied()) {
            MaterialAlertDialogBuilder(this)
                .setTitle("Atenção")
                .setMessage("O aplicativo precisa de todas as permissoẽs para iniciar uma aula.")
                .setCancelable(false)
                .setPositiveButton("OK"
                ) { dialog, which -> dialog?.dismiss() }
                .show()
            val permission: Array<String> = getListPermissions()
            requestPermissions(permission, PERMISSION_CODE)
            return
        }

        Thread(Runnable {
            if (!validateFields()) return@Runnable
            syncClassData()

            runOnUiThread {
                if (academicClass == null){
                    Toast.makeText(this, "Erro ao criar a aula.", Toast.LENGTH_SHORT).show()
                    return@runOnUiThread
                }
                button_beginAttendance.isEnabled = false
                button_saveClassInfo.isEnabled = false
                button_status.isEnabled = true
            }
            intent = Intent(this, ManageFrequency::class.java)
            intent.putExtra(getString(R.string.academic_class), academicClass as Serializable)
            startActivity(intent)//bluetooth versao minima = 4.2, android 6
        }).start()
    }

    fun statusFrequency(view: View) {
        if ( SystemClock.elapsedRealtime() - lastClickTime < 1000) return
        lastClickTime = SystemClock.elapsedRealtime()

        if(academicClass!!.activeValidation){
            val date: String = textView_date.text.toString()
            val endTime:String =  textView_timeEnd.text.toString()
            val rightNow = Calendar.getInstance()

            val blocked = try {
                val format = SimpleDateFormat("dd/MM/yyyy HH:mm")
                val endDate = format.parse("$date $endTime")

                if (!Connection().isOnline(this)){
                    dialogError(getString(R.string.error_connect))
                    return
                }
                if (endDate < rightNow.time){
                    dialogError("A aula já passou do horário.")
                    button_status.isEnabled = false
                    button_timeEnd.isEnabled = false
                    academicClassDB.blockClass(academicClass!!.id)
                    academicClass!!.blockedAttendance = true
                    true
                }else false
            }catch (e:Exception){
                Log.e(TAG, "Erro ao bloquear a aula: ${e}.")
                true
            }
            if (blocked) return
        }
        intent = Intent(this, ManageFrequency::class.java)
        intent.putExtra(getString(R.string.academic_class), academicClass as Serializable)
        startActivity(intent)
    }

    fun studentList(view: View) {
        intent = Intent(this, StudentList::class.java)
        intent.putExtra(getString(R.string.academic_class), academicClass as Serializable)
        startActivity(intent)
    }

    private fun syncClassData(){
        if (newAcademicClass) createClass()
        else if (classHasBeenUpdated()) updateClass()
      }

    private fun classHasBeenUpdated():Boolean{
        if (editText_class.text.toString()  != academicClass!!.titleClass) return true
        if (editText_description.text.toString() != academicClass!!.descriptionClass) return true
        if (radioButtonBLE.isChecked != academicClass!!.validationByBLE) return true
        if (radioButtonQrCode.isChecked != academicClass!!.validationByQrCode) return true

        var beginDate = textView_date.text.toString()  + " " +  textView_timeBegin.text.toString()
        if(!beginDate.isNullOrBlank()){
            beginDate = convertDatePattern(beginDate, displayTimePattern, databaseTimePattern)
        }

        var endDate = textView_date.text.toString()  + " " +  textView_timeEnd.text.toString()
        if (!endDate.isNullOrBlank()){
            endDate = convertDatePattern(endDate, displayTimePattern, databaseTimePattern)
        }

        if (compareDate(academicClass!!.beginDate, beginDate, databaseTimePattern) != 0) return true
        if (compareDate(academicClass!!.endDate, endDate, databaseTimePattern) != 0) return true

        return false
    }

    private fun validateFields():Boolean{
        val titleClass:String = editText_class.text.toString()
        val descriptionClass:String = editText_description.text.toString()
        val date: String = textView_date.text.toString()
        val beginTime:String = textView_timeBegin.text.toString()
        val endTime:String =  textView_timeEnd.text.toString()
        if (titleClass.isBlank() ){
            editText_class.error = "Campo obrigatório."
            editText_class.requestFocus()
            return false
        }
        if (descriptionClass.isBlank()){
            editText_description.error = "Campo obrigatório."
            editText_description.requestFocus()
            return false
        }
        if (date.isBlank()){
            textView_date.error = "Campo obrigatório."
            textView_date.requestFocus()
            return false
        }
        if (beginTime.isBlank()){
            textView_timeBegin.error = "Campo obrigatório."
            textView_timeBegin.requestFocus()
            return false
        }
        if (endTime.isBlank()){
            textView_timeEnd.error = "Campo obrigatório."
            textView_timeEnd.requestFocus()
            return false
        }

        val rightNow = Calendar.getInstance()
        val format = SimpleDateFormat("dd/MM/yyyy HH:mm")
        val endDate = format.parse("$date $endTime")
        val beginDate = format.parse("$date $beginTime")

        if (endDate!! < rightNow.time){
            dialogError("Horário da aula já passou. Insira um horário válido.")
            textView_date.text = ""
            textView_timeBegin.text = ""
            textView_timeEnd.text = ""
            return false
        }

        val oneHourBefore = Calendar.getInstance()
        oneHourBefore.add(Calendar.HOUR_OF_DAY, -1)
        if(beginDate!! < oneHourBefore.time){
            dialogError("A aula pode ser iniciada no máximo com uma hora de antecedência.")
            return false
        }

        if (!radioButtonBLE.isChecked && !radioButtonQrCode.isChecked){
            radioButtonBLE.error = "Campo obrigatório."
            return false
        }

        return true
    }

    //sem zona de tempo na data de entrada
    private fun convertDatePattern(date: String, patternIn: String, patternOut: String): String {
        val timeZone = TimeZone.getDefault().getDisplayName(false, TimeZone.SHORT)
        //val utc = timeZone.drop(3)
        val formatIn = SimpleDateFormat(patternIn)
        val formatOut = SimpleDateFormat(patternOut)

        val temp = formatIn.parse(date + timeZone)

        return formatOut.format(temp!!)
    }

    // 0 -> igual, 1-> data1 > data2, -1-> data1 < data2, -2 -> error
    private fun compareDate(date1:String?, date2:String?, pattern: String):Int{
        if (date1.isNullOrBlank() && date2.isNullOrBlank()) return 0
        if (date1.isNullOrBlank() && !date2.isNullOrBlank()) return -1
        if (!date1.isNullOrBlank() && date2.isNullOrBlank()) return 1

        val result = try {
            val dateFormat = SimpleDateFormat(pattern)
            val begin = dateFormat.parse(date1!!)
            val end =  dateFormat.parse(date2!!)
            when {
                begin!!.time < end!!.time -> -1
                begin.time > end.time -> 1
                else -> 0
            }
        }catch (e:Exception){
            Log.e(TAG, "Erro ao fazer o parse de datas: $e")
            -2
        }
        return result
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

    private fun loadClasInfos(): AcademicClass? {
        val titleClass: String = editText_class.text.toString()
        val descriptionClass: String = editText_description.text.toString()

        if (editText_class.text.isBlank()) {
            editText_class.error = "Campo obrigatório."
            return null
        }
        if (editText_description.text.isBlank()) {
            editText_description.error = "Campo obrigatório."
            return null
        }

        val beginDate: String? = try {
            val date = textView_date.text.toString() + " " + textView_timeBegin.text.toString()
            convertDatePattern(date, displayTimePattern, databaseTimePattern)
        } catch (e: Exception) {
            Log.e(TAG, e.toString())
            null
        }

        val endDate: String? = try {
            val date = textView_date.text.toString() + " " + textView_timeEnd.text.toString()
            convertDatePattern(date, displayTimePattern, databaseTimePattern)
        } catch (e: Exception) {
            Log.e(TAG, e.toString())
            null
        }

        try {
            location = locationManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER)
            longitude = location?.longitude ?: 0.0
            latitude = location?.latitude ?: 0.0
            Log.i(TAG, "Longitude: ${longitude}, latitude:${latitude}")
        } catch(ex: SecurityException) {
            latitude = 0.0
            longitude = 0.0
            Log.d(TAG, "Erro a localização não está disponível")
        }

        val id = 0
        return AcademicClass(
            id, group.id, titleClass, descriptionClass, beginDate, endDate,
            longitude, latitude, false,
            qrcode, ble, false, null)
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
                    if ( SystemClock.elapsedRealtime() - lastClickTime < 1000)
                        return@setOnMenuItemClickListener true
                    lastClickTime = SystemClock.elapsedRealtime()

                    refreshInfos()
                   true
                }
                else -> false
            }
        }
    }

    private fun refreshInfos(){
        if (newAcademicClass) return
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
        }else if (academicClass != null){
            Thread(Runnable {
                if(academicClass!!.id > 0) {
                    try{
                        academicClass = academicClassDB.read(academicClass!!.id)
                        runOnUiThread {
                            setObjects()
                            flowControl()
                            Toast.makeText(this, "Informações atualizadas.", Toast.LENGTH_SHORT).show()
                        }
                    }catch (e:Exception){
                        Log.v(TAG, "Erro na atualização da tela: $e")
                    }
                }
            }).start()
        }
    }

    private fun checkPermissionsDenied():Boolean{
        if (checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_DENIED) return true
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_DENIED) return true
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            if (checkSelfPermission(Manifest.permission.BLUETOOTH_SCAN) == PackageManager.PERMISSION_DENIED) return true
            if (checkSelfPermission(Manifest.permission.BLUETOOTH_ADVERTISE) == PackageManager.PERMISSION_DENIED) return true
            if (checkSelfPermission(Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_DENIED) return true
        }else{
            if (checkSelfPermission(Manifest.permission.BLUETOOTH) == PackageManager.PERMISSION_DENIED) return true
            if (checkSelfPermission(Manifest.permission.BLUETOOTH_ADMIN) == PackageManager.PERMISSION_DENIED) return true
        }
        return false
    }

    private fun getListPermissions(): Array<String> {
        val permissions = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            arrayOf(
                Manifest.permission.ACCESS_COARSE_LOCATION,
                Manifest.permission.ACCESS_FINE_LOCATION,
                Manifest.permission.BLUETOOTH_SCAN,
                Manifest.permission.BLUETOOTH_ADVERTISE,
                Manifest.permission.BLUETOOTH_CONNECT
            )
        } else {
            arrayOf(
                Manifest.permission.BLUETOOTH,
                Manifest.permission.ACCESS_COARSE_LOCATION,
                Manifest.permission.ACCESS_FINE_LOCATION,
                Manifest.permission.BLUETOOTH_ADMIN
            )
        }
        return permissions
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
}