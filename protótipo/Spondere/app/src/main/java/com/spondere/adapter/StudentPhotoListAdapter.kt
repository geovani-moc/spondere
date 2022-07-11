package com.spondere.adapter

import android.content.Context
import android.graphics.Bitmap
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.spondere.R
import com.spondere.entity.StudentPhoto

class StudentPhotoListAdapter(
    private val context: Context,
    private val students: ArrayList<StudentPhoto>,
):
    RecyclerView.Adapter<StudentPhotoListAdapter.ViewHolder>() {
        private val TAG = "StudentPhotoListAdapter"
        private lateinit var mListener: onItemClickListener

        interface onItemClickListener{
            fun onItemClick(position: Int)
        }

        fun setOnItemClickListener(listener: onItemClickListener){
            mListener = listener
        }

        override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): StudentPhotoListAdapter.ViewHolder {
            val viewItem = LayoutInflater
                .from(parent.context)
                .inflate(R.layout.student_photo_item, parent, false)
            return ViewHolder(viewItem, mListener)
        }

        override fun onBindViewHolder(holder: StudentPhotoListAdapter.ViewHolder, position: Int) {
            holder.textView_name.text = students[position].name
            try {
                val height = 100
                val originalWidth = students[position].photo.width
                val originalHeight = students[position].photo.height
                val scale:Double = height.toDouble() / originalHeight;
                val with = (originalWidth/scale).toInt()
                holder.imageView_photo.setImageBitmap(
                    Bitmap.createScaledBitmap(students[position].photo,
                        with,
                        height,
                        false))
            }catch (e:Exception) {
                Log.e(TAG, "Falha ao exibir imagem, $e")
            }

        }

        override fun getItemCount(): Int {
            return students.size
        }

        fun updateItens(students: ArrayList<StudentPhoto>) {
            this.students.clear()
            this.students.addAll((students))
        }

        inner class ViewHolder(itemView: View, listener: onItemClickListener): RecyclerView.ViewHolder(itemView){
            lateinit var textView_name: TextView
            lateinit var imageView_photo: ImageView

            init {
                textView_name = itemView.findViewById(R.id.textview_name)
                imageView_photo = itemView.findViewById(R.id.imageView_photo)

                itemView.setOnClickListener {
                    listener.onItemClick(adapterPosition)
                }
            }
        }
}