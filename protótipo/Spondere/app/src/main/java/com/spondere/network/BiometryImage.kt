package com.spondere.network

import android.content.Context
import android.util.Log
import com.spondere.R
import com.spondere.entity.Frequency
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import okio.IOException
import org.json.JSONObject
import java.util.concurrent.CountDownLatch
import com.spondere.util.Token as TokenVerification

class BiometryImage(private var context: Context, private val token:String) {
    private val TAG = "biometryImage"
    private val client = OkHttpClient()
    private val baseURL:String = context.getString(R.string.url_base)
    private val route:String = "/biometria"
    private val tokenVerification = TokenVerification(context)

    fun checkImage(image: ByteArray, frequency: Frequency):String{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""
        val urlParameters = "?studentID=${frequency.studentID}&classID=${frequency.academicClassID}" +
                "&ble=${frequency.BLEAttendance}&qrcode=${frequency.QrCodeAttendance}" +
                "&validationCode=${frequency.validationCode}&latitude=${frequency.latitude}" +
                "&longitude=${frequency.longitude}"

        val body = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart("file", "selfie_${frequency.studentID}_${frequency.academicClassID}.jpg",
                  image.toRequestBody("application/octet-stream".toMediaTypeOrNull(), 0, image.size))
            .build()

        val request = Request.Builder()
            .addHeader("Accept", "application/json")
            .addHeader("Content-Type", "multipart/form-data")
            .addHeader("Authorization", "Bearer $token")
            .url("${baseURL}${route}/checar/${urlParameters}")
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
                    if (!response.isSuccessful || response.code != 200) {
                        countRequest.countDown()
                        return
                    }

                    records = response.body!!.string()
                    Log.v(TAG, "Requisição realizada com sucesso.")
                    Log.v(TAG, "Response: $records" )
                    countRequest.countDown()
                }
            }
        })
        countRequest.await()
        if(records.isEmpty()) throw Exception("Response vazio.")

        val json = JSONObject(records)
        if (!json.has("result")) throw Exception("Campo \"result\" não encontrado na resposta do servidor.")

        return json.getString("result")
    }

    fun checkStatus(userID:Int):Pair<Int, String>{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""
        var id = 0
        var error = ""

        val request = Request.Builder()
            .addHeader("Accept", "application/json")
            .addHeader("Content-Type", "application/json")
            .addHeader("Authorization", "Bearer $token")
            .url("${baseURL}${route}/valida/${userID}")
            .method("GET", null)
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
                        countRequest.countDown()
                        return
                    }

                    records = response.body!!.string()
                    Log.v(TAG, "Requisição realizada com sucesso.")
                    Log.v(TAG, "Response: $records" )
                    countRequest.countDown()
                }
            }
        })
        countRequest.await()
        if(records.isEmpty()) throw Exception("Response vazio.")

        val json = JSONObject(records)
        if (!json.has("biometryID")) throw Exception("Campo \"biometryID\" não encontrado na resposta do servidor.")
        if (!json.has("biometryError")) throw Exception("Campo \"biometryError\" não encontrado na resposta do servidor.")

        if (!json.isNull("biometryID")){
            id = json.getInt("biometryID")
        }
        if (!json.isNull("biometryError")){
            error =  json.getString("biometryError")
        }

        return Pair(id,error)
    }

    fun create(userID: Int, photos: ArrayList<ByteArray>):Int{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""

        val body = MultipartBody.Builder().setType(MultipartBody.FORM)

        var count = 1
        for (photo in photos){
            body.addFormDataPart("files",  "selfie_${userID}_$count.jpg",
                photo.toRequestBody("application/octet-stream".toMediaTypeOrNull(), 0, photo.size))
            count+=1
        }

        val request = Request.Builder()
            .addHeader("Accept", "application/json")
            .addHeader("Content-Type", "multipart/form-data")
            .addHeader("Authorization", "Bearer $token")
            .url("${baseURL}${route}/${userID}")
            .method("POST", body.build())
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
                        countRequest.countDown()
                        return
                    }

                    records = response.body!!.string()
                    Log.v(TAG, "Requisição realizada com sucesso.")
                    Log.v(TAG, "Response: $records" )
                    countRequest.countDown()
                }
            }
        })
        countRequest.await()
        if(records.isEmpty()) throw Exception("Response vazio.")

        val json = JSONObject(records)
        if (!json.has("id")) throw Exception("Campo \"id\" não encontrado na resposta do servidor.")

        return json.getInt("id")
    }

    fun addPhotoInValidBiometry(biometryID: Int, photos: ArrayList<ByteArray>):String{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""

        val body = MultipartBody.Builder().setType(MultipartBody.FORM)

        var count = 1
        for (photo in photos){
            body.addFormDataPart("files",  "selfie_$count.jpg",
                photo.toRequestBody("application/octet-stream".toMediaTypeOrNull(), 0, photo.size))
            count+=1
        }

        val request = Request.Builder()
            .addHeader("Accept", "application/json")
            .addHeader("Content-Type", "multipart/form-data")
            .addHeader("Authorization", "Bearer $token")
            .url("${baseURL}${route}/adicionar_fotos/${biometryID}")
            .method("PUT", body.build())
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
                        Log.i(TAG, response.body!!.string())
                        countRequest.countDown()
                        return
                    }

                    records = response.body!!.string()
                    Log.v(TAG, "Requisição realizada com sucesso.")
                    Log.v(TAG, "Response: $records" )
                    countRequest.countDown()
                }
            }
        })
        countRequest.await()
        if(records.isEmpty()) throw Exception("Response vazio.")

        val json = JSONObject(records)
        if (!json.has("result")) throw Exception("Campo \"result\" não encontrado na resposta do servidor.")

        return json.getString("result")
    }
}