using Michsky.MUIP;
using TMPro;
using UnityEngine;

namespace UserData_Related
{
    public class UserData : MonoBehaviour
    {
        [SerializeField] private TMP_Text userName;
        [SerializeField] private TMP_Text problemText;
        [SerializeField] private ButtonManager startSessionButton;

        // [SerializeField]
        // private  SessionCreator SessionCreator;

        public void SetUserName(string uName)
        {
            userName.text = uName;
        }

        public void SetProblemText(string pText)
        {
            problemText.text = pText;
        }

        public ButtonManager GetSessionStartButton()
        {
            return startSessionButton;
        }
    }
}