package com.spondere

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.os.SystemClock
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.Toolbar
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.spondere.adapter.DisciplineAdapter
import com.spondere.entity.Discipline
import com.spondere.entity.Group
import com.spondere.entity.User
import com.spondere.util.App
import com.spondere.util.Connection
import com.spondere.util.LoadingDialog
import com.spondere.util.Preferences
import java.io.Serializable
import com.spondere.network.Frequency as FrequencyDB
import com.spondere.network.Discipline as DisciplineDB

class StudentHome : AppCompatActivity() {
    private val TAG = "student_home"
    private lateinit var recyclerView_discipline: RecyclerView
    private lateinit var preferences: Preferences
    private lateinit var userPreferences:Preferences
    private lateinit var token: String
    private lateinit var username:String
    private lateinit var disciplines: ArrayList<Discipline>
    private lateinit var groups: ArrayList<Group>
    private lateinit var user:User
    private val mapper = jacksonObjectMapper()
    private val BLE_METHOD = 1001
    private val QRCODE_METHOD = 1002
    private lateinit var frequencyDB:FrequencyDB
    private lateinit var disciplineDB:DisciplineDB
    private lateinit var toolbar: Toolbar
    private val app = App()
    private lateinit var adapter: DisciplineAdapter
    private lateinit var loadingDialog: LoadingDialog
    private var lastClickTime: Long = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_student_home)

        loadAppBar()
        readPreferences()
        loadObjects()
        loadAdapter()
    }

    private fun loadAdapter(){
        Thread(Runnable {
            if (!this::disciplines.isInitialized || !this::groups.isInitialized){ getDisciplines() }
            else if (disciplines.isEmpty() || groups.isEmpty()){ getDisciplines() }

            recyclerView_discipline = findViewById(R.id.recyclerView_discipline)
            runOnUiThread {
                recyclerView_discipline.layoutManager = LinearLayoutManager(this)
                adapter =  DisciplineAdapter(this, disciplines, groups)
                recyclerView_discipline.adapter = adapter
                adapter.setOnItemClickListener(object: DisciplineAdapter.onItemClickListener{
                    override fun onItemClick(position: Int) {
                        if (!Connection().isOnline(applicationContext)){
                            dialogError(getString(R.string.error_connect))
                            return
                        }
                        val intent = Intent(this@StudentHome, DisciplineClasses::class.java)
                        intent.putExtra(getString(R.string.discipline), disciplines[position] as Serializable)
                        intent.putExtra(getString(R.string.group), groups[position] as Serializable)
                        startActivity(intent)
                    }
                })
            }
        }).start()
    }

    private fun readPreferences(){
        preferences = Preferences(getString(R.string.settings_login), this)
        userPreferences = Preferences(getString(R.string.user_preference), this)
        token = preferences.loadData(getString(R.string.token)).toString()
        username = preferences.loadData(getString(R.string.user_name)).toString()

        val disciplinesJson = userPreferences.loadData(getString(R.string.disciplines))
        val groupsJson = userPreferences.loadData(getString(R.string.groups))

        if (!disciplinesJson.isNullOrBlank()) { disciplines = mapper.readValue(disciplinesJson) }
        if (!groupsJson.isNullOrBlank()){ groups = mapper.readValue(groupsJson) }

        frequencyDB = FrequencyDB(this, token)
        disciplineDB = DisciplineDB(this, token)

        val userJson = userPreferences.loadData(getString(R.string.user_preference))
        if (userJson.isNullOrBlank()){
            app.logout(this)
            Toast.makeText(this,
                "Dados de usuários estão vazios, faça login novamente.",
                Toast.LENGTH_LONG).show()
            intent = Intent(this, Login::class.java)
            startActivity(intent)
            finishAffinity()
        }
        user = mapper.readValue(userJson, User::class.java)
    }

    private fun loadObjects(){
        loadingDialog = LoadingDialog(this)
    }

    fun qrcodeMethod(view: View) {
        Log.v(TAG, "Metodo não implementado.")
    }

    fun bleMethod(view: View) {
        intent = Intent(this, FrequencyValidation::class.java)
        intent.putExtra(getString(R.string.method), getString(R.string.bluetooth))
        startActivityForResult(intent, BLE_METHOD)
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode != BLE_METHOD) return
        if (resultCode != RESULT_OK) return

        val codes = data!!.extras?.getStringArrayList(getString(R.string.validatioCode))
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return
        }
        codes?.let { initBiometry(it) }
    }

    private fun initBiometry(codes:ArrayList<String>){
        if (codes.size < 1) {
            Toast.makeText(this,
                "Nenhum código foi encontrado, tente mais tarde.",
                Toast.LENGTH_LONG).show()
            return
        }
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return
        }
        Thread(Runnable {
            runOnUiThread{loadingDialog.startLoadingDialog()}
            var classID = 0
            for (code in codes){
                if (code.length == 10){
                    try {
                        classID = frequencyDB.checkValidationCode(code)
                        if (classID > 0) break
                    }catch (e:Exception){
                        Log.v(TAG, "Erro ao verificar o código $code: $e")
                    }
                }
            }
            if (classID < 1) {
                runOnUiThread {
                    Toast.makeText(this,
                        "Nenhum código válido encontrado.",
                        Toast.LENGTH_SHORT).show()
                }
                return@Runnable
            }

            intent = Intent(this, Biometry::class.java)
            intent.putExtra("classID", classID)
            startActivity(intent)
            runOnUiThread { loadingDialog.dismissDialog() }
        }).start()
    }

    @SuppressLint("NotifyDataSetChanged")
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
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return
        }
        Thread(Runnable {
            var updated = false
            try {
                if (!this::adapter.isInitialized){
                    loadAdapter()
                }else{
                    updated = getDisciplines()
                    adapter.updateItens(disciplines, groups)
                    runOnUiThread { adapter.notifyDataSetChanged() }
                }

            }catch (e: Exception){ Log.e(TAG, "Erro ao atualizar adapter: $e")}

            if (updated){
                runOnUiThread{
                    Toast.makeText(this, "Informações atualizadas.", Toast.LENGTH_SHORT).show()
                }
                Log.v(TAG, "Disciplinas atualizadas.")
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

    private fun getDisciplines():Boolean{
        var result = false
        if (token.isNotBlank() and username.isNotBlank()) {
            if (!Connection().isOnline(this)){
                runOnUiThread { dialogError(getString(R.string.error_connect))}
                return false
            }
            try {
                runOnUiThread { loadingDialog.startLoadingDialog() }
                val (disciplineTemp, groupTemp) = disciplineDB.getDisciplinesByStudent(username)
                disciplines = disciplineTemp
                groups = groupTemp
                val disciplinesJson = mapper.writeValueAsString(disciplines)
                val groupsJson = mapper.writeValueAsString(groups)
                userPreferences.saveData(getString(R.string.disciplines), disciplinesJson)
                userPreferences.saveData(getString(R.string.groups), groupsJson)
                result = true
            }catch (e: Exception) {
                Log.e(TAG, "e")
            }finally {
                runOnUiThread{ loadingDialog.dismissDialog() }
            }
        }
        return result
    }

}
