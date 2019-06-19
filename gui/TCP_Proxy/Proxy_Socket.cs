using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Threading;
using System.Windows.Forms;
using System.Net;
using System.IO;
using Newtonsoft.Json.Linq;

namespace TCP_Proxy
{
    
    class Proxy_Socket
    {
        TcpListener server;
        TcpClient client;
        NetworkStream ns;

        int idx = 1;

        bool isRunning = false;

        public List<string[]> history_list = new List<string[]>();
        ListView history_listview;

        public delegate void send_gui_Delegate(Control ctl, string msg);
        public void send_gui(Control ctl, string json_msg)
        {
            if (ctl.InvokeRequired)
                ctl.Invoke(new send_gui_Delegate(send_gui), ctl, json_msg);
            else
            {
                // json 형태로 수신
                JObject obj = JObject.Parse(json_msg);

                // service 명 parsing
                string service = obj["data"]["service"].ToString();

                if (service.Equals("proxy"))
                {
                    // parsing data
                    string ip = obj["data"]["message"]["IP"].ToString();
                    string port = obj["data"]["message"]["PORT"].ToString();
                    string hexdump = obj["data"]["message"]["hex_dump"].ToString();

                    // 내부 관리용 리스트에 등록
                    string[] tmp_list = { idx.ToString("G"), ip, port, hexdump };
                    history_list.Add(tmp_list);
                    idx = idx + 1;

                    // gui 에 등록
                    ListViewItem tmp_item = new ListViewItem(tmp_list);              
                    history_listview.Items.Add(tmp_item);
                }
                
            }
        }

        public void thread_control(bool flag)
        {
            isRunning = flag;
        }

        public Proxy_Socket(ListView listview)
        {
            try
            {
                history_listview = listview;

                IPAddress ipAd = IPAddress.Parse("127.0.0.1");
                server = new TcpListener(ipAd, 12344);
                Thread handler = new Thread(new ThreadStart(socket_handler));
                handler.Start();

            }
            catch (SocketException)
            {
                MessageBox.Show("서버와의 연결에 실패했습니다.");
            }
        }


        public void socket_handler()
        {
            server.Start();

            client = server.AcceptTcpClient();
            isRunning = true;

            ns = client.GetStream();

            Thread recvThread = new Thread(new ThreadStart(RecvThread));
            recvThread.Start();
        }


        public void send(byte[] data)
        {
            byte[] buffer = new byte[65535];
            buffer = data;
            try
            {
                ns.Write(buffer, 0, buffer.Length);
            }
            catch (SocketException)
            {
                MessageBox.Show("send failed...");
            }
        }

        public void send2(string data)
        {
            string buffer2 = data;
            byte[] buffer = StringToByte(buffer2);

            try
            {
                ns.Write(buffer, 0, buffer.Length);
                ns.Flush();
            }
            catch (SocketException)
            {
                MessageBox.Show("send failed...");
            }
        }

        public string recv()
        {
            byte[] buffer = new byte[65535];
            string msg = "";
            try
            {
                ns.Read(buffer, 0, buffer.Length);
                msg = Encoding.ASCII.GetString(buffer);
            }
            catch (SocketException)
            {
                MessageBox.Show("send failed...");
            }
            return msg;
        }

        public string recv2()
        {
            byte[] buffer = new byte[65535];
            string msg = "";
            try
            {
                ns.Read(buffer, 0, buffer.Length);
                msg = ByteToString(buffer);
            }
            catch (SocketException)
            {
                MessageBox.Show("send failed...");
            }
            return msg;
        }

        
        public void RecvThread()
        {
            byte[] buffer = new byte[65535];
            string msg;
            int byte_read;


            while (isRunning)
            {
                
                try
                {
                    byte_read = 0;
                    byte_read = ns.Read(buffer, 0, buffer.Length);
                    if (byte_read > 0)
                    {
                        ASCIIEncoding encoder = new ASCIIEncoding();
                        msg = encoder.GetString(buffer, 0, byte_read);
                        //msg = Encoding.ASCII.GetString(buffer);

                        send_gui(history_listview, msg);

                        //serverMessage.Invoke(new LogToForm(Log), new object[] { msg });
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);
                }
            }
        }
        /*
        private void Receive() // 클라이언트에게 받기
        {
            string msg = log_console.Text;
            AddTextDelegate AddText = new AddTextDelegate(log_console.AppendText);

            while (isRunning)
            {
                Thread.Sleep(1);

                if (ns.CanRead) // 받아온 데이터가 있다면 출력
                {
                    string tempStr = reader.ReadLine();
                    if (tempStr.Length > 0)
                    {
                        MethodInvoker(AddText, "You : " + tempStr + "\r\n");
                    }
                }
            }
}
*/
            private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            isRunning = false;
            ns.Close();
            client.Close();
        }

        private string ByteToString(byte[] strByte) {
            string str = Encoding.Default.GetString(strByte);
            return str;
        } 

        private byte[] StringToByte(string str) {
            byte[] StrByte = Encoding.UTF8.GetBytes(str);
            return StrByte;
        }

        public List<string[]> get_history_list()
        {
            return history_list;
        }

    }
}
