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
    private float prevRatioY = 0.0f;
    private float prevRatioX = 0.0f;
    private float centerRatioY = 0.0f;
    private float centerRatioX = 0.0f;
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
            centerRatioY = float.Parse(messageArr[0]);
            centerRatioX = float.Parse(messageArr[1]);
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
        //change floats bellow to modify max and min angle
        float prevAngleY = 20.0f * prevRatioY;
        float prevAngleX = 15.0f * prevRatioX;
        float angleY = 20.0f * centerRatioY;
        float angleX = 15.0f * centerRatioX;
        var prevStateY = Quaternion.Euler(0, prevAngleY, 0);
        var prevStateX = Quaternion.Euler(prevAngleX, 0, 0);
        var currStateY = Quaternion.Euler(0, angleY, 0);
        var currStateX = Quaternion.Euler(angleX, 0, 0);
        var prevState = prevStateY * prevStateX;
        var currState = currStateY * currStateX;

        transform.rotation = Quaternion.Slerp(prevState, currState, 0.05f);
        //transform.eulerAngles = new Vector3(0.0f, angle, 0.0f);
        prevRatioY = centerRatioY;
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
