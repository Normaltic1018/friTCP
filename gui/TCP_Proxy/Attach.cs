using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;

namespace TCP_Proxy
{
    public partial class Attach : Form
    {
        public delegate void sendPID_Delegate(String PID);
        public event sendPID_Delegate sendPID;
        public Attach()
        {
            InitializeComponent();
            get_process_list();
        }

        public void get_process_list()
        {
            Process[] processlist = Process.GetProcesses();

            foreach (Process theprocess in processlist)
            {
                listBox1.Items.Add(theprocess.ProcessName + " [" + theprocess.Id + "]");
            }
        }


        private void ListBox1_MouseDoubleClick_1(object sender, MouseEventArgs e)
        {
            sendPID(listBox1.SelectedItem.ToString().Split('[')[1].Split(']')[0]);
        }
    }
}