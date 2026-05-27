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
    //128 is the length of the audio sample has to be a power of 2
    private float[] audioSample = new float[128];
    private int sampleLen = 128;
    private Material cubeMaterial;

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
        string rootDir = Path.GetFullPath(Path.Combine(Application.dataPath, "..", ".."));
        string fileString = Path.Combine(rootDir, "ollama_voice.wav");
        fileUri = new Uri(fileString).AbsoluteUri;
        cubeAudioSource = GetComponent<AudioSource>();
        var cubeRenderer = GetComponent<Renderer>();
        cubeMaterial = cubeRenderer.material;
    }

    // Update is called once per frame
    void Update()
    {
        if (udpClient.Available > 0)
        {
            StartCoroutine(playAudio());
        }
        if (cubeAudioSource.isPlaying)
        {
            cubeAudioSource.GetOutputData(audioSample, 0);
            float totalSample = 0;
            for (int i = 0; i < sampleLen; i++)
            {
                totalSample += Math.Abs(audioSample[i]);
            }
            float averageSample = totalSample / sampleLen;
            cubeMaterial.SetFloat("_PulseSpeed", 0.0f);
            cubeMaterial.SetFloat("_SpeakStrength", averageSample);
        }
        else
        {
            cubeMaterial.SetFloat("_PulseSpeed", 1.0f);
            cubeMaterial.SetFloat("_SpeakStrength", 0.0f);
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
