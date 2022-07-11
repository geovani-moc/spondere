package com.spondere.entity

data class User(
    val id: Int? = null,
    var username: String? = null,
    var password: String? = null,
    var email: String? = null,
    var fullName: String? = null,
    var disabled: Boolean = false,
    var professor: Boolean = false,
    var student: Boolean = false,
    var administrator: Boolean = false,
)