using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using BeginningUI;
using Michsky.MUIP;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;
using Random = UnityEngine.Random;

namespace ExperienceDataSender
{
    [Serializable]
    public class AnswersDataWithUser
    {
        public List<string> answers = new List<string>();
        public int ID;
    }

    public class ExperienceDataSender : MonoBehaviour
    {
        [SerializeField] private List<TMP_InputField> userInputs;
        [SerializeField] private string apiEndPoint;

        private int _id;

        [SerializeField] private ButtonManager buttonManager;

        [SerializeField] private SlidePanelController slidePanelController;

        private void Start()
        {
            buttonManager.onClick.AddListener(() =>
            {
                if (_id <= 0)
                {
                    Debug.Log("No id Set");
                    return;
                }

                // Prepare the data
                AnswersDataWithUser dataToSend = new AnswersDataWithUser
                {
                    ID = _id
                };
                dataToSend.answers.Clear();
                foreach (var input in userInputs)
                {
                    dataToSend.answers.Add(input.text);
                }

                StartCoroutine(SendDataToServer(dataToSend));
            });
        }

        private IEnumerator SendDataToServer(AnswersDataWithUser data)
        {
            string jsonData = JsonUtility.ToJson(data);

            using (UnityWebRequest request = new UnityWebRequest(apiEndPoint, "POST"))
            {
                byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
                request.uploadHandler = new UploadHandlerRaw(bodyRaw);
                request.downloadHandler = new DownloadHandlerBuffer();

                request.SetRequestHeader("Content-Type", "application/json");

                yield return request.SendWebRequest();

                if (request.result == UnityWebRequest.Result.Success)
                {
                    Debug.Log("Data sent successfully: " + request.downloadHandler.text);

                    slidePanelController.OpenPanel();
                }
                else
                {
                    Debug.LogError("Failed to send data: " + request.error);
                }
            }
        }

        public void SetId(int id)
        {
            _id = id;
        }
    }
}