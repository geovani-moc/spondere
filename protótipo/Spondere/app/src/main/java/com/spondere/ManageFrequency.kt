package com.spondere

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.bluetooth.le.AdvertiseCallback
import android.bluetooth.le.AdvertiseData
import android.bluetooth.le.AdvertiseSettings
import android.bluetooth.le.BluetoothLeAdvertiser
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.*
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.Toolbar
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.spondere.adapter.StudentPhotoListAdapter
import com.spondere.entity.AcademicClass
import com.spondere.entity.StudentPhoto
import com.spondere.entity.User
import com.spondere.util.Connection
import com.spondere.util.LoadingDialog
import com.spondere.util.Preferences
import java.util.*
import kotlin.collections.ArrayList
import com.spondere.network.Frequency as FrequencyDB
import com.spondere.network.AcademicClass as AcademicClassDB

class ManageFrequency : AppCompatActivity() {
    private val TAG = "manage_frequency"
    private val PERMISSION_CODE = 1006
    private var academicClass: AcademicClass? = null
    private lateinit var button_pauseFrequency:Button
    private lateinit var button_endFrequency:Button
    private lateinit var textView_attendanceRate:TextView
    private lateinit var preferences: Preferences
    private lateinit var userPreferences: Preferences
    private lateinit var token: String
    private lateinit var username:String
    private lateinit var user: User
    private lateinit var academicClassDB: AcademicClassDB
    private lateinit var frequencyDB: FrequencyDB
    private lateinit var studentsPhotos:ArrayList<StudentPhoto>
    private lateinit var recyclerView_studentPhoto: RecyclerView
    private lateinit var adapter: StudentPhotoListAdapter
    private val mapper = jacksonObjectMapper()
    private val databaseTimePattern = "yyyy-MM-dd'T'HH:mm:ssZ"
    private val displayTimePattern = "dd/MM/yyyy HH:mmZ"
    private var numberStudents:Int = 0
    private var numberPresents:Int = 0
    private lateinit var toolbar: Toolbar
    private val bluetoothAdapter: BluetoothAdapter? by lazy(LazyThreadSafetyMode.NONE) {
        val bluetoothManager = getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        bluetoothManager.adapter
    }
    private val registerForResult =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == RESULT_OK) Log.v(TAG, "Bluetooth ligado")
            if (result.resultCode == RESULT_CANCELED) Log.v(TAG, "Bluetooth não foi ligado.")
        }

    private var advertiser:BluetoothLeAdvertiser? = null
    private lateinit var advertisingCallback: AdvertiseCallback
    private lateinit var loadingDialog: LoadingDialog
    private var lastClickTime: Long = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_manage_frequency)

        loadPermissions()
        readPreferences()
        loadObjects()
        setObjects()
        loadAppBar()
        loadAdapter()
        beginFrequency()
    }

    override fun onRestart() {
        super.onRestart()
        refresh()
    }

    override fun onDestroy() {
        super.onDestroy()
        try {
            if ((Build.VERSION.SDK_INT >= Build.VERSION_CODES.S)
                && (checkSelfPermission( Manifest.permission.BLUETOOTH_ADVERTISE) != PackageManager.PERMISSION_GRANTED)){
                Log.v(TAG, "Sem permissao de uso de advertaise.")
                return
            }
            if ((advertiser == null) || (!this::advertisingCallback.isInitialized)){
                Log.v(TAG, "Advertise estava sem funcionar.")
                return
            }
            advertiser?.stopAdvertising(advertisingCallback)
        }catch (e:Exception){
            Log.e(TAG, "Erro ao finalizar anuncio: $e")
        }
    }

    private fun loadObjects(){
        button_pauseFrequency = findViewById(R.id.button_pauseFrequency)
        textView_attendanceRate = findViewById(R.id.textView_attendanceRate)
        loadingDialog = LoadingDialog(this)
    }

    private fun readPreferences(){
        academicClass = intent.extras!!.get(getString(R.string.academic_class)) as AcademicClass

        preferences = Preferences(getString(R.string.settings_login), this)
        userPreferences = Preferences(getString(R.string.user_preference), this)
        token = preferences.loadData(getString(R.string.token)).toString()
        username = preferences.loadData(getString(R.string.user_name)).toString()
        academicClassDB = AcademicClassDB(this, token)
        frequencyDB = FrequencyDB(this, token)

        val userJson = userPreferences.loadData(getString(R.string.user_preference))
        if (userJson.isNullOrEmpty()){
            Toast.makeText(applicationContext,
                "Erro ao carregar as informações do usuário, faça a autenticação novamente.",
                Toast.LENGTH_LONG).show()
        }

        user = mapper.readValue(userJson, User::class.java)
    }

    private fun setObjects(){
        advertiser = bluetoothAdapter?.bluetoothLeAdvertiser
        if(advertiser == null){
            Toast.makeText(this,
                "Seu aparelho não é compatível, não é possível anunciar os códigos de validação.",
                Toast.LENGTH_LONG).show()
        }
    }

    private fun beginFrequency(){
        if (academicClass == null) return
        Thread(Runnable {
            try {
                val (numberStudents, numberPresents) = frequencyDB.attendanceRate(academicClass!!.id)
                runOnUiThread {
                    textView_attendanceRate.text = "Discentes presentes ($numberPresents | $numberStudents)"
                }
            }catch (e:Exception){
                Log.e(TAG, "Erro ao tentar carregar a taxa de alunos presents: $e")
                runOnUiThread {
                    textView_attendanceRate.text = "Discentes presentes"
                }
            }
        }).start()
        if (!academicClass!!.blockedAttendance && !academicClass!!.validationCode.isNullOrBlank()){
            Thread(Runnable {
                academicClass!!.validationCode?.let { advertise(it) }
            }).start()
            return
        }
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            finish()
        }
        Thread(Runnable {
            runOnUiThread { loadingDialog.startLoadingDialog() }
            var code = ""
            try {
                code = frequencyDB.beginFrequency(academicClass!!.id)
            }catch (e:Exception){
                Log.e(TAG, "Erro: nenhum código retornado do servidor. $e")
            }
            if (code == ""){
                Log.v(TAG, "O código de validação está vazio.")
                runOnUiThread {
                    Toast.makeText(applicationContext,
                        "Não foi obtido o código de validação, tente mais tarde.",
                        Toast.LENGTH_LONG).show()
                }
                finish()
            }else advertise(code)
            runOnUiThread { loadingDialog.dismissDialog()}
        }).start()
    }

    fun endFrequency(view: View) {
        if ((Build.VERSION.SDK_INT >= Build.VERSION_CODES.S)
            && (checkSelfPermission( Manifest.permission.BLUETOOTH_ADVERTISE) != PackageManager.PERMISSION_GRANTED)){
            Log.v(TAG, "Sem permissao de uso de advertaise.")
            finish()
        }
        if ((advertiser == null) || (!this::advertisingCallback.isInitialized)){
            Log.v(TAG, "Advertise não foi iniciado.")
            finish()
        }
        advertiser?.stopAdvertising(advertisingCallback)

        MaterialAlertDialogBuilder(this)
            .setTitle("Atenção")
            .setMessage("Ao finalizar uma aula, ela será bloqueada e os discentes não poderão fazer " +
                    "mais comprovação biométrica nesta aula.")
            .setPositiveButton("Finalizar"
            ) { dialog, which -> blockFrequency() }
            .setNegativeButton("Cancelar"){
                dialog, which -> dialog.dismiss()
            }
            .show()
    }

    fun blockFrequency(){
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return
        }
        if (academicClass == null) return
        if (academicClass!!.id <= 0) return

        try {
            academicClassDB.blockClass(academicClass!!.id)
        }catch (e:Exception){
            Log.e(TAG, "Erro ao bloquear aula: $e")
        }
        finish()
    }

    fun pauseFrequency(view: View) {
        if ((Build.VERSION.SDK_INT >= Build.VERSION_CODES.S)
            && (checkSelfPermission( Manifest.permission.BLUETOOTH_ADVERTISE) != PackageManager.PERMISSION_GRANTED)){
            Log.v(TAG, "Sem permissao de uso de advertaise.")
            finish()
        }
        if ((advertiser == null) || (!this::advertisingCallback.isInitialized)){
            Log.v(TAG, "Advertise estava sem funcionar.")
            finish()
        }
        advertiser?.stopAdvertising(advertisingCallback)

        finish()
    }

    private fun advertise(code:String) {
        val settings = AdvertiseSettings.Builder()
            .setAdvertiseMode(AdvertiseSettings.ADVERTISE_MODE_LOW_LATENCY)
            .setTxPowerLevel(AdvertiseSettings.ADVERTISE_TX_POWER_HIGH)
            .setTimeout(0)
            .setConnectable(false)
            .build()
        val pUuid = ParcelUuid(UUID.fromString(getString(R.string.uuid)))

        val data = AdvertiseData.Builder()
            .setIncludeTxPowerLevel(false)
            .setIncludeDeviceName(false)
            .addServiceUuid(pUuid)
            .addServiceData(pUuid, code.toByteArray(Charsets.UTF_8))
            .build()

        advertisingCallback = object : AdvertiseCallback() {
            override fun onStartSuccess(settingsInEffect: AdvertiseSettings) {
                super.onStartSuccess(settingsInEffect)
                Log.v(TAG, "Advertising iniciado com sucesso.data: ${code.toByteArray(Charsets.UTF_8)}")
            }

            override fun onStartFailure(errorCode: Int) {
                super.onStartFailure(errorCode)
                Log.e(TAG, "Advertising onStartFailure: $errorCode")
            }
        }
        if (advertiser == null){
            runOnUiThread {
                Toast.makeText(this,
                    "O Bluetooth está desligado ou seu aparelho não tem suporte.",
                    Toast.LENGTH_LONG).show()
            }
            finish()
            return
        }
        if ((Build.VERSION.SDK_INT >= Build.VERSION_CODES.S)
            && (checkSelfPermission( Manifest.permission.BLUETOOTH_ADVERTISE) != PackageManager.PERMISSION_GRANTED) ) {
            Log.v(TAG, "Sem permissao de uso de advertaise.")
            return
        }
        advertiser?.startAdvertising(settings, data, advertisingCallback)
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
                    refresh()
                    true
                }
                else -> false
            }
        }
    }

    private fun refresh(){
        Thread(Runnable {
            runOnUiThread { loadingDialog.startLoadingDialog() }
            var updated  = false
            try {
                updated = getAttendanceRate()
                runOnUiThread {
                    textView_attendanceRate.text = "Discentes presentes ($numberPresents | $numberStudents)"
                }
                updated = true
            }catch (e:Exception){
                Log.e(TAG, "Erro ao tentar carregar a taxa de alunos presents: $e")
                runOnUiThread { textView_attendanceRate.text = "Discentes presentes" }
            }

            try {
                if (!this::adapter.isInitialized){
                    loadAdapter()
                    updated = true
                }else{
                    getStudentsPhotos()
                    adapter.updateItens(studentsPhotos)
                    runOnUiThread { adapter.notifyDataSetChanged() }
                    updated = true
                }
            }catch (e: Exception){
                Log.e(TAG, "Erro ao atualizar adapter: $e")
            }
            runOnUiThread{
                if(updated){
                    Toast.makeText(this, "Informações atualizadas.", Toast.LENGTH_SHORT).show()
                    Log.v(TAG, "Lista de presentes com foto atualizado.")
                }
                loadingDialog.dismissDialog()
            }
        }).start()
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
        } else {
            if (!bluetoothAdapter?.isEnabled!!) {
                val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
                registerForResult.launch(enableBtIntent)
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

    private fun loadAdapter(){
        Thread(Runnable {
            getStudentsPhotos()
            if (!this::studentsPhotos.isInitialized){
                Log.v(TAG, "Não foi possivel carregar as disciplinas.")
                return@Runnable
            }
            recyclerView_studentPhoto = findViewById(R.id.recyclerView_studentPhotoList)
            runOnUiThread {
                recyclerView_studentPhoto.layoutManager = GridLayoutManager(this, 3)
                adapter =  StudentPhotoListAdapter(this, studentsPhotos)
                recyclerView_studentPhoto.adapter = adapter
                adapter.setOnItemClickListener(object: StudentPhotoListAdapter.onItemClickListener{
                    override fun onItemClick(position: Int) {
                        Log.i(TAG, "clique do intent")
                    }
                })
            }
        }).start()
    }

    private fun getStudentsPhotos():Boolean{
        if (academicClass == null) return false
        if (academicClass!!.id <= 0) return false
        if (!Connection().isOnline(this)){
            runOnUiThread { dialogError(getString(R.string.error_connect)) }
            return false
        }
        var updated = false
        try {
            studentsPhotos = frequencyDB.studentWithPhotoPresent(academicClass!!.id)
            updated = true
        }catch (e: Exception) {
            Log.e(TAG, "e")
        }
        return updated
    }

    private fun getAttendanceRate():Boolean{
        if (!Connection().isOnline(this)){
            runOnUiThread { dialogError(getString(R.string.error_connect)) }
            return false
        }
        var updated = false
        try {
            val result = frequencyDB.attendanceRate(academicClass!!.id)
            numberStudents = result.first
            numberPresents = result.second
            updated = true
        }catch (e: Exception) {
            Log.e(TAG, "e")
        }
        return updated
    }
}