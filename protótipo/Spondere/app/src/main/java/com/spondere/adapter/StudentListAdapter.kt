package com.spondere.adapter

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.core.view.isVisible
import androidx.recyclerview.widget.RecyclerView
import com.spondere.R
import com.spondere.entity.StudentManualFrequency

class StudentListAdapter (
    private val context: Context,
    private val studentsList: ArrayList<StudentManualFrequency>):

    RecyclerView.Adapter<StudentListAdapter.ViewHolder>() {
    private lateinit var mListener: onItemClickListener

    interface onItemClickListener{
        fun onItemClick(position: Int)
    }

    fun setOnItemClickListener(listener: onItemClickListener){
        mListener = listener
    }

    fun updateItens(students:ArrayList<StudentManualFrequency>) {
        this.studentsList.clear()
        this.studentsList.addAll(students)

    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): StudentListAdapter.ViewHolder {
        val viewItem = LayoutInflater
            .from(parent.context)
            .inflate(R.layout.manual_attendance_item, parent, false)
        return ViewHolder(viewItem, mListener)
    }

    override fun onBindViewHolder(holder: StudentListAdapter.ViewHolder, position: Int) {
        holder.textView_student.text = studentsList[position].fullName
        if (studentsList[position].frequencyID != null){
            if(studentsList[position].isManual){
                holder.imageView.setImageResource(R.drawable.icon_is_present_foreground)
                holder.imageView_biometry.isVisible = false
            }else if (!studentsList[position].isManual){
                holder.imageView_biometry.isVisible = true
                holder.imageView.setImageResource(R.drawable.icon_is_present_foreground)
            }
        }else{
            holder.imageView.setImageResource(R.drawable.icon_is_not_present_foreground)
            holder.imageView_biometry.isVisible = false
        }

    }

    override fun getItemCount(): Int {
        return studentsList.size
    }


    inner class ViewHolder(itemView: View, listener: onItemClickListener): RecyclerView.ViewHolder(itemView){
        lateinit var imageView: ImageView
        lateinit var imageView_biometry: ImageView
        lateinit var textView_student: TextView

        init {
            textView_student = itemView.findViewById(R.id.textView_student)
            imageView = itemView.findViewById(R.id.imageView_check)
            imageView_biometry = itemView.findViewById(R.id.imageView_biometry)

            itemView.setOnClickListener {
                listener.onItemClick(adapterPosition)
            }
        }
    }
}