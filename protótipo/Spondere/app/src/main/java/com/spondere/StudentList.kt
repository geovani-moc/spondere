package com.spondere

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.SystemClock
import android.util.Log
import android.widget.Toast
import androidx.appcompat.widget.Toolbar
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.spondere.adapter.StudentListAdapter
import com.spondere.entity.AcademicClass
import com.spondere.entity.StudentManualFrequency
import com.spondere.util.Connection
import com.spondere.util.LoadingDialog
import com.spondere.network.Frequency as FrequencyDB
import com.spondere.util.Preferences
import com.spondere.network.Group as GroupDB

class StudentList : AppCompatActivity() {
    private lateinit var academicClass:AcademicClass
    private lateinit var preferences:Preferences
    private val TAG = "student_list"
    private lateinit var token:String
    private lateinit var frequencyDB:FrequencyDB
    private lateinit var recyclerView_studentList: RecyclerView
    private lateinit var groupDB:GroupDB
    private lateinit var toolbar: Toolbar
    private lateinit var adapter: StudentListAdapter
    private lateinit var loadingDialog: LoadingDialog
    private var lastClickTime: Long = 0
    private lateinit var students:ArrayList<StudentManualFrequency>

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_student_list)

        readPreferences()
        loadObjects()
        setObjects()
        loadAdapter()
        loadAppBar()
    }

    private fun loadObjects(){
        loadingDialog = LoadingDialog(this)
    }

    private fun readPreferences(){
        academicClass = intent!!.extras!!.get(getString(R.string.academic_class)) as AcademicClass
        preferences = Preferences(getString(R.string.settings_login), this)
        token = preferences.loadData(getString(R.string.token)).toString()
        frequencyDB = FrequencyDB(this, token)
        groupDB = GroupDB(this, token)
    }

    private fun setObjects(){

    }

    private fun getStudents():Boolean{
        var result = false
        if (token.isNotBlank()) {
            if (!Connection().isOnline(this)){
                runOnUiThread{ dialogError(getString(R.string.error_connect))}
                return false
            }
            try {
                runOnUiThread{ loadingDialog.startLoadingDialog()}
                students = groupDB.readAttendanceList(academicClass.id, academicClass.groupID)

                result = true
            }catch (e: Exception) {
                Log.e(TAG, "e")
            }finally {
                runOnUiThread { loadingDialog.dismissDialog()}
            }
        }
        return result
    }

    private fun loadAdapter(){
        Thread(Runnable {
            getStudents()
            adapter = StudentListAdapter(this, students)
            recyclerView_studentList = findViewById(R.id.recyclerView_studentList)
            runOnUiThread {
                recyclerView_studentList.layoutManager = LinearLayoutManager(this)
                recyclerView_studentList.adapter = adapter
                adapter.setOnItemClickListener(object : StudentListAdapter.onItemClickListener {
                    override fun onItemClick(position: Int) {
                        changeStudentAttendance(position)
                    }
                })
            }
        }).start()
    }

    private fun changeStudentAttendance(position:Int){
        if ((!students[position].isManual) && (students[position].frequencyID != null)){
            runOnUiThread {
                MaterialAlertDialogBuilder(this@StudentList)
                    .setTitle("Ação indisponível")
                    .setMessage("Usuários que comprovaram presença por biometria não podem ter sua presença removida.")
                    .setCancelable(false)
                    .setPositiveButton("OK"
                    ) { dialog, which -> dialog?.dismiss() }
                    .show()
            }
            return
        }else if((students[position].isManual) && (students[position].frequencyID != null)){
            MaterialAlertDialogBuilder(this@StudentList)
                .setTitle("Atenção")
                .setMessage("Deseja realmente remover esta presença?")
                .setCancelable(false)
                .setNegativeButton("Não") { dialog, which ->
                    dialog?.dismiss()
                    Log.e(TAG, "cancelado(apagar frequencia).")
                }
                .setPositiveButton("Sim"){ dialog, which ->
                    Thread(Runnable {
                        try {
                            students[position].frequencyID?.let {
                                frequencyDB.deleteManualFrequency(it)
                            }
                            students[position].frequencyID = null
                            students[position].isManual = false
                        }catch (e:Exception){
                            Log.e(TAG, "Erro ao deletar frequência manual: $e")
                        }finally {
                            runOnUiThread { adapter.notifyDataSetChanged() }
                        }
                    }).start()
                }
                .show()

        }else if ((!students[position].isManual) && (students[position].frequencyID == null) ){
            Thread(Runnable {
                try {
                    val id =  frequencyDB.createManualFrequency(academicClass.id, students[position].studentID)
                    students[position].frequencyID = id
                    students[position].isManual = true
                    runOnUiThread { adapter.notifyDataSetChanged() }
                }catch (e:Exception){Log.e(TAG, "Erro ao criar frequência manual: $e")}
            }).start()
        }
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
                    updated = getStudents()
                    adapter.updateItens(students)
                    runOnUiThread { adapter.notifyDataSetChanged() }
                }
            }catch (e: Exception){
                Log.e(TAG, "Erro ao atualizar adapter: $e")
            }
            if (updated){
                runOnUiThread{
                    Toast.makeText(this, "Informações atualizadas.", Toast.LENGTH_SHORT).show()
                }
                Log.v(TAG, "Lista de discentes atualizadas.")
            }
        }).start()
    }

    private fun confirmDialog(text:String):Boolean{
        var result = false
        MaterialAlertDialogBuilder(this@StudentList)
            .setTitle("Atenção")
            .setMessage(text)
            .setCancelable(false)
            .setNegativeButton("Não") { dialog, which ->
                dialog?.dismiss()
                result = false
            }
            .setPositiveButton("Sim"){ dialog, which ->
                result = true
            }
            .show()
        return result
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