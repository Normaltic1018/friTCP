using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TCP_Proxy
{
    class Sorting
    {
        ArrayList origin_column_arraylist = new ArrayList();  // sort 에 이용할 원본 column list
        string[] origin_column_arraylist_string = null;
        ListView listView = null;

        public Sorting(ListView listView1)
        {
            listView = listView1;
            _initialize();

        }

        // 원본 column name list 받아오기
        private void _initialize()
        {
            for (int idx = 0; idx < listView.Columns.Count; idx++)
            {
                origin_column_arraylist.Add(listView.Columns[idx].Text);
            }
            origin_column_arraylist_string = (string[])origin_column_arraylist.ToArray(typeof(string));
        }

        public void sort(ColumnClickEventArgs e)
        {
            /*
                if (e.Column == 0)
                {
                    return;
                }*/

            // column name initialize
            for (int idx = 0; idx < origin_column_arraylist.Count; idx++)
            {
                listView.Columns[idx].Text = origin_column_arraylist_string[idx];
            }

            listView.Columns[e.Column].Text = listView.Columns[e.Column].Text.Replace(" ▼", "");
            listView.Columns[e.Column].Text = listView.Columns[e.Column].Text.Replace(" ▲", "");


            if (this.listView.Sorting == SortOrder.Ascending || listView.Sorting == SortOrder.None)
            {
                listView.ListViewItemSorter = new ListviewItemComparer(e.Column, "desc");
                listView.Sorting = SortOrder.Descending;

                listView.Columns[e.Column].Text = listView.Columns[e.Column].Text + " ▼";
            }
            else
            {
                listView.ListViewItemSorter = new ListviewItemComparer(e.Column, "asc");
                listView.Sorting = SortOrder.Ascending;
                listView.Columns[e.Column].Text = listView.Columns[e.Column].Text + " ▲";
            }

            listView.Sort();
        }
    }


    class ListviewItemComparer : IComparer
    {
        private int col;
        public string sort = "asc";
        public ListviewItemComparer()
        {
            col = 0;
        }

        public ListviewItemComparer(int column, string sort)
        {
            col = column;
            this.sort = sort;
        }

        public int Compare(object x, object y)
        {
            if (sort == "asc")
            {
                return String.Compare(((ListViewItem)x).SubItems[col].Text, ((ListViewItem)y).SubItems[col].Text);
            }
            else
            {
                return String.Compare(((ListViewItem)y).SubItems[col].Text, ((ListViewItem)x).SubItems[col].Text);
            }
        }
    }
}
