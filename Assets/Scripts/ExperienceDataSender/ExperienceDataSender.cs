using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using BeginningUI;
using Michsky.MUIP;
using ProfessionalDataFinder;
using SignIn;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;
using UserData_Related;
using Random = UnityEngine.Random;

namespace ExperienceDataSender

{
    public enum ClientType
    {
        User,
        Professional
    }

    [Serializable]
    public class AnswersDataWithUser
    {
        public List<string> answers = new List<string>();
        public int ID;
    }

    [Serializable]
    public class ResponseData
    {
        public string msg;
        public List<string> profnames;
        public List<string> budgets;
        public List<string> expertises;
    }


    public class ExperienceDataSender : MonoBehaviour
    {
        [SerializeField] private List<TMP_InputField> userInputs;
        [SerializeField] private string apiEndPoint;

        private int _id;

        [SerializeField] private ButtonManager buttonManager;

        [SerializeField] private SlidePanelController slidePanelController;
        [SerializeField] private ProfessionalDataGenerator professionalDataGenerator;
        [SerializeField] private TotalUsersShow totalUsersShow;

        [SerializeField] ClientType clientType;


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

        private ProfessionalsData _professionalsData = new ProfessionalsData();

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
                    ResponseData responseData = JsonUtility.FromJson<ResponseData>(request.downloadHandler.text);

                    if (clientType == ClientType.User)
                    {
                        for (int i = 0; i < responseData.profnames.Count; i++)
                        {
                            ProfessionalData professionalData = new ProfessionalData();
                            professionalData.name = responseData.profnames[i];
                            professionalData.budget = responseData.budgets[i];
                            professionalData.summary = responseData.expertises[i];

                            _professionalsData.professionalDataCollection.Add(professionalData);
                        }


                        professionalDataGenerator.SpawnProfessionalData(_professionalsData);
                    }
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