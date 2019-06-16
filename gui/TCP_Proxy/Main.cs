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
    public partial class Main : Form
    {        //delegate void SetTextCallback(String text);

        Process pro = null;
        Attach form2 = null;
        public Main()
        {
            InitializeComponent();
            test_init2();

            /*
            My_Socket my_sock = new My_Socket();
            my_sock.send2("test");
            MessageBox.Show(my_sock.recv());*/

            //shell_start();
            //get_process_list();

        }

        private void test_init()
        {
            String[] aa = { "1", "2", "3" };
            ListViewItem item = new ListViewItem(aa);
            listView1.Items.Add(item);
        }

        private void test_init2()
        {
            String[] aa = { "1", "2", "3" };
            ListViewItem item = new ListViewItem(aa);
            item.SubItems.Add("aaaa");
            listView1.Items.Add(item);
        }
        public void python_start(String PID)
        {
            ProcessStartInfo proinfo = new ProcessStartInfo();
            pro = new Process();

            // process information settings
            proinfo.FileName = @"python";
            proinfo.CreateNoWindow = true;
            proinfo.UseShellExecute = false;
            proinfo.RedirectStandardOutput = true;
            proinfo.RedirectStandardInput = true;
            proinfo.RedirectStandardError = true;
            proinfo.Arguments = "tcp_proxy.py " + PID;


            // process settings
            pro.StartInfo = proinfo;
            pro.EnableRaisingEvents = false;

            //pro.OutputDataReceived += new DataReceivedEventHandler(p_OutputDataReceived);

            pro.Start();
            pro.BeginOutputReadLine();

            form2.Close();
        }

        public void p_OutputDataReceived(object sender, DataReceivedEventArgs e)
        {
            String line = e.Data;
            //SetText(line);

            if (line.Contains("------------"))
            {
                pro.OutputDataReceived += new DataReceivedEventHandler(get_mlist);
                pro.OutputDataReceived -= p_OutputDataReceived;
                pro.StandardInput.Write("mlist" + Environment.NewLine);
            }
        }
        public void get_mlist(object sender, DataReceivedEventArgs e)
        {
        }

            private void Main_Load(object sender, EventArgs e)
        {

        }

        private void TEST2ToolStripMenuItem1_Click(object sender, EventArgs e)
        {
            form2 = new Attach();
            form2.sendPID += new Attach.sendPID_Delegate(python_start);
            form2.Show();
        }

        private void ListView1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        private void Button1_Click(object sender, EventArgs e)
        {

        }
    }
}
