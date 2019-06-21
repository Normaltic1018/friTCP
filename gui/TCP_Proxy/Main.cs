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
using System.Windows.Forms.VisualStyles;
using System.ComponentModel.Design;

namespace TCP_Proxy
{
    public partial class Main : Form
    {        //delegate void SetTextCallback(String text);

        
        Attach form2 = null;
        Sorting sorter = null;

        Cmd_Socket cmd_sock = null;
        Proxy_Socket proxy_sock = null;
        Process pro = null;
        bool pro_flag = false;

        TextBox[] hex_list = null;
        TextBox[] string_list = null;

        

        public Main()
        {
            InitializeComponent();

            //init_screen();
            //sort 관리자 생성
            sorter = new Sorting(listView1);

            // process exit event => clean all!
            // AppDomain.CurrentDomain.ProcessExit += ProcessExitHanlder;
        }

        private void ProcessExitHanlder(object sender, EventArgs e)
        {
            MessageBox.Show("process killed...");

            if (pro_flag)
            {
                pro.Kill();
            }
        }


    

        public void init_screen()
        {
            this.StartPosition = FormStartPosition.Manual;

            Rectangle fullScrenn_bounds = Rectangle.Empty;

            foreach (var screen in Screen.AllScreens)
            {
                fullScrenn_bounds = Rectangle.Union(fullScrenn_bounds, screen.Bounds);
            }
            this.ClientSize = new Size(fullScrenn_bounds.Width, fullScrenn_bounds.Height);
            this.Location = new Point(fullScrenn_bounds.Left, fullScrenn_bounds.Top);

        }

        public void set_text_gui(string msg)
        {
            tabPage5.Text = msg;
        }

        public void python_start(String PID)
        {
            // server Start!
            cmd_sock = new Cmd_Socket(textBox1);
            proxy_sock = new Proxy_Socket(listView1);

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
            pro_flag = true;
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

        private void Create_HexEditor_Contents(string[] hexdump_list, int line_limits)
        {
            int counts = hexdump_list.Length;
            hex_list = new TextBox[counts];
            string_list = new TextBox[counts];


            int column_index = 0;
            int row_index = 0;
            for (int i = 0; i < hexdump_list.Length; i++)
            {
                if (column_index == line_limits)
                {
                    column_index = 0;
                    row_index += 1;
                }


                hex_list[i] = new TextBox();
                hex_list[i].Location = new Point(11 + (22 * column_index), 5 + (22 * row_index + 1));
                hex_list[i].Size = new Size(18, 25);
                hex_list[i].Text = hexdump_list[i];
                hex_list[i].BorderStyle = System.Windows.Forms.BorderStyle.None;
                hex_list[i].KeyPress += hexbox_keypress_event;
                panel1.Controls.Add(hex_list[i]);

                string_list[i] = new TextBox();
                string_list[i].Location = new Point(5 + (14 * column_index), 5 + (22 * row_index + 1));
                string_list[i].Size = new Size(13, 25);
                string_list[i].Text = Byte_To_Ascii(hexdump_list[i]);
                string_list[i].BorderStyle = System.Windows.Forms.BorderStyle.None;
                string_list[i].KeyPress += stringbox_keypress_event;
                panel3.Controls.Add(string_list[i]);

                column_index += 1;

            }

            Label[] offset_list = new Label[row_index + 1];

            // OFFSET 찍기
            for (int i = 0; i < row_index + 1; i++)
            {
                offset_list[i] = new Label();
                offset_list[i].Location = new Point(5, 4 + (22 * i));
                offset_list[i].Text = (line_limits + (16 * i)).ToString("X8");
                offset_list[i].BorderStyle = System.Windows.Forms.BorderStyle.None;
                offset_list[i].ForeColor = System.Drawing.Color.DarkBlue;
                offset_list[i].Font = new System.Drawing.Font("맑은 고딕", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
                //offset_list[i].ReadOnly = true;
                offset_list[i].BackColor = System.Drawing.SystemColors.Window;
                //offset_list[i].Size = new Size(25, 300);
                panel2.Controls.Add(offset_list[i]);
            }

        }

        private void Create_StringEditor(string[] hexdump_list)
        {
            foreach (string hex in hexdump_list)
            {
                int value = Convert.ToInt32(hex, 16);
                string stringValue = Char.ConvertFromUtf32(value);
                textBox3.Text += stringValue;
            }
        }

        private void Create_HexEditor_Title(int line_limits)
        {
            Label offset_title = new Label();
            offset_title.Location = new Point(14, 5);
            offset_title.Text = "Offset";
            offset_title.BorderStyle = System.Windows.Forms.BorderStyle.None;
            offset_title.ForeColor = System.Drawing.Color.DarkBlue;
            offset_title.Font = new System.Drawing.Font("맑은 고딕", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));
            //offset_title.ReadOnly = true;
            offset_title.BackColor = System.Drawing.SystemColors.Window;
            //offset_title.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            //offset_title.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            //offset_list[i].Size = new Size(25, 300);
            panel4.Controls.Add(offset_title);

            string[] hexa = new string[] { "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0A", "0B", "0C", "0D", "0E", "0F" };
            for (int i = 0; i < line_limits; i++)
            {
                Label tmp_textbox = new Label();
                tmp_textbox.Location = new Point(9 + (22 * i), 5);
                tmp_textbox.Size = new Size(23, 25);
                tmp_textbox.Text = hexa[i];
                tmp_textbox.BorderStyle = System.Windows.Forms.BorderStyle.None;
                tmp_textbox.ForeColor = System.Drawing.Color.DarkBlue;
                //tmp_textbox.ReadOnly = true;
                tmp_textbox.BackColor = System.Drawing.SystemColors.Window;
                tmp_textbox.Font = new System.Drawing.Font("맑은 고딕", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(129)));

                panel5.Controls.Add(tmp_textbox);
            }

        }
        private void Create_HexEditor(string[] hexdump_list, int line_limits)
        {
            Create_HexEditor_Title(16);
            Create_HexEditor_Contents(hexdump_list, 16);
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

            string[] hexdump_list = history[3].Replace(" ", "").Replace("\'", "").Replace("[", "").Replace("]", "").Split(',');
            //hexdump example : ['48', '65', '6c', '6c', '6f', '20', '53', '65', '72', '76', '65', '72', '21']

            
            // initialize request textbox
            textBox3.Text = "";

            // initialize response textbox
            textBox4.Text = "";
            textBox6.Text = "";

            
            Create_StringEditor(hexdump_list);
            Create_HexEditor(hexdump_list, 16);


            //byteviewer는 viewer기능밖에 없음..
            /*
            ByteViewer bv = new ByteViewer();
            byte[] test11 = { 0x01, 0x02, 0x03, 0x04};
            bv.SetBytes(test11);
            
            //bv.SetFile(@"c:\windows\notepad.exe"); // or SetBytes
            textBox4.Controls.Add(bv);*/

        }

