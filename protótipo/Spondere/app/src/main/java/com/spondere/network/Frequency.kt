package com.spondere.network

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Base64
import android.util.Log
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.spondere.R
import com.spondere.entity.ResponseStudentPhoto
import com.spondere.entity.StudentPhoto
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import okio.IOException
import org.json.JSONObject
import java.util.concurrent.CountDownLatch
import com.spondere.util.Token as TokenVerification
import kotlin.collections.ArrayList

class Frequency(private var context: Context, private val token:String) {
    private var TAG = "CRUD_FREQUENCY"
    private val client = OkHttpClient()
    private val baseURL:String = context.getString(R.string.url_base)
    private val route:String = "/validacao"
    private val tokenVerification = TokenVerification(context)

    fun checkValidationCode(validationCode:String):Int{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records:String = ""

        val mediaType = "application/json".toMediaType()
        val body = "\"$validationCode\"".toRequestBody(mediaType)

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL$route/verificar/")
            .method("POST", body)
            .addHeader("Authorization", "Bearer $token")
            .addHeader("Accept", "application/json")
            .addHeader("Content-Type", "application/json")
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
                    if (response.isSuccessful && response.code == 200){
                        records = response.body!!.string()
                        Log.v(TAG, "Requisição realizada com sucesso.")
                        Log.v(TAG, "Response: $records" )
                    }
                    countRequest.countDown()
                }
            }
        })

        countRequest.await()
        if(records.isBlank()) throw Exception("Erro de requisição")

        val json = JSONObject(records)
        if (!json.has("classID")) throw Exception("Campo classID vazio.")

        return json.getInt("classID")
    }

    fun beginFrequency(classID:Int):String{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""
        var validationCode = ""
        val mediaType = "application/json".toMediaType()
        val body = classID.toString().toRequestBody(mediaType)

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL$route/criar")
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
        if(records.isEmpty()) throw Exception("Erro de requisição")
        var json = JSONObject(records).getString("validationCode")
        if (json.isNullOrEmpty()) throw Exception("Retorno vazio.")
        validationCode = json.toString()

        return validationCode
    }

    fun createManualFrequency(classID: Int, studentID: Int):Int{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records:String = ""
        val mediaType = "application/json".toMediaType()
        val jsonBody = JSONObject()

        jsonBody.put("academicClassID", classID)
        jsonBody.put("studentID", studentID)
        val body = jsonBody.toString().toRequestBody(mediaType)

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL/frequencia/manual")
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
                    if (response.isSuccessful && response.code == 200){
                        records = response.body!!.string()
                        Log.v(TAG, "Requisição realizada com sucesso.")
                        Log.v(TAG, "Response: $records" )
                    }

                    countRequest.countDown()
                }
            }
        })

        countRequest.await()
        if(records.isEmpty()) throw Exception("Resposta vazia.")

        val json = JSONObject(records)
        if (!json.has("id")) throw Exception("Erro, campo id não existe.")

        return json.getInt("id")
    }

    fun deleteManualFrequency(id:Int){
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records:String = ""
        var result:String? = null

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL/frequencia/$id")
            .method("DELETE", null)
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
                    if (response.isSuccessful && response.code == 200) {
                        records = response.body!!.string()
                        Log.v(TAG, "Requisição realizada com sucesso.")
                        Log.v(TAG, "Response: $records" )
                    }

                    countRequest.countDown()
                }
            }
        })

        countRequest.await()
        if(records.isEmpty()) throw Exception("Erro ao apagar frequência")

        val json = JSONObject(records)
        if (!json.has("result")) throw Exception("Erro ao apagar frequência")

        result = json.getString("result")
        if (result.isNullOrBlank()) throw Exception("Erro ao apagar frequência")
    }

    fun isPresent(academicClassID:Int, studentID:Int):Pair<Int, String?>{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""
        var code = 0;

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL/frequencia/aluno/?academicClassID=$academicClassID&studentID=$studentID")
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
                    code = response.code
                    records = response.body!!.string()
                    when(code){
                        200 ->{
                            Log.v(TAG, "Requisição realizada com sucesso")
                            Log.v(TAG, "Result : $records")
                        }
                        403 ->{
                            Log.v(TAG, "Nenhum dado retornado")
                        }
                        else -> {
                            Log.v(TAG, "Codigo não tratado: $code")
                            records = ""
                        }

                    }
                    countRequest.countDown()
                }
            }
        })

        countRequest.await()
        if (code == 403){
            return Pair(-1, null)
        }

        if(records.isEmpty()) throw Exception("Erro, retorno vazio.")
        val json = JSONObject(records)
        if (!json.has("id")) throw Exception("Erro, campo id não existe.")
        if (!json.has("failure")) throw Exception("Erro, campo failure não existe.")

        val id = json.getInt("id")

        val failure = if(json.isNull("failure")) null
        else json.getString("failure")

        return Pair(id, failure)
    }

    fun studentWithPhotoPresent(academicClassID:Int):ArrayList<StudentPhoto>{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""
        var code = 0;

        val request = Request.Builder()
            .addHeader("content-type", "application/json")
            .url("$baseURL/frequencia/alunos_fotos/?academicClassID=${academicClassID}")
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
                    code = response.code
                    records = response.body!!.string()
                    when(code){
                        200 ->{
                            Log.v(TAG, "Requisição realizada com sucesso")
                        }
                        else -> {
                            Log.v(TAG, "Codigo não tratado: $code")
                            records = ""
                        }

                    }
                    countRequest.countDown()
                }
            }
        })

        countRequest.await()
        if (code != 200) throw Exception("Erro, a requisição falhou.")

        if (records.isNullOrBlank()) throw Exception("Resposta vazia.")
        return createListOfStudentPhoto(records)
    }

    private fun createListOfStudentPhoto(presents:String):ArrayList<StudentPhoto>{
        val students = decodePresentsJson(presents)
        val studentsPhoto = ArrayList<StudentPhoto>()

        for ((name, imageBase64) in students){
            if (imageBase64.isNotBlank()){
                val decodedBytesImage: ByteArray = Base64.decode(imageBase64, Base64.DEFAULT)
                val image = BitmapFactory.decodeByteArray(decodedBytesImage, 0, decodedBytesImage.size)
                studentsPhoto.add(StudentPhoto(name, image))
            }else{
                var image = BitmapFactory.decodeResource(context.resources , R.drawable.ic_spondere_ico)
                image = Bitmap.createScaledBitmap(image, 100, 100, false)
                studentsPhoto.add(StudentPhoto(name, image))
            }
        }

        return studentsPhoto
    }

    private fun decodePresentsJson(presents:String):ArrayList<Pair<String,String>>{
        val noImage = ""
        val mapper = jacksonObjectMapper()
        val students = ArrayList<Pair<String, String>>()

        val json = JSONObject(presents)
        val classJson = json.getJSONArray("presents").toString()
        val jsonObjects: List<ResponseStudentPhoto> = mapper.readValue(classJson)

        for (item in jsonObjects) {
            Log.i(TAG, "Codificação da imagem: ${item.encode}")
            if (item.biometry){
                students.add(Pair(item.name, item.image!!))
            }else{
                students.add(Pair(item.name, noImage))
            }
         }

        return students
    }

    fun attendanceRate(classID: Int):Pair<Int, Int>{
        if (!tokenVerification.verify(token)) throw Exception("Token inválido.")
        var records = ""
        var code = 0;

        val request = Request.Builder()
            .addHeader("Accept", "application/json")
            .url("$baseURL/frequencia/taxa_presenca/$classID")
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
                    code = response.code
                    records = response.body!!.string()
                    when(code){
                        200 ->{
                            Log.v(TAG, "Requisição realizada com sucesso")
                            Log.v(TAG, "Result : $records")
                        }
                        else -> {
                            Log.v(TAG, "Código não tratado: $code")
                            records = ""
                        }

                    }
                    countRequest.countDown()
                }
            }
        })

        countRequest.await()

        if(records.isEmpty()) throw Exception("Erro, retorno vazio.")
        val json = JSONObject(records)

        if (!json.has("students")) throw Exception("Erro, campo students não existe.")
        if (!json.has("presents")) throw Exception("Erro, campo presents não existe.")

        val numberStudents = json.getInt("students")
        val numberPresents = json.getInt("presents")

        return Pair(numberStudents, numberPresents)
    }
}