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
using System.Data.SqlClient;
using System.Net.Sockets;
using System.Threading;

namespace TCP_Proxy
{
    public partial class Main : Form
    {        //delegate void SetTextCallback(String text);

        
        Attach form2 = null;
        Sorting sorter = null;

        Cmd_Socket cmd_sock = null;
        Proxy_Socket proxy_sock = null;
        bool kill_flag = false;

        Process pro = null;

        TextBox[] hex_list = null;
        TextBox[] string_list = null;

        int line_limits = 16;

        bool attach_flag = false;

        public Main()
        {
            InitializeComponent();

            //init_screen();
            //sort 관리자 생성
            sorter = new Sorting(listView1);

            // hexeditor title 세팅
            Create_HexEditor_Title(16);

            // process exit event => clean all!
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.ProcessExitHanlder);
            AppDomain.CurrentDomain.ProcessExit += ProcessExitHanlder;
        }

        private void clear_all()
        {
            if (pro!=null)
            {
                if(!pro.HasExited)
                    pro.Kill();
            }

            if (proxy_sock != null)
                proxy_sock.Close();
            if(cmd_sock != null)
                cmd_sock.Close();
            
        }

        private void ProcessExitHanlder(object sender, EventArgs e)
        {
            kill_flag = true;
            clear_all();
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

        private void pro_alive_check()
        {
            while(!pro.HasExited)
            {
                
            }

            if(!kill_flag)
                MessageBox.Show("[Core Process Killed]: 코어 프로세스가 비정상적으로 종료되었습니다.");
            clear_all();
        }
        public void python_start(String PID)
        {
            

            form2.Close();

            // server Start!
            cmd_sock = new Cmd_Socket(textBox1);
            proxy_sock = new Proxy_Socket(listView1);

            // client Start soon!
            ProcessStartInfo proinfo = new ProcessStartInfo();
            pro = new Process();

            // process information settings
            proinfo.FileName = @"python";
            proinfo.CreateNoWindow = true;
            proinfo.UseShellExecute = false;
            proinfo.RedirectStandardOutput = true;
            proinfo.RedirectStandardInput = false;
            proinfo.RedirectStandardError = true;
            //proinfo.Arguments = "C:\\Users\\A0502640\\source\\repos\\TCP_Proxy\\TCP_Proxy\\core\\tcp_proxy.py " + PID;
            proinfo.Arguments = "core\\tcp_proxy.py " + PID;

            // process settings
            pro.StartInfo = proinfo;
            //pro.EnableRaisingEvents = false;

            //pro.OutputDataReceived += new DataReceivedEventHandler(p_OutputDataReceived);
            try
            {
                // python 없으면 예외발생
                
                pro.Start();
                

                // python 은 있으나 tcp_proxy.py 파일이 없으면 예외발생이 되지 않음.
                // 알아낼 방법?
                // 1. tcp_proxy.py(client) 가 proxy_server(server)에 10초이내에 연결되지 않으면
                // 2. tcp_proxy.py(client) 가 error pipe로 에러메시지 전달하면
                // 3. process가 유효한지 일정시간 기다려보기

                // 3번 구현

                // 1초 기다린 후 python 이 종료되면 core가 정상적으로 실행되지 않음을 알 수 있다.
                // 정상적으로 실행되지 않는경우
                // 1. core파일 자체의 에러
                // 2. core파일 위치를 찾을 수 없음
                // 3. pid 실수


                Thread.Sleep(1000);

                bool result = pro.HasExited;
                if (result)
                {
                    string txt = pro.StandardError.ReadToEnd();
                    MessageBox.Show("[core not started]: "+txt);
                    clear_all();
                }

                else
                {
                    Thread pro_alive_checker = new Thread(new ThreadStart(pro_alive_check));
                    pro_alive_checker.Start();
                }

            }
            catch (Exception e)
            {
                //string txt = pro.StandardError.ReadToEnd();
                MessageBox.Show("[python not founded]: "+e.Message.ToString());
                clear_all();
            }






            //pro.BeginOutputReadLine();




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

        private void Create_HexEditor(string[] hexdump_list, int line_limits)
        {
            /*
            foreach (Control c in panel2.Controls)
            {
                if(c.Name.Equals("offset_panel"))
                {
                    panel2.Controls.Clear;
                }
            }*/



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
                //tmp_panel1.Controls.Add(hex_list[i]);

                string_list[i] = new TextBox();
                string_list[i].Location = new Point(5 + (14 * column_index), 5 + (22 * row_index + 1));
                string_list[i].Size = new Size(13, 25);
                string_list[i].Text = Byte_To_Ascii(hexdump_list[i]);
                string_list[i].BorderStyle = System.Windows.Forms.BorderStyle.None;
                string_list[i].KeyPress += stringbox_keypress_event;
                //tmp_panel2.Controls.Add(string_list[i]);

                column_index += 1;

            }

            
            Panel tmp_panel1 = new Panel();
            tmp_panel1.Size = new System.Drawing.Size(366, 385);
            
            Panel tmp_panel2 = new Panel();
            

            for (int i = 0; i < hexdump_list.Length; i++)
            {
                tmp_panel1.Controls.Add(hex_list[i]);
                tmp_panel2.Controls.Add(string_list[i]);
            }

            panel1.Controls.Clear();
            panel1.Controls.Add(tmp_panel1);
            panel3.Controls.Clear();
            panel3.Controls.Add(tmp_panel2);

            Label[] offset_list = new Label[row_index + 1];

            panel2.Controls.Clear();
            Panel tmp_panel3 = new Panel();
            panel2.Controls.Add(tmp_panel3);
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
                tmp_panel3.Controls.Add(offset_list[i]);
            }

        }

