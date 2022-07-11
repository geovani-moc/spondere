package com.spondere.adapter

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.spondere.R
import com.spondere.entity.AcademicClass
import com.spondere.entity.Discipline
import com.spondere.entity.Group

class AcademicClassAdapter(private val context:Context, private val academicClasses: ArrayList<AcademicClass>):
    RecyclerView.Adapter<AcademicClassAdapter.ViewHolder>() {
    private lateinit var listener: onItemClickListener

    interface onItemClickListener{
        fun onItemClick(position: Int)
    }

    fun setOnItemClickListener(listener: onItemClickListener){
        this.listener = listener
    }

    override fun onCreateViewHolder(
        parent: ViewGroup,
        viewType: Int
    ): AcademicClassAdapter.ViewHolder {
        val viewItem = LayoutInflater.from(parent.context).inflate(R.layout.academicclass_item, parent, false)
        return ViewHolder(viewItem, listener)
    }

    override fun onBindViewHolder(holder: AcademicClassAdapter.ViewHolder, position: Int) {
        holder.textView_Title.text = academicClasses[position].titleClass
        holder.textView_Description.text = academicClasses[position].descriptionClass
    }

    override fun getItemCount(): Int {
        return academicClasses.size
    }

    inner class ViewHolder(itemView: View, listener: onItemClickListener):RecyclerView.ViewHolder(itemView){
        lateinit var textView_Title: TextView
        lateinit var textView_Description: TextView

        init {
            textView_Title = itemView.findViewById(R.id.textview_academicClassTitle)
            textView_Description = itemView.findViewById(R.id.textview_academicDescription)

            itemView.setOnClickListener{
                listener.onItemClick(adapterPosition)
            }
        }
    }

    fun updateItens(academicClasses: ArrayList<AcademicClass>) {
        this.academicClasses.clear()
        this.academicClasses.addAll(academicClasses)
    }
}