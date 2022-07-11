package com.spondere.entity

import java.io.Serializable

data class StudentManualFrequency(
    val groupID:Int,
    val studentID:Int,
    val fullName:String,
    var frequencyID:Int?,
    var isManual:Boolean
): Serializable