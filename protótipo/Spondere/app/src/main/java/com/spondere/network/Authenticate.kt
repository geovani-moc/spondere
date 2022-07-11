package com.spondere.network

import android.content.Context
import android.util.Log
import com.spondere.R
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okio.IOException
import org.json.JSONObject
import java.util.concurrent.CountDownLatch
import okhttp3.OkHttpClient
import okhttp3.RequestBody.Companion.toRequestBody


class Authenticate(private var context: Context) {
    private val TAG = "autenticacao"
    private val client = OkHttpClient()
    private val baseURL:String = context.getString(R.string.url_base)
    private val route:String = "/usuario/login"

    fun loginJWT(userName: String, password: String): Pair<String, String> {
        var records: String = ""
        var detail = ""
        var mediaType = "application/json".toMediaType()
        val json = JSONObject()

        json.put("username", userName)
        json.put("password", password)

        val body = json.toString().toRequestBody(mediaType)

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url(baseURL + route)
            .method("POST", body)
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
                    records = response.body!!.string()
                    if (response.code == 406 ){
                        detail = JSONObject(records).getString("detail")
                        if (detail != "u001") detail = ""
                    }
                    if (!response.isSuccessful || response.code != 200) {
                        records = ""
                    } else {
                        Log.v(TAG, "Requisição realizada com sucesso")
                        Log.v(TAG, "token : $records")
                    }
                    countRequest.countDown()
                }
            }
        })

        countRequest.await()

        if (records.isNullOrEmpty()){
            return Pair("", detail)
        }
        val jsonToken = JSONObject(records)
        if (!jsonToken.has("token")) throw Exception("Campo token não localizado.")

        return Pair(jsonToken.getString("token"), detail)
    }

}
