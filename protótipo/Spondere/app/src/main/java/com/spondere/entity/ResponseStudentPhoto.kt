package com.spondere.entity

import com.fasterxml.jackson.annotation.JsonAlias
import com.fasterxml.jackson.annotation.JsonProperty

data class ResponseStudentPhoto(
    @JsonProperty("name")
    val name:String,
    @JsonProperty("biometry")
    val biometry:Boolean,
    @JsonProperty("encode")
    val encode:String?,
    @JsonProperty("image")
    val image:String?
)
