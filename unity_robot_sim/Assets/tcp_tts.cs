using System;
using System.Collections;
using System.IO;
using System.Net;
using System.Net.Sockets;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;




public class tcp_tts : MonoBehaviour
{
    private UdpClient udpClient;
    private IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 5009);
    private string fileUri;
    private AudioSource cubeAudioSource;

    IEnumerator playAudio()
    {
        byte[] messageEncrypted = udpClient.Receive(ref remoteEndPoint);
        //Get Unity Audioclip
        UnityWebRequest webRequest = UnityWebRequestMultimedia.GetAudioClip(fileUri, AudioType.WAV);
        yield return webRequest.SendWebRequest();
        AudioClip cubeClip = DownloadHandlerAudioClip.GetContent(webRequest);
        cubeAudioSource.clip = cubeClip;
        cubeAudioSource.Play();
    }


    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        udpClient = new UdpClient(5009);
        var filePath = Directory.GetParent(Application.dataPath).Parent;
        string fileString = Path.Combine(filePath.FullName, "ollama_voice.wav");
        fileUri = new Uri(fileString).AbsoluteUri;
        cubeAudioSource = GetComponent<AudioSource>();
        
    }

    // Update is called once per frame
    void Update()
    {
        if (udpClient.Available > 0)
        {
            StartCoroutine(playAudio());
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
