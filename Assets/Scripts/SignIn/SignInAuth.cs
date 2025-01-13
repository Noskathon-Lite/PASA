using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using BeginningUI;
using Michsky.MUIP;
using NUnit.Framework;
using ProfessionalDataFinder;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.Serialization;

namespace SignIn
{
    [Serializable]
    public class UserLoginData
    {
        [FormerlySerializedAs("usrname")] [FormerlySerializedAs("userName")]
        public string username;

        [FormerlySerializedAs("userPassword")] public string password;
    }

    [Serializable]
    public class LoginResponse
    {
        public string msg;
        public string username;
        public string userType;

        // Match JSON keys
        public List<string> profnames = new List<string>();
        public List<int> budgets = new List<int>(); // Budget is an integer in the JSON
        public List<string> summaries = new List<string>();
    }

    [Serializable]
    public class ProfessionalData
    {
        public string name;
        public string budget;
        public string summary;
    }

    [Serializable]
    public class ProfessionalsData
    {
        public List<ProfessionalData> professionalDataCollection = new List<ProfessionalData>();
    }


    public class SignInAuth : MonoBehaviour
    {
        [SerializeField] private TMP_InputField userName;
        [SerializeField] private TMP_InputField password;
        [SerializeField] private ButtonManager submitButton;

        [Header("Animations")] [SerializeField]
        private SlidePanelController userMainMenuSLide;


        private UserLoginData _userLoginData = new UserLoginData();

        private const string ApiUrl = "http://192.168.137.16:8000/login";

        [SerializeField] private ProfessionalDataGenerator professionalDataGenerator;
        //    private const string ApiKey = "-api-key";

        private void Start()
        {
            _professionalsData.professionalDataCollection.Clear();

            submitButton.onClick.AddListener(CheckData);
        }

        private void CheckData()
        {
            if (_professionalsData.professionalDataCollection.Count>0)
            {
                return;
            }
            _userLoginData.username = userName.text;
            _userLoginData.password = password.text;

            StartCoroutine(SendLoginDataToApi());
        }

        private ProfessionalsData _professionalsData = new ProfessionalsData();

      private IEnumerator SendLoginDataToApi()
{
    string jsonData = JsonUtility.ToJson(_userLoginData);

    using (UnityWebRequest request = new UnityWebRequest(ApiUrl, "POST"))
    {
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();

        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("Login successful: " + request.downloadHandler.text);

            LoginResponse loginResponse = JsonUtility.FromJson<LoginResponse>(request.downloadHandler.text);

            if (loginResponse != null)
            {
                for (int i = 0; i < loginResponse.profnames.Count; i++)
                {
                    ProfessionalData professionalData = new ProfessionalData
                    {
                        name = loginResponse.profnames[i],
                        budget = loginResponse.budgets[i].ToString(), // Convert int to string
                        summary = loginResponse.summaries[i]
                    };

                    _professionalsData.professionalDataCollection.Add(professionalData);
                }

                Debug.Log($"Message: {loginResponse.msg}");
                Debug.Log($"Username: {loginResponse.username}");
                Debug.Log($"User Type: {loginResponse.userType}");

                if (loginResponse.userType == "User")
                {
                    Debug.Log("Regular user logged in.");
                    professionalDataGenerator.SpawnProfessionalData(_professionalsData);
                }
                else if (loginResponse.userType == "Prof")
                {
                    Debug.Log("Professional logged in.");
                }
            }
            else
            {
                Debug.LogError("Failed to deserialize login response.");
            }
            userMainMenuSLide.OpenPanel();
        }
        else
        {
            Debug.LogError("Login failed: " + request.error);
        }
    }
}

    }
}