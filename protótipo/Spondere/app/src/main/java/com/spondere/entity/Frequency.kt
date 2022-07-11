package com.spondere.entity

import java.io.Serializable

data class Frequency(
    val id:Int?,
    val studentID:Int,
    val academicClassID:Int,
    val ManualAttendance:Boolean,
    val BLEAttendance:Boolean,
    val QrCodeAttendance:Boolean,
    val createDate:String?,
    val validationCode:String?,
    val latitude:Double?,
    val longitude:Double?,
    val failure:String?,
    val photo:ByteArray?
):Serializable