        /*
        private void Create_StringEditor(string[] hexdump_list)
        {
            for (int i = 0; i < hexdump_list.Length; i++)
            {
                int value = Convert.ToInt32(hexdump_list[i], 16);
                string stringValue = Char.ConvertFromUtf32(value);
                textBox3.Text += stringValue;
            }
        }*/
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

            //string[] tmp_list = { idx.ToString("G"), ip, port, hexdump, intercept_mode, complete };
            string intercept_mode = history[4];
            string complete = history[5];

            if (intercept_mode.Equals("on") && complete.Equals("N"))
            {
                button2.Enabled = true;
            }
            else
            {
                button2.Enabled = false;
            }

            string hexdump = history[3];
            string[] hexdump_list = hexdump.Split(' ');

            //hexdump example : "48 65 6c 6c 6f 20 53 65 72 76 65 72 21"



            
            
            Create_HexEditor(hexdump_list, line_limits);
            //Create_StringEditor(hexdump_list);


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
            System.Diagnostics.Debug.WriteLine("Byte_To_Ascii input: " + my_byte);
            System.Diagnostics.Debug.WriteLine("Byte_To_Ascii output: " + stringValue);
            return stringValue;
        }

        public string Ascii_To_Byte(string ascii)
        {
            StringBuilder hexNumbers = new StringBuilder();
            byte[] byteArray = ASCIIEncoding.ASCII.GetBytes(ascii);
            string hex_value = byteArray[0].ToString("x").PadLeft(2,'0');
            System.Diagnostics.Debug.WriteLine("Ascii_To_Byte input: " + ascii);
            System.Diagnostics.Debug.WriteLine("Ascii_To_Byte output: " + hex_value);
            return hex_value;
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
                    System.Diagnostics.Debug.WriteLine("stringbox 기존 문자열: " + tmp_text);


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
                    System.Diagnostics.Debug.WriteLine("stringbox 새 문자열: " + new_text);

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

        private void intercept_button_clicked(object sender, EventArgs e)
        {
            if (attach_flag)
            {
                if (button1.Text.Equals("intercept on"))
                {
                    cmd_sock.send2("set intercept on");
                    button1.Text = "intercept off";
                }
                else
                {
                    cmd_sock.send2("set intercept off");
                    button1.Text = "intercept on";
                }
            }
        }

        private void Button2_Click(object sender, EventArgs e)
        {
            StringBuilder modified_hexdump_strbuilder = new StringBuilder();
            foreach(TextBox tbox in hex_list)
            {
                modified_hexdump_strbuilder.Append(tbox.Text+" ");
                
            }
            string modified_hexdump = modified_hexdump_strbuilder.ToString().Substring(0, modified_hexdump_strbuilder.Length - 1);

            System.Diagnostics.Debug.WriteLine("strbuilder " + modified_hexdump);
            proxy_sock.send2(modified_hexdump);

            //

            List<string[]> history_list = proxy_sock.get_history_list();

            ListViewItem item = listView1.SelectedItems[0];
            int idx = Convert.ToInt32(item.SubItems[0].Text);

            string[] history = history_list[idx - 1];
            //history[0]; // idx
            //history[1]; // ip
            //history[2]; // port
            //history[3]; // hexdump
            //history[4]; // intercept_mode
            //history[5]; // complete

            history[3] = modified_hexdump;
            history[5] = "Y";

            button2.Enabled = false;
        }
        private bool check_intercept_mode()
        {
            if(button1.Text.Equals("intercept off"))
            {
                return true;
            }
            else
                return false;
        }


        /*
        private static void NetErrorDataHandler(object sendingProcess,
            DataReceivedEventArgs errLine)
        {
            // Write the error text to the file if there is something
            // to write and an error file has been specified.

            if (!String.IsNullOrEmpty(errLine.Data))
            {
                if (!errorsWritten)
                {
                    if (streamError == null)
                    {
                        // Open the file.
                        try
                        {
                            streamError = new StreamWriter(netErrorFile, true);
                        }
                        catch (Exception e)
                        {
                            Console.WriteLine("Could not open error file!");
                            Console.WriteLine(e.Message.ToString());
                        }
                    }

                    if (streamError != null)
                    {
                        // Write a header to the file if this is the first
                        // call to the error output handler.
                        streamError.WriteLine();
                        streamError.WriteLine(DateTime.Now.ToString());
                        streamError.WriteLine("Net View error output:");
                    }
                    errorsWritten = true;
                }

                if (streamError != null)
                {
                    // Write redirected errors to the file.
                    streamError.WriteLine(errLine.Data);
                    streamError.Flush();
                }
            }
        }*/
    }

}
