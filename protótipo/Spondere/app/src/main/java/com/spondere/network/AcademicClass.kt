package com.spondere.network

import android.content.Context
import android.util.Log
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.spondere.R
import com.spondere.entity.AcademicClass
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.CountDownLatch
import okio.IOException
import com.spondere.util.Token as TokenVerification

class AcademicClass(private var context: Context, private val token:String) {
    private var TAG = "CRUD_CLASS"
    private val client = OkHttpClient()
    private val baseURL:String = context.getString(R.string.url_base)
    private val route:String = "/aula"
    private val mapper = jacksonObjectMapper()
    private lateinit var academicClass:AcademicClass
    private val tokenVerification = TokenVerification(context)

    fun read(id:Int): AcademicClass {
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""
        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL$route/$id")
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
                        Log.v(TAG, "token : $records")
                    }
                    countRequest.countDown()
                }
            }
        })
        countRequest.await()

        if (records.isBlank()) throw Exception("Nenhum dado recebido do banco de dados.")
        val json = JSONObject(records)
        if (!json.has("academicClass")) throw Exception("Nenhum dado recebido do banco de dados.")
        val jsonClass:String = json.getJSONObject("academicClass").toString()

        academicClass = mapper.readValue(jsonClass)
        return academicClass
    }

    fun getClassByGroupID(groupID:Int): ArrayList<AcademicClass> {
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""
        val academicClasses:ArrayList<AcademicClass> = ArrayList()

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL$route/grupo/?groupID=$groupID")
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
        if(records.isEmpty()) throw Exception("Erro de requisição")
        val json = JSONObject(records)
        val classJson = json.getJSONArray("academicClass").toString()
        if (classJson.isBlank()) return academicClasses

        return mapper.readValue(classJson)
    }

    fun createClass(academicClass:AcademicClass): Int{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""
        val mediaType = "application/json".toMediaType()
        val jsonClass:JSONObject =  createJsonClass(academicClass)

        val body = jsonClass.toString().toRequestBody(mediaType)
        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL$route/")
            .method("POST", body)
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
        if(records.isEmpty()) throw Exception("Resposta do servidor vazia.")
        val json = JSONObject(records)
        if (!json.has("id")) throw Exception("Campo id não existe.")

        return json.getInt("id")
    }

    fun updateClass(academicClass:AcademicClass): Boolean{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        if(academicClass.id < 1) return false
        var records = ""
        val mediaType = "application/json".toMediaType()
        val jsonBody:JSONObject =  createJsonClass(academicClass)
        val body = jsonBody.toString().toRequestBody(mediaType)
        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL$route/")
            .method("PUT", body)
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
        if(records.isEmpty()) return false
        val json = JSONObject(records)
        if (!json.has("result")) return false

        return true
    }

    fun blockClass(id:Int): Boolean{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        if(id <= 0) return false
        var records = ""
        val mediaType = "application/json".toMediaType()
        val body = "".toRequestBody(mediaType)
        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL$route/bloquear/?academicClassID=$id")
            .method("PUT", body)
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
        if(records.isEmpty()) return false
        val json = JSONObject(records)
        if (!json.has("result")) return false
        val result = json.getString("result")

        return (result == "success")
    }

    private fun createJsonClass(academicClass: AcademicClass):JSONObject{
        val jsonBody=JSONObject()

        jsonBody.put("id", academicClass.id)
        jsonBody.put("groupID", academicClass.groupID)
        jsonBody.put("titleClass", academicClass.titleClass)
        jsonBody.put("descriptionClass", academicClass.descriptionClass)
        jsonBody.put("beginDate", academicClass.beginDate)
        jsonBody.put("endDate", academicClass.endDate)
        jsonBody.put("longitude", academicClass.longitude)
        jsonBody.put("latitude", academicClass.latitude)
        jsonBody.put("activeValidation", academicClass.activeValidation)
        jsonBody.put("validationByQrCode", academicClass.validationByQrCode)
        jsonBody.put("validationByBLE", academicClass.validationByBLE)
        jsonBody.put("blockedAttendance", academicClass.blockedAttendance)
        jsonBody.put("validationCode", academicClass.validationCode)

        return jsonBody
    }
}