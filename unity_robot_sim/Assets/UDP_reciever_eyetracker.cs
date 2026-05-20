using UnityEngine;
using System;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Configuration;
using System.Runtime.CompilerServices;
using UnityEditor;




public class UDP_reciever_eyetracker : MonoBehaviour
{
    private UdpClient udpClient;
    private IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
    public float centerRatio = 0.0f;

    public void UDP_reciever()
    {
        while (true)
        {
            Debug.Log("Thread Innitialize...");
            byte[] messageEncrypted = udpClient.Receive(ref remoteEndPoint);
            Debug.Log("UDP Recieve...");
            string trueMessage = System.Text.Encoding.UTF8.GetString(messageEncrypted);
            //float conversion might be unsafe may need to change
            centerRatio = float.Parse(trueMessage);
        }
    }
    void Start()
    {
        udpClient = new UdpClient(5008);
        Thread t1 = new Thread(UDP_reciever);
        t1.IsBackground = true;
        t1.Start();
    }

    void Update()
    {
        float angle = 90.0f * centerRatio;
        transform.eulerAngles = new Vector3(0.0f, angle, 0.0f);
    }

    void OnDisable()
    {
        if (udpClient != null)
        {
            udpClient.Close();
        }
    }

}
