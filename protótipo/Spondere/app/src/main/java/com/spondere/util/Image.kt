package com.spondere.util

import android.graphics.Bitmap
import android.graphics.BitmapFactory
import java.io.ByteArrayOutputStream

class Image {

    public fun resizeCompactImage(image:ByteArray):ByteArray{
        val bitmap = BitmapFactory.decodeByteArray(image,0, image.size)
        val width = 480
        val factor:Double = bitmap.width/width.toDouble()
        val height = (bitmap.height/factor).toInt()
        val stream = ByteArrayOutputStream()

        Bitmap.createScaledBitmap(bitmap, width, height, false)
            .compress(Bitmap.CompressFormat.JPEG, 90, stream)

        return stream.toByteArray()
    }
}