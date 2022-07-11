package com.spondere.entity

import java.io.Serializable

data class Group (val id:Int,
        val code:String,
        val active:Boolean,
        val semesterID:Int,
        val disciplineID: Int): Serializable