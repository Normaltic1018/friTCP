using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Threading;
using System.Windows.Forms;

namespace TCP_Proxy
{
    
    class My_Socket
    {
        TcpClient client;
        NetworkStream ns;
        bool isRunning = true;

        public My_Socket()
        {
            try
            {
                client = new TcpClient("127.0.0.1", 12345);
                ns = client.GetStream();
                //Thread recvThread = new Thread(new ThreadStart(RecvThread));
                //recvThread.Start();
            }
            catch (SocketException)
            {
                MessageBox.Show("서버와의 연결에 실패했습니다.");
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

            while (isRunning)
            {
                try
                {
                    ns.Read(buffer, 0, buffer.Length);
                    msg = Encoding.ASCII.GetString(buffer);
                    //serverMessage.Invoke(new LogToForm(Log), new object[] { msg });
                }
                catch (Exception ex)
                {
                    MessageBox.Show(ex.Message);
                }
            }
        }

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



    }
}
