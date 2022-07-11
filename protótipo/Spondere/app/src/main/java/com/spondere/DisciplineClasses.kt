package com.spondere

import android.annotation.SuppressLint
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.SystemClock
import android.util.Log
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.widget.Toolbar
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.spondere.adapter.AcademicClassAdapter
import com.spondere.entity.Discipline
import com.spondere.entity.Group
import com.spondere.util.Connection
import com.spondere.util.Preferences
import java.io.Serializable
import com.spondere.entity.AcademicClass
import com.spondere.util.LoadingDialog
import com.spondere.network.AcademicClass as AcademicClassDB

class DisciplineClasses : AppCompatActivity() {
    private lateinit var recyclerView_academicClass: RecyclerView
    private lateinit var discipline: Discipline
    private lateinit var group: Group
    private lateinit var textView_diciplineName: TextView
    private lateinit var textView_diciplineDescription: TextView
    private lateinit var textView_groupCode: TextView
    private lateinit var token:String
    private lateinit var preferences: Preferences
    private lateinit var toolbar: Toolbar
    private lateinit var academicClassDB:AcademicClassDB
    private lateinit var academicClasses:ArrayList<AcademicClass>
    private lateinit var adapter:AcademicClassAdapter
    private val TAG = "discipline_classes"
    private lateinit var loadingDialog: LoadingDialog
    private var lastClickTime: Long = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_discipline_classes)

        readPreferences()
        loadObjects()
        setObjects()
        loadAdapter()
        loadAppBar()
    }

    private fun loadObjects(){
        textView_diciplineName = findViewById(R.id.textView_disciplineName)
        textView_diciplineDescription = findViewById(R.id.textView_disciplineDescription)
        textView_groupCode = findViewById(R.id.textView_groupCode)
        loadingDialog = LoadingDialog(this)
    }

    @SuppressLint("SetTextI18n")
    private fun setObjects(){
        textView_diciplineName.text = discipline.name
        textView_diciplineDescription.text = discipline.description
        textView_groupCode.text = "Código da turma: " + group.code
    }

    private fun readPreferences(){
        preferences = Preferences(getString(R.string.settings_login), this)
        token = preferences.loadData(getString(R.string.token)).toString()
        discipline = intent.extras!!.get(getString(R.string.discipline)) as Discipline
        group = intent.extras!!.get(getString(R.string.group)) as Group
        academicClassDB = AcademicClassDB(this, token)

    }

    private fun loadAdapter(){
        Thread(Runnable {
            getAcademicClasses()
            adapter = AcademicClassAdapter(this, academicClasses)
            recyclerView_academicClass = findViewById(R.id.recyclerView_academicClass)

            runOnUiThread {
                recyclerView_academicClass.layoutManager = LinearLayoutManager(this)
                recyclerView_academicClass.adapter = adapter

                adapter.setOnItemClickListener(object: AcademicClassAdapter.onItemClickListener{
                    override fun onItemClick(position: Int) {
                        val intent = Intent(this@DisciplineClasses, Biometry::class.java)
                        intent.putExtra(getString(R.string.academic_class), academicClasses[position] as Serializable)
                        startActivity(intent)
                    }
                })
            }
        }).start()
    }

    private fun getAcademicClasses(){
        if (!Connection().isOnline(this)){
            runOnUiThread { dialogError(getString(R.string.error_connect)) }
            return
        }
        try{
            runOnUiThread { loadingDialog.startLoadingDialog() }
            academicClasses = academicClassDB.getClassByGroupID(group.id)
        }catch (e:Exception){
            Log.e(TAG, "Erro ao buscar aulas.")
        }finally {
            runOnUiThread { loadingDialog.dismissDialog() }
        }
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
        Thread(Runnable {
            var updated = try {
                if (!this::adapter.isInitialized){
                    loadAdapter()
                    true
                }else{
                    getAcademicClasses()
                    adapter.updateItens(academicClasses)
                    runOnUiThread { adapter.notifyDataSetChanged() }
                    true
                }
            }catch (e: Exception){
                Log.e(TAG, "Erro ao atualizar adapter: $e")
                false
            }
            if (updated){
                runOnUiThread {  Toast.makeText(this, "Informações atualizadas.", Toast.LENGTH_SHORT).show() }
                Log.v(TAG, "Aulas do discente atualizadas.")
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
}
