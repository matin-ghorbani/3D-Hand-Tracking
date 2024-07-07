using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandTracking : MonoBehaviour
{
    // Start is called before the first frame update
    public UDPReceive udpReceive;
    public GameObject[] handPoints;
    void Start()
    {

    }

    // Update is called once per frame
    private int offset = 70;
    void Update()
    {
        string data = udpReceive.data;
        if (data.Length > 0)
        {
            data = data.Remove(0, 1);
            data = data.Remove(data.Length - 1, 1);

            string[] points = data.Split(',');
            // print(points[0]);

            for (int i = 0; i < 21; i++)
            {
                float x = 7 - float.Parse(points[i * 3]) / this.offset;
                float y = float.Parse(points[i * 3 + 1]) / this.offset;
                float z = float.Parse(points[i * 3 + 2]) / this.offset;

                handPoints[i].transform.localPosition = new Vector3(x, y, z);
            }
        }
        else
            print("No hand detected.");
    }
}
