using UnityEngine;
using System;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Configuration;
using System.Runtime.CompilerServices;
using UnityEditor;
using Random = System.Random;

public class tcp_tts : MonoBehaviour
{
    private UdpClient udpClient;
    private IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 5009);

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        udpClient = new UdpClient(5009);

    }

    // Update is called once per frame
    void Update()
    {
        if (udpClient.Available > 0)
        {
            byte[] messageEncrypted = udpClient.Receive(ref remoteEndPoint);
            //Play Message
        }
        
    }
    void OnDisable()
    {
        if (udpClient != null)
        {
            udpClient.Close();
        }
    }
}
