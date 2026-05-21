using UnityEngine;
using System;
using System.Threading;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Configuration;
using System.Runtime.CompilerServices;
using UnityEditor;

public class UDP_mp_tracker : MonoBehaviour
{
    private UdpClient udpClient;
    private IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);
    private float prevRatioX = 0.0f;
    private float prevRatioY = 0.0f;
    private float centerRatioX = 0.0f;
    private float centerRatioY = 0.0f;
    public void UDP_reciever()
    {
        while (true)
        {
            Debug.Log("Thread Innitialize...");
            byte[] messageEncrypted = udpClient.Receive(ref remoteEndPoint);
            Debug.Log("UDP Recieve...");
            string messageString = System.Text.Encoding.UTF8.GetString(messageEncrypted);
            //float conversion might be unsafe may need to change
            string[] messageArr = messageString.Split(',');
            centerRatioX = float.Parse(messageArr[0]);
            centerRatioY = float.Parse(messageArr[1]);
        }
    }

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        udpClient = new UdpClient(5008);
        Thread t1 = new Thread(UDP_reciever);
        t1.IsBackground = true;
        t1.Start();
    }

    // Update is called once per frame
    void Update()
    {
        float prevAngle = 90.0f * prevRatioX;
        float angle = 90.0f * centerRatioX;
        var prevState = Quaternion.Euler(0, prevAngle, 0);
        var currState = Quaternion.Euler(0, angle, 0);

        transform.rotation = Quaternion.Slerp(prevState, currState, 0.05f);
        //transform.eulerAngles = new Vector3(0.0f, angle, 0.0f);
        prevRatioX = centerRatioX;
    }
    void OnDisable()
    {
        if (udpClient != null)
        {
            udpClient.Close();
        }
    }

}
