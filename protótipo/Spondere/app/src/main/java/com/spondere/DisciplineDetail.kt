package com.spondere

import android.annotation.SuppressLint
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.SystemClock
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.widget.Toolbar
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.spondere.adapter.AcademicClassAdapter
import com.spondere.entity.AcademicClass
import com.spondere.entity.Discipline
import com.spondere.entity.Group
import com.spondere.util.Connection
import com.spondere.util.LoadingDialog
import com.spondere.util.Preferences
import java.io.Serializable
import com.spondere.network.AcademicClass as AcademicClassDB


class DisciplineDetail : AppCompatActivity() {
    private lateinit var recyclerView_academicClass:RecyclerView
    private lateinit var discipline: Discipline
    private lateinit var group: Group
    private lateinit var textView_diciplineName: TextView
    private lateinit var textView_diciplineDescription: TextView
    private lateinit var textView_groupCode: TextView
    private lateinit var button_newClass:Button
    private lateinit var token:String
    private lateinit var preferences:Preferences
    private lateinit var toolbar: Toolbar
    private lateinit var academicClassDB:AcademicClassDB
    private lateinit var adapter: AcademicClassAdapter
    private lateinit var academicClasses:ArrayList<AcademicClass>
    private val TAG = "discipline_detail"
    private lateinit var loadingDialog: LoadingDialog
    private var lastClickTime: Long = 0

    val listener = View.OnClickListener { view ->
        when(view.id){
            R.id.button_newClass -> {
                newAcademicClass()
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_discipline_detail)

        loadPreferences()
        loadObjects()
        setObjects()
        loadAdapter()
        loadAppBar()
    }

    private fun loadObjects(){
        textView_diciplineName = findViewById(R.id.textView_disciplineName)
        textView_diciplineDescription = findViewById(R.id.textView_disciplineDescription)
        textView_groupCode = findViewById(R.id.textView_groupCode)
        button_newClass = findViewById(R.id.button_newClass)
        loadingDialog = LoadingDialog(this)
    }

    @SuppressLint("SetTextI18n")
    private fun setObjects(){
        textView_diciplineName.text = discipline.name
        textView_diciplineDescription.text = discipline.description
        textView_groupCode.text = "Código da turma: " + group.code
        button_newClass.setOnClickListener(listener)
    }

    private fun loadPreferences(){
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
                adapter.setOnItemClickListener(object : AcademicClassAdapter.onItemClickListener {
                    override fun onItemClick(position: Int) {
                        val intent = Intent(this@DisciplineDetail, ClassManager::class.java)
                        intent.putExtra(getString(R.string.academic_class), academicClasses[position] as Serializable)
                        intent.putExtra(getString(R.string.group), group as Serializable)
                        startActivity(intent)
                    }
                })
            }
        }).start()
    }

    private fun getAcademicClasses():Boolean{
        if (!Connection().isOnline(this)){
            dialogError(getString(R.string.error_connect))
            return false
        }
        var result = false
        try{
            runOnUiThread { loadingDialog.startLoadingDialog() }
            academicClasses= academicClassDB.getClassByGroupID(group.id)
            result = true
        }catch (e:Exception){
            Log.e(TAG, "Erro ao buscar aulas.")
            result = false
        }finally {
            runOnUiThread { loadingDialog.dismissDialog() }
        }

        return result
    }

    private fun newAcademicClass() {
        val intent = Intent(this, ClassManager::class.java)
        intent.putExtra(getString(R.string.group), group as Serializable)
        startActivity(intent)
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
            var updated = false

            try {
                if (!this::adapter.isInitialized){
                    loadAdapter()
                }else{
                    updated = getAcademicClasses()
                    adapter.updateItens(academicClasses)
                    runOnUiThread { adapter.notifyDataSetChanged() }
                }
            }catch (e: Exception){
                Log.e(TAG, "Erro ao atualizar adapter: $e")
                updated = false
            }
            if (updated){
                runOnUiThread {
                    Toast.makeText(this, "Informações atualizadas.", Toast.LENGTH_SHORT).show()
                }
                Log.v(TAG, "Aulas do docente atualizadas.")
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