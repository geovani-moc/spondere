package com.spondere.util

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.util.Base64
import android.util.Log
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.google.gson.JsonArray
import com.google.gson.JsonObject
import com.google.gson.JsonParser
import com.spondere.entity.ResponseStudentPhoto
import com.spondere.entity.StudentPhoto
import org.json.JSONObject
import org.json.JSONTokener
import java.io.ByteArrayInputStream
import java.io.IOException
import java.nio.charset.Charset
import java.util.zip.ZipEntry
import java.util.zip.ZipInputStream

class Zip {

    private val TAG = "util_zip"

    fun zipToStudentPhoto(zipResponse:ByteArray):ArrayList<StudentPhoto>{
        val streamZip = ZipInputStream(ByteArrayInputStream(zipResponse))
        var presents = ""
        try {
            var entry:ZipEntry? = null
            while (streamZip.nextEntry.also { entry = it } != null) {
                val file = readDataFromZipStream(streamZip, entry!!)
                if(entry!!.name == "presents.json"){
                    presents = String(file, Charset.forName("UTF-8"))
                    break
                }
            }
        }catch (e:Exception){
            Log.e(TAG, e.toString())
        } finally {
            streamZip.closeEntry()
        }

        return createListOfStudentPhoto(presents)
    }

    @Throws(IOException::class)
    private fun readDataFromZipStream(zipStream: ZipInputStream, entry: ZipEntry): ByteArray {
        val data = ByteArray(entry.size.toInt())
        zipStream.read(data)
        return data
    }

    private fun createListOfStudentPhoto(presents:String):ArrayList<StudentPhoto>{
        val students = decodePresentsJson(presents)
        val studentsPhoto = ArrayList<StudentPhoto>()

        for ((name, imageBase64) in students){
            val decodedBytesImage: ByteArray = Base64.decode(imageBase64, Base64.DEFAULT)
            val image = BitmapFactory.decodeByteArray(decodedBytesImage, 0, decodedBytesImage.size)
            studentsPhoto.add(StudentPhoto(name, image))
        }

        return studentsPhoto
    }

    private fun decodePresentsJson(presents:String):ArrayList<Pair<String,String>>{
        val mapper = jacksonObjectMapper()
        val temp = """{"presents":[{"name": "James Warman", "biometry": true, "encode": "jpg/base64", "image": "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"}, {"name": "Flavia Miles", "biometry": false, "encode": null, "image": null}]}"""

        val json = JSONObject(temp)
        val classJson = json.getJSONArray("presents").toString()
        val students = ArrayList<Pair<String, String>>()
        //val jsonObjects = mapper.readValue(classJson)
        val jsonObjects: List<ResponseStudentPhoto> = mapper.readValue(classJson)
        //val jsonObject = JsonParser().parse(presents).asJsonObject
        //val jsonArray = jsonObject.getAsJsonArray("presents")

        Log.i(TAG, presents)

        for (json in jsonObjects){
            Log.i(TAG, json.toString())
        }

       /* for (i in 0 until jsonArray.length()) {
            val jsonStudent = jsonArray.getJSONObject(i)
            val name = jsonStudent.getString("name")
            val biometry = jsonStudent.getBoolean("biometry")
            val encode = jsonStudent.getString("encode")
            val imageBase64 = jsonStudent.getString("image")

            Log.i(TAG, "Codificação da imagem: $encode")
            if (biometry){
                students.add(Pair(name, imageBase64))
            }else{
                students.add(Pair(name, ""))
            }
        }*/

        return students
    }
}