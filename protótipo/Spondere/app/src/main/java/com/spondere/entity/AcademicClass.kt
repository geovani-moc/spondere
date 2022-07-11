package com.spondere.entity

import com.fasterxml.jackson.annotation.JsonAlias
import com.fasterxml.jackson.annotation.JsonProperty
import java.io.Serializable

data class AcademicClass(
    @JsonProperty ("id")
    var id:Int,
    @JsonProperty ("groupid")
    @JsonAlias("groupID")
    val groupID:Int,
    @JsonProperty ("titleclass")
    @JsonAlias("titleClass")
    val titleClass:String,
    @JsonProperty ("descriptionclass")
    @JsonAlias("descriptionClass")
    val descriptionClass:String?,
    @JsonProperty ("begindate")
    @JsonAlias("beginDate")
    val beginDate: String?,
    @JsonProperty ("enddate")
    @JsonAlias("endDate")
    val endDate:String?,
    @JsonProperty ("longitude")
    val longitude:Double?,
    @JsonProperty ("latitude")
    val latitude:Double?,
    @JsonProperty ("activevalidation")
    @JsonAlias("activeValidation")
    val activeValidation:Boolean,
    @JsonProperty ("validationbyqrcode")
    @JsonAlias("validationByQrCode")
    val validationByQrCode:Boolean,
    @JsonProperty ("validationbyble")
    @JsonAlias("validationByBLE")
    val validationByBLE:Boolean,
    @JsonProperty ("blockedattendance")
    @JsonAlias("blockedAttendance")
    var blockedAttendance:Boolean,
    @JsonProperty ("validationcode")
    @JsonAlias("validationCode")
    val validationCode:String?):Serializable
