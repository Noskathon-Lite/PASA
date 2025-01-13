using System;
using System.Collections;
using System.Text;
using BeginningUI;
using Michsky.MUIP;
using TMPro;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.Rendering.Universal;

namespace RegistrationAuth
{
    public class RegistrationAuthUser : MonoBehaviour
    {
        [SerializeField] private TMP_InputField fullName;
        [SerializeField] private TMP_InputField userName;
        [SerializeField] private TMP_InputField email;
        [SerializeField] private TMP_InputField password;

        [SerializeField] private ButtonManager submitButton;

        private RegistrationDataUser _regAuth = new RegistrationDataUser();
        [SerializeField] private SlidePanelController slidePanelController;
        [SerializeField] private ExperienceDataSender.ExperienceDataSender dataSender;

        [SerializeField] private string ApiUrl = "https://-api-endpoint.com/register"; // Api end point

        private void Start()
        {
            submitButton.onClick.AddListener(() =>
            {
                _regAuth.fullname = fullName.text;
                _regAuth.username = userName.text;
                _regAuth.email = email.text;
                _regAuth.password = password.text;


                StartCoroutine(SendDataToServer());
            });
        }

        private IEnumerator SendDataToServer()
        {
            string jsonData = JsonUtility.ToJson(_regAuth);

            using (UnityWebRequest request = new UnityWebRequest(ApiUrl, "POST"))
            {
                byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
                request.uploadHandler = new UploadHandlerRaw(bodyRaw);
                request.downloadHandler = new DownloadHandlerBuffer();

                request.SetRequestHeader("Content-Type", "application/json");


                yield return request.SendWebRequest();

                if (request.result == UnityWebRequest.Result.Success)
                {
                    Debug.Log("Registration successful: " + request.downloadHandler.text);
                    if (slidePanelController)
                    {
                        slidePanelController.OpenPanel();

                        SignUpResponse response = JsonUtility.FromJson<SignUpResponse>(request.downloadHandler.text);

                        dataSender.SetId(response.id);
                    }
                }
                else
                {
                    Debug.LogError("Registration failed: " + request.error);
                }
            }
        }
    }
}