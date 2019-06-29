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
    
    class Cmd_Socket
    {
        TcpListener server;
        TcpClient client;
        NetworkStream ns;

        public bool isRunning = false;
        Thread recvThread;

        TextBox log_console;


        public delegate void send_gui_Delegate(Control ctl, string msg);
        public void send_gui(Control ctl, string msg)
        {
            if (ctl.InvokeRequired)
                ctl.Invoke(new send_gui_Delegate(send_gui), ctl, msg);
            else
            {
                try
                {

                    // json 형태로 수신
                    JObject obj = JObject.Parse(msg);
                    string type = obj["type"].ToString();
                    string process = obj["data"]["process"].ToString();
                    string res = obj["data"]["res"].ToString();

                    string draw_text = "";

                    if(type.Equals("init_process"))
                    {
                        if (process.Equals("core_boot"))
                        {
                            if (res.Equals("success"))
                            {
                                draw_text = "init success~";//OK!
                            }
                            else
                            {
                                string err = obj["data"]["err"].ToString();
                                MessageBox.Show(err);
                                Main.clear_all();
                            }
                        }
                    }

                    else if(type.Equals("cmd"))
                    {
                        if(process.Equals("get_setting"))
                        {
                            if(res.Equals("success"))
                            {
                                string res_data = obj["data"]["res_data"].ToString();
                                draw_text = "get_setting success~";
                                draw_text += res_data;
                            }
                            else
                            {
                                string err = obj["data"]["err"].ToString();
                                MessageBox.Show(err);
                                Main.clear_all();
                            }
                        }
                    }


                    ctl.Text += draw_text;
                }
                catch (Exception e)
                {
                    MessageBox.Show(e.ToString());
                }
            }

        }


        public void Close()
        {
            isRunning = false; // 중요!! 안해주면 networkstream error 발생. RecvThread 종료 키워드
            //recvThread.Abort();

            if (server != null)
                server.Server.Close();

            if (client != null)
                client.Close();

        }
        public Cmd_Socket(TextBox textbox)
        {
            try
            {
                log_console = textbox;

                IPAddress ipAd = IPAddress.Parse("127.0.0.1");
                server = new TcpListener(ipAd, 12345);
                Thread handler = new Thread(new ThreadStart(socket_handler));
                handler.Start();

            }
            catch (SocketException)
            {
                // python 없을 시 에러 발생
                //MessageBox.Show("서버와의 연결에 실패했습니다.");
            }
        }


        public void socket_handler()
        {
            //server.Server.ReceiveTimeout = 3000;
            //server.Server.SendTimeout = 3000;
            server.Start();

            try
            {


                client = server.AcceptTcpClient();
                // linger 옵션 -> true,0 -> 버퍼에 있는 데이터를 버리고 소켓을 바로 닫아버려라.
                // 버퍼에 데이터가 남아있는 상태로 연결 종료 시 버퍼 데이터를 다시 전송하기 위해 Block 상태가 되버림.
                // 따라서 데이터를 버리고 block 해제를 위함
                LingerOption lingerOption = new LingerOption(true, 0);
                client.LingerState = lingerOption;
                //

                // 소켓이 붙었다 -> 프로그램이 정상적으로 실행되었다.
                isRunning = true;

                ns = client.GetStream();

                recvThread = new Thread(new ThreadStart(RecvThread));
                recvThread.Start();
            }
            catch(Exception e)
            {
                // 클라이언트가 정상적으로 실행되지 않았을 시에 에러 발생
                // 에러발생조건
                // 1. python 명령어 찾을 수 없음
                // 2. core 파일을 찾을 수 없음
                //MessageBox.Show(e.ToString());
            }
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


            while (true)
            {
                
                try
                {
                    //if (ns.DataAvailable)
                    //{
                        byte_read = ns.Read(buffer, 0, buffer.Length);
                        if (byte_read > 0)
                        {
                            ASCIIEncoding encoder = new ASCIIEncoding();
                            msg = encoder.GetString(buffer, 0, byte_read);
                        //msg = Encoding.ASCII.GetString(buffer);
                        System.Diagnostics.Debug.WriteLine("$$recv: "+ msg);
                        send_gui(log_console, msg);

                            //serverMessage.Invoke(new LogToForm(Log), new object[] { msg });
                        }

                        else
                        {
                            MessageBox.Show("Cmd_Socket: Data 0 recv");
                        }
                    //}
                }
                catch (Exception e)
                {
                    System.Diagnostics.Debug.WriteLine("Cmd_Socket recvThread: " + e.ToString());
                    /*
                    if (e.ErrorCode == 10035)
                    {
                        System.Diagnostics.Debug.WriteLine("socket error 10035: " + e.ToString());
                    }*/
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
        private string ByteToString(byte[] strByte) {
            string str = Encoding.Default.GetString(strByte);
            return str;
        } 

        private byte[] StringToByte(string str) {
            byte[] StrByte = Encoding.UTF8.GetBytes(str);
            return StrByte;
        }



    }
}
