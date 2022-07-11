package com.spondere.network

import android.content.Context
import android.util.Log
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.spondere.R
import com.spondere.entity.Discipline
import com.spondere.entity.Group
import okhttp3.*
import okio.IOException
import org.json.JSONObject
import java.util.concurrent.CountDownLatch
import com.spondere.util.Token as TokenVerification

class Discipline(private var context:Context, private var token:String) {
    private val TAG = "discipline"
    private val client = OkHttpClient()
    private val baseURL:String = context.getString(R.string.url_base)
    private val route:String = "/disciplina"
    private val tokenVerification = TokenVerification(context)

    fun getDisciplinesByProfessor(username:String):
            Pair<ArrayList<Discipline>, ArrayList<Group> >{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records:String = ""
        var disciplines:ArrayList<Discipline> = ArrayList<Discipline>()
        var groups:ArrayList<Group> = ArrayList()

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL$route/professor/?professorUsername=$username")
            .method("GET", null)
            .addHeader("Authorization", "Bearer $token")
            .build()

        Log.v(TAG, "Requisição criada.")
        val countRequest = CountDownLatch(1)

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e(TAG, e.printStackTrace().toString())
                Log.v(TAG, "Não foi possivel realizar a requisição.")
                records = ""
                countRequest.countDown()
            }

            override fun onResponse(call: Call, response: Response) {
                response.use {
                    if (!response.isSuccessful || response.code != 200) {
                        records = ""
                    } else {
                        records = response.body!!.string()
                        Log.v(TAG, "Requisição realizada com sucesso")
                        Log.v(TAG, "Result : $records")
                    }
                    countRequest.countDown()
                }
            }
        })

        countRequest.await()
        if(records.isEmpty()) return Pair(disciplines, groups)

        var json = JSONObject(records)
        var disciplineJson = json.getJSONArray("discipline").toString()
        var groupJson = json.getJSONArray("group").toString()

        if (disciplineJson.isNullOrEmpty() or groupJson.isNullOrEmpty())
            return Pair(disciplines, groups)

        disciplines = jacksonObjectMapper().readValue(disciplineJson)
        groups = jacksonObjectMapper().readValue(groupJson)

        return Pair(disciplines, groups)
    }

    fun getDisciplinesByStudent(username:String):
            Pair<ArrayList<Discipline>, ArrayList<Group> >{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""
        var disciplines:ArrayList<Discipline> = ArrayList()
        var groups:ArrayList<Group> = ArrayList()

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL$route/aluno/?studentUsername=$username")
            .method("GET", null)
            .addHeader("Authorization", "Bearer $token")
            .build()

        Log.v(TAG, "Requisição criada.")
        val countRequest = CountDownLatch(1)

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                Log.e(TAG, e.printStackTrace().toString())
                Log.v(TAG, "Não foi possivel realizar a requisição.")
                records = ""
                countRequest.countDown()
            }

            override fun onResponse(call: Call, response: Response) {
                response.use {
                    if (!response.isSuccessful || response.code != 200) {
                        records = ""
                    } else {
                        records = response.body!!.string()
                        Log.v(TAG, "Requisição realizada com sucesso")
                        Log.v(TAG, "Result : $records")
                    }
                    countRequest.countDown()
                }
            }
        })

        countRequest.await()
        if(records.isEmpty()) return Pair(disciplines, groups)

        var json = JSONObject(records)
        var disciplineJson = json.getJSONArray("discipline").toString()
        var groupJson = json.getJSONArray("group").toString()

        if (disciplineJson.isNullOrEmpty() or groupJson.isNullOrEmpty())
            return Pair(disciplines, groups)

        disciplines = jacksonObjectMapper().readValue(disciplineJson)
        groups = jacksonObjectMapper().readValue(groupJson)

        return Pair(disciplines, groups)
    }
}


