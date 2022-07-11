package com.spondere.util

import android.app.Activity
import androidx.appcompat.app.AlertDialog
import com.google.android.material.dialog.MaterialAlertDialogBuilder
import com.spondere.R

class LoadingDialog (private var activity:Activity){
    private val dialog = MaterialAlertDialogBuilder(activity)
    private lateinit var loading: AlertDialog

    fun startLoadingDialog(){
        dialog.setView(R.layout.loading_dialog)
            .setCancelable(false)

        loading = dialog.create()
        loading.show()
    }

    fun dismissDialog(){
        if (this::loading.isInitialized) loading.dismiss()
    }

}