        public string Byte_To_Ascii(string my_byte)
        {
            int value = Convert.ToInt32(my_byte, 16);
            string stringValue = Char.ConvertFromUtf32(value);
            return stringValue;
        }

        public string Ascii_To_Byte(string ascii)
        {
            StringBuilder hexNumbers = new StringBuilder();
            byte[] byteArray = ASCIIEncoding.ASCII.GetBytes(ascii);
            return byteArray[0].ToString("x");
        }
        public void Refresh_HexBox(int i)
        {
            hex_list[i].Text = Ascii_To_Byte(string_list[i].Text);
        }

        public void Refresh_StringBox(int i)
        {
            string_list[i].Text = Byte_To_Ascii(hex_list[i].Text);
        }

        public void stringbox_keypress_event(object sender, KeyPressEventArgs e)
        {
            for (int i = 0; i < string_list.Length; i++)
            {
                if (string_list[i].Equals(sender))
                {
                    int idx = string_list[i].SelectionStart; // 현재 textbox의 커서 인덱스 값

                    string tmp_text = string_list[i].Text;
                    System.Diagnostics.Debug.WriteLine("tmp_text: " + tmp_text);


                    string old_text = tmp_text;

                    StringBuilder strbuilder1 = new StringBuilder();
                    for (int j = 0; j < string_list[j].Text.Length; j++)
                    {
                        if (idx != j)
                            strbuilder1.Append(tmp_text[j]);
                        else
                            strbuilder1.Append(e.KeyChar);

                    }
                    string new_text = strbuilder1.ToString();

                    string_list[i].Text = new_text;
                    

                    // hex 값 변경 시 string 변경 수행
                    Refresh_HexBox(i);
                }
            }
            e.Handled = true; // default eventhandler 사용안함!
        }

        public void hexbox_keypress_event(object sender, KeyPressEventArgs e)
        {
            for(int i=0; i<hex_list.Length; i++)
            {
                if (hex_list[i].Equals(sender))
                {
                    int idx = hex_list[i].SelectionStart; // 현재 textbox의 커서 인덱스 값

                    string tmp_text = hex_list[i].Text;
                    System.Diagnostics.Debug.WriteLine("tmp_text: " + tmp_text);


                    string old_text = tmp_text;

                    StringBuilder strbuilder1 = new StringBuilder();
                    for (int j = 0; j < hex_list[j].Text.Length; j++)
                    {
                        if (idx != j)
                            strbuilder1.Append(tmp_text[j]);
                        else
                            strbuilder1.Append(e.KeyChar);

                    }
                    string new_text = strbuilder1.ToString().ToUpper();

                    if (hex_input_validation_check(new_text))
                    {
                        hex_list[i].Text = new_text;
                    }

                    else
                    {
                        hex_list[i].Text = old_text;
                    }

                    // hex 값 변경 시 string 변경 수행
                    Refresh_StringBox(i);
                }
            }
            e.Handled = true; // default eventhandler 사용안함!
        }


        private void TextBox4_TextChanged(object sender, EventArgs e)
        {
            
        }

        private void alksdjflkadsjf(object sender, KeyEventArgs e)
        {

        }

        private void asdsad(object sender, KeyPressEventArgs e)
        {

        }

        private bool hex_input_validation_check(string str)
        {
            char[] validation_list = { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F' };
            bool result = false;
            foreach(char tmp_str in str.ToUpper())
            {
                result = false;
                foreach(char chr in validation_list)
                {
                    if(chr.Equals(tmp_str))
                    {
                        result = true;
                    }
                }
                if (!result)
                    return false;
            }
            return true;
        }

    }
}
