using System;
using System.Collections;
using System.Collections.Generic;
using System.Text;
using BeginningUI;
using Michsky.MUIP;
using NUnit.Framework;
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
        public string professional;
        public string budgets;
        public string summary;
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
        public List<ProfessionalData> professionalDataCollection;
    }


    public class SignInAuth : MonoBehaviour
    {
        [SerializeField] private TMP_InputField userName;
        [SerializeField] private TMP_InputField password;
        [SerializeField] private ButtonManager submitButton;

        [Header("Animations")] [SerializeField]
        private SlidePanelController userMainMenuSLide;


        private UserLoginData _userLoginData = new UserLoginData();

        private const string ApiUrl = "";
        //    private const string ApiKey = "-api-key";

        private void Start()
        {
            submitButton.onClick.AddListener(CheckData);
        }

        private void CheckData()
        {
            _userLoginData.username = userName.text;
            _userLoginData.password = password.text;

            StartCoroutine(SendLoginDataToApi());
        }

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
                        Debug.Log($"Message: {loginResponse.msg}");
                        Debug.Log($"Username: {loginResponse.username}");
                        Debug.Log($"User Type: {loginResponse.userType}");

                        // Perform actions based on the deserialized data
                        if (loginResponse.userType == "User")
                        {
                            Debug.Log("Regular user logged in.");
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
                    //the response we get  is the type of the user.
                }
                else
                {
                    Debug.LogError("Login failed: " + request.error);
                    //do not let user login
                }
            }
        }
    }
}