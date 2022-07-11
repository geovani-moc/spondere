package com.spondere

import android.Manifest
import android.annotation.SuppressLint
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.bluetooth.le.*
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.*
import android.text.TextUtils
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.Toolbar
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.spondere.entity.User
import com.spondere.util.Preferences
import java.nio.charset.Charset

class FrequencyValidation : AppCompatActivity() {
    private val TAG = "validacao"
    private var codes:ArrayList<String> = ArrayList()
    private lateinit var user:User
    private lateinit var preferences: Preferences
    private lateinit var userPreferences:Preferences
    private val mapper = jacksonObjectMapper()
    private lateinit var toolbar: Toolbar
    private val PERMISSION_CODE = 1005
    private var lastClickTime: Long = 0
    private val handler: Handler = Handler(Looper.getMainLooper())
    private val bluetoothAdapter: BluetoothAdapter? by lazy(LazyThreadSafetyMode.NONE) {
        val bluetoothManager = getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        bluetoothManager.adapter
    }
    private val registerForResult =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == RESULT_OK) Log.v(TAG, "Bluetooth ligado")
            if (result.resultCode == RESULT_CANCELED) Log.v(TAG, "Bluetooth não foi ligado.")
        }
    private var bluetoothLeScanner: BluetoothLeScanner? = null
    private lateinit var scanCallback: ScanCallback

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_frequency_validation)

        loadPermissions()
        readPreferences()
        setObjects()
        loadAppBar()
        discover()
    }

    override fun onDestroy() {
        super.onDestroy()
        try{
            if ((Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) &&
                (checkSelfPermission( Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED)) {
                Log.v(TAG, "Sem permisão para scannear via Bluetooh")
                return
            }
            bluetoothLeScanner!!.stopScan(scanCallback)
        }catch (e:Exception){
            Log.e(TAG, "Erro ao finalizar escaneamento do BLE: $e")
        }
    }

   /* override fun onResume() {
        super.onResume()
        discover()
    }*/


    private fun readPreferences(){
        preferences = Preferences(getString(R.string.settings_login), this)
        userPreferences = Preferences(getString(R.string.user_preference), this)

        val userJson = userPreferences.loadData(getString(R.string.user_preference))
        if (userJson.isNullOrEmpty()){
            Toast.makeText(applicationContext,
                "Erro ao carregar informações de usuário, faça a autenticação novamente.",
                Toast.LENGTH_LONG).show()
        }
        user = mapper.readValue(userJson, User::class.java)
    }

    private fun setObjects(){
        bluetoothLeScanner = bluetoothAdapter?.bluetoothLeScanner
    }

    fun cancel(view: View) {
        try{
            if ((Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) &&
                (checkSelfPermission( Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED)) {
                Log.v(TAG, "Sem permisão para scannear via Bluetooh")
                finish()
            }
            bluetoothLeScanner!!.stopScan(scanCallback)
        }catch (e:Exception){
            Log.e(TAG, "Erro ao finalizar escaneamento do BLE: $e")
        }
        finish()
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
                else -> false
            }
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
        } else {
            if (!bluetoothAdapter?.isEnabled!!) {
                val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
                registerForResult.launch(enableBtIntent)
                return
            }
        }

    }

    private fun discover() {
        //val filters: MutableList<ScanFilter> = java.util.ArrayList()
        val filters:MutableList<ScanFilter> = ArrayList()
        val filter = ScanFilter.Builder()
            .setServiceUuid(ParcelUuid.fromString(getString(R.string.uuid)))
            .build()
        filters.add(filter)
        val settings = ScanSettings.Builder()
            .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
            .build()

        scanCallback = object : ScanCallback() {
            @SuppressLint("MissingPermission", "SetTextI18n")
            override fun onScanResult(callbackType: Int, result: ScanResult?) {
                super.onScanResult(callbackType, result)

                if (result?.device == null || !TextUtils.isEmpty(result.device.name)) return
                val data = String(
                    result.scanRecord?.getServiceData(
                        result.scanRecord!!.serviceUuids[0])!!, Charset.forName("UTF-8"))
                codes.add(data)
            }

            override fun onBatchScanResults(results: List<ScanResult?>?) {
                super.onBatchScanResults(results)
            }

            override fun onScanFailed(errorCode: Int) {
                super.onScanFailed(errorCode)
                Log.e(TAG, "onScanFailed: $errorCode")
            }
        }

        if ((Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) &&
            (checkSelfPermission( Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED)) {
            Log.v(TAG, "Sem permisão para scannear via Bluetooh")
            return
        }

        if(bluetoothLeScanner == null){
            Toast.makeText(this,
                "O bluetooth está desativado ou seu aparelho não dá suporte a busca.",
                Toast.LENGTH_SHORT).show()
            finish()
            return
        }
        bluetoothLeScanner!!.startScan(filters, settings, scanCallback)

        handler.postDelayed(Runnable {
            if ((Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) &&
                (checkSelfPermission( Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED)) {
                Log.v(TAG, "Sem permisão para scannear via Bluetooh")
                return@Runnable
            }
            bluetoothLeScanner!!.stopScan(scanCallback)
            Log.v(TAG, "Escaneamento finalizado")
            val intent = Intent()
            val codesDistinct:ArrayList<String> = ArrayList(codes.distinct())
            intent.putStringArrayListExtra(getString(R.string.validatioCode), codesDistinct)
            setResult(RESULT_OK, intent)
            finish()
        }, 5000)
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        when (requestCode) {
            PERMISSION_CODE -> {
                if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED)
                    Log.v(TAG, "Permissoes do aplicavo liberada.")
                else
                    Log.v(TAG, "Permissoes não liberadas liberadas.")
            }
        }
    }
}