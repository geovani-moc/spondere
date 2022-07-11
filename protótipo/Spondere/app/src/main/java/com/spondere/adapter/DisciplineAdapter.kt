package com.spondere.adapter

import android.content.Context;
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.spondere.R
import com.spondere.entity.Discipline
import com.spondere.entity.Group

class DisciplineAdapter(
    private val context: Context,
    private val disciplines: ArrayList<Discipline>,
    private val groups: ArrayList<Group>):
    RecyclerView.Adapter<DisciplineAdapter.ViewHolder>() {
    private lateinit var mListener: onItemClickListener

    interface onItemClickListener{
        fun onItemClick(position: Int)
    }

    fun setOnItemClickListener(listener: onItemClickListener){
        mListener = listener
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): DisciplineAdapter.ViewHolder {
        val viewItem = LayoutInflater.from(parent.context).inflate(R.layout.discipline_item, parent, false)
        return ViewHolder(viewItem, mListener)
    }

    override fun onBindViewHolder(holder: DisciplineAdapter.ViewHolder, position: Int) {
        holder.textView_Title.text = disciplines[position].name
        holder.textView_Description.text = disciplines[position].description
        holder.textView_GroupCode.text = "Código da turma: "+groups[position].code
    }

    override fun getItemCount(): Int {
        return disciplines.size
    }

    fun updateItens(disciplines: ArrayList<Discipline>, groups: ArrayList<Group>) {
        this.disciplines.clear()
        this.disciplines.addAll(disciplines)
        this.groups.clear()
        this.groups.addAll(groups)
    }

    inner class ViewHolder(itemView:View, listener: onItemClickListener):RecyclerView.ViewHolder(itemView){
        lateinit var textView_Title:TextView
        lateinit var textView_Description:TextView
        lateinit var textView_GroupCode: TextView

        init {
            textView_Title = itemView.findViewById(R.id.textview_disciplineTitle)
            textView_Description = itemView.findViewById(R.id.textview_descriptionDiscipline)
            textView_GroupCode = itemView.findViewById(R.id.textView_groupCode)

            itemView.setOnClickListener {
                listener.onItemClick(adapterPosition)
            }
        }
    }
}