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
using System.Collections;

namespace TCP_Proxy
{
    public partial class Main : Form
    {        //delegate void SetTextCallback(String text);

        Process pro = null;
        Attach form2 = null;
        Sorting sorter = null;

        Cmd_Socket cmd_sock = null;
        bool cmd_sock_flag = false;
        Proxy_Socket proxy_sock = null;
        bool proxy_sock_flag = false;

        public Main()
        {
            InitializeComponent();

            //sort 관리자 생성
            sorter = new Sorting(listView1);
            

        }


        public void set_text_gui(string msg)
        {
            tabPage5.Text = msg;
        }

        public void python_start(String PID)
        {
            // server Start!
            cmd_sock = new Cmd_Socket(textBox1);
            cmd_sock_flag = true;
            proxy_sock = new Proxy_Socket(listView1);
            proxy_sock_flag = true;

            // client Start soon!
            ProcessStartInfo proinfo = new ProcessStartInfo();
            pro = new Process();

            // process information settings
            proinfo.FileName = @"python3";
            proinfo.CreateNoWindow = true;
            proinfo.UseShellExecute = false;
            proinfo.RedirectStandardOutput = false;
            proinfo.RedirectStandardInput = false;
            proinfo.RedirectStandardError = false;
            //proinfo.Arguments = "C:\\Users\\A0502640\\source\\repos\\TCP_Proxy\\TCP_Proxy\\core\\tcp_proxy.py " + PID;
            proinfo.Arguments = "core\\tcp_proxy.py " + PID;

            // process settings
            pro.StartInfo = proinfo;
            pro.EnableRaisingEvents = false;

            //pro.OutputDataReceived += new DataReceivedEventHandler(p_OutputDataReceived);

            pro.Start();
            //pro.BeginOutputReadLine();

            form2.Close();


        }
        /*
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

 
        */

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

        private void ListView1_ColumnClick(object sender, ColumnClickEventArgs e)
        {
            sorter.sort(e);

        }

        private void TabPage5_Click(object sender, EventArgs e)
        {

        }

        private void TextBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void Button3_Click(object sender, EventArgs e)
        {
            string msg = textBox2.Text;
            cmd_sock.send2(msg);
        }

        private void Main_Closed(object sender, FormClosedEventArgs e)
        {
            // socket close

            if(cmd_sock_flag)
                cmd_sock.thread_control(false);
            if(proxy_sock_flag)
                proxy_sock.thread_control(false);
        }

        private void ListView1_MouseClick(object sender, MouseEventArgs e)
        {
            List<string[]> history_list = proxy_sock.get_history_list();

            ListViewItem item = listView1.SelectedItems[0];
            int idx = Convert.ToInt32(item.SubItems[0].Text);

            string[] history = history_list[idx-1];
            //textBox3.Text = history[0]; // idx
            //textBox3.Text += history[1]; // ip
            //textBox3.Text += history[2]; // port
            //textBox3.Text += history[3]; // hexdump

            string[] hex_list = history[3].Replace(" ","").Replace("\'","").Replace("[","").Replace("]","").Split(',');
            //hexdump example : ['48', '65', '6c', '6c', '6f', '20', '53', '65', '72', '76', '65', '72', '21']

            // initialize
            textBox3.Text = "";

            foreach (string hex in hex_list)
            {
                int value = Convert.ToInt32(hex, 16);
                string stringValue = Char.ConvertFromUtf32(value);
                textBox3.Text += stringValue;
            }
            
    }
    }
}
