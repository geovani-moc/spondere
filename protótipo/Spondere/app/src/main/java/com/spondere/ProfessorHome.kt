package com.spondere

import android.annotation.SuppressLint
import android.content.Intent
import android.os.Bundle
import android.os.SystemClock
import android.util.Log
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
import kotlin.system.exitProcess
import com.spondere.network.Discipline as DisciplineBD

class ProfessorHome : AppCompatActivity() {
    private lateinit var recyclerView_discipline: RecyclerView
    private lateinit var preferences: Preferences
    private lateinit var userPreferences:Preferences
    private lateinit var token: String
    private lateinit var username:String
    private lateinit var disciplines:ArrayList<Discipline>
    private lateinit var groups:ArrayList<Group>
    private lateinit var user:User
    private val mapper = jacksonObjectMapper()
    private val TAG = "professor_home"
    private lateinit var toolbar:Toolbar
    private val app = App()
    private lateinit var adapter: DisciplineAdapter
    private lateinit var loadingDialog: LoadingDialog
    private var lastClickTime: Long = 0

        override fun onCreate(savedInstanceState: Bundle?) {
            super.onCreate(savedInstanceState)
            setContentView(R.layout.activity_professor_home)

            loadAppBar()
            readPreferences()
            loadObjects()
            loadAdapter()
    }

     override fun onBackPressed() {
         super.onBackPressed()
         moveTaskToBack(true)
         finish()
         exitProcess(0)
     }

    private fun loadObjects(){
        loadingDialog = LoadingDialog(this)
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

        val userJson = userPreferences.loadData(getString(R.string.user_preference))
        if (userJson.isNullOrEmpty()){
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

    private fun loadAdapter(){
        Thread(Runnable {
            if (!this::disciplines.isInitialized || !this::groups.isInitialized){ getDisciplines() }
            else if (disciplines.isEmpty() || groups.isEmpty()){ getDisciplines() }

            recyclerView_discipline = findViewById(R.id.recyclerView_discipline)
            runOnUiThread {
                recyclerView_discipline.layoutManager = LinearLayoutManager(this)
                adapter =  DisciplineAdapter(this, disciplines, groups)
                recyclerView_discipline.adapter = adapter
                adapter.setOnItemClickListener(object:DisciplineAdapter.onItemClickListener{
                    override fun onItemClick(position: Int) {
                        if (!Connection().isOnline(applicationContext)){
                            dialogError(getString(R.string.error_connect))
                            return
                        }
                        val intent = Intent(this@ProfessorHome, DisciplineDetail::class.java)
                        intent.putExtra(getString(R.string.discipline), disciplines[position] as Serializable)
                        intent.putExtra(getString(R.string.group), groups[position] as Serializable)
                        startActivity(intent)
                    }
                })
            }
        }).start()
    }

    @SuppressLint("NotifyDataSetChanged")
    private fun loadAppBar(){
        toolbar = findViewById(R.id.topAppBar)
        toolbar.setOnMenuItemClickListener {menuItem ->
            when (menuItem.itemId) {
                R.id.edit -> {
                    if (SystemClock.elapsedRealtime() - lastClickTime < 1000){
                        Log.i(TAG, "Duplo clique impedido.")
                    }else{
                        lastClickTime = SystemClock.elapsedRealtime()
                        intent = Intent(this, Account::class.java)
                        startActivity(intent)
                    }
                    true
                }
                R.id.refresh -> {
                    if ( SystemClock.elapsedRealtime() - lastClickTime < 1000){
                        Log.i(TAG, "Duplo clique impedido.")
                    }else{
                        lastClickTime = SystemClock.elapsedRealtime()
                        refresh()
                    }
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

            }catch (e: Exception){
                Log.e(TAG, "Erro ao atualizar adapter: $e")
            }
            if (updated){
                Log.v(TAG, "Disciplinas atualizadas.")
                runOnUiThread {
                    Toast.makeText(this, "Informações atualizadas.", Toast.LENGTH_SHORT).show()
                }
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
                runOnUiThread{ dialogError(getString(R.string.error_connect))}
                return false
            }
            try {
                runOnUiThread{ loadingDialog.startLoadingDialog()}
                var (disciplineTemp, groupTemp ) = DisciplineBD(this, token).getDisciplinesByProfessor(username)
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
                runOnUiThread { loadingDialog.dismissDialog()}
            }
        }
        return result
    }

}

