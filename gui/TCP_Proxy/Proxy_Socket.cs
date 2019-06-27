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
        public TcpListener server;
        TcpClient client;
        NetworkStream ns;

        int idx = 1;

        bool isRunning = false;

        public List<string[]> history_list = new List<string[]>();
        ListView history_listview;



        public delegate void proxy_data_handler_Delegate(Control ctl, string msg);
        public void proxy_data_handler(Control ctl, string json_msg)
        {
            if (ctl.InvokeRequired)
                ctl.Invoke(new proxy_data_handler_Delegate(proxy_data_handler), ctl, json_msg);
            else
            {
                // json 형태로 수신
                JObject obj = JObject.Parse(json_msg);
                

                // service 명 parsing
                string service = obj["data"]["service"].ToString();

                if (service.Equals("proxy")) // add and display history_view to gui
                {
                    // parsing data
                    string intercept_mode = obj["data"]["message"]["INTERCEPT"].ToString();

                    // 구현하고자 하는 명세
                    /////////////////////////////////////////////////////////////////////////////////////
                    // read하고, intercept 모드를 파싱하기 전까지 intercept 버튼이 클릭되어서는 안된다.
                    // 클릭된다면 꼬이게 됨.
                    // 예:) intercept on를 read함. 실제 해당 패킷이 intercept on 이라는 것을 확인하는 절차중에 intercept 버튼을 클릭해서 off 가 된다면
                    // intercept off 패킷을 read한 것으로 착각함.
                    // 그래서 send 버튼이 활성화 되지 않음. 이럴 경우 멈춘 상황에서 gui상 send를 보내지 못하는 상황이 발생
                    // 따라서 read_data -> intercept 모드 파싱 사이에서는 intercept 버튼을 비활성화 시켜준다.

                    string ip = obj["data"]["message"]["IP"].ToString();
                    string port = obj["data"]["message"]["PORT"].ToString();
                    string hexdump = obj["data"]["message"]["hex_dump"].ToString().Replace(" ", "").Replace("\'", "").Replace("[", "").Replace("]", "").Replace(","," ");
                    //hexdump example : ['48', '65', '6c', '6c', '6f', '20', '53', '65', '72', '76', '65', '72', '21']
                    // => "48 65 6c 6c 6f 20 53 65 72 76 65 72 21"

                    string complete = "N"; //처리되었는지 여부 변수

                    // 내부 관리용 리스트에 등록
                    string[] tmp_list = { idx.ToString("G"), ip, port, hexdump, intercept_mode, complete };
                    history_list.Add(tmp_list);
                    idx = idx + 1;

                    // gui 에 등록
                    ListViewItem tmp_item = new ListViewItem(tmp_list);              
                    history_listview.Items.Add(tmp_item);

                    
                }
                
            }
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

        public void Close()
        {
            isRunning = false; // 중요!! 안해주면 networkstream error 발생. RecvThread 종료 키워드

            if (server != null)
                server.Server.Close();
            
            if(client != null)
                client.Close();
        }

        public void socket_handler()
        {
            server.Server.ReceiveTimeout = 3000;
            server.Server.SendTimeout = 3000;
            server.Start();

            try
            {
                client = server.AcceptTcpClient();
                // linger 옵션 -> true,0 -> 버퍼에 있는 데이터를 버리고 소켓을 바로 닫아버려라.
                // 버퍼에 데이터가 남아있는 상태로 연결 종료 시 버퍼 데이터를 다시 전송하기 위해 Block 상태가 되버림.
                // 따라서 데이터를 버리고 block 해제를 위함
                //LingerOption lingerOption = new LingerOption(true, 0);
                //client.LingerState = lingerOption;
                //

                isRunning = true;

                ns = client.GetStream();

                Thread recvThread = new Thread(new ThreadStart(RecvThread));
                recvThread.Start();
            }
            catch(SocketException e)
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


            while (isRunning)
            {
                
                try
                {
                    if (ns.DataAvailable)
                    {
                        byte_read = 0;
                        byte_read = ns.Read(buffer, 0, buffer.Length);
                        if (byte_read > 0)
                        {
                            ASCIIEncoding encoder = new ASCIIEncoding();
                            msg = encoder.GetString(buffer, 0, byte_read);
                            //msg = Encoding.ASCII.GetString(buffer);

                            proxy_data_handler(history_listview, msg);

                            //serverMessage.Invoke(new LogToForm(Log), new object[] { msg });
                        }

                        else
                        {
                            MessageBox.Show("Proxy_Socket: Data 0 recv");
                        }
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
