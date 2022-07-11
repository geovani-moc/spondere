package com.spondere.network

import android.content.Context
import android.util.Log
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.spondere.R
import com.spondere.entity.User
import okhttp3.*
import okio.IOException
import org.json.JSONObject
import java.util.concurrent.CountDownLatch
import com.spondere.util.Token as TokenVerification

class User (private var context: Context, private val token:String){
    private var TAG = "CRUD_USER"
    private val mapper = jacksonObjectMapper()
    private var user = User()
    private val tokenVerification = TokenVerification(context)

    fun read():User {
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        val client = OkHttpClient()
        val baseURL:String = context.getString(R.string.url_base)
        val route:String = "/usuario"
        var records:String = ""

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url(baseURL + route)
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
        if (records.isNullOrEmpty()) throw Exception("Erro, retorno vazio.")

        var userJson = JSONObject(records).getJSONObject("user").toString()
        user = mapper.readValue(userJson, User::class.java)

        return user
    }
}