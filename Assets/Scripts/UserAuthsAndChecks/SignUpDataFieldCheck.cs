using System.Collections.Generic;
using System.Text.RegularExpressions;
using Michsky.MUIP;
using TMPro;
using UnityEngine;

namespace UserAuthsAndChecks
{
    public class SignUpDataFieldCheck : MonoBehaviour
    {
        [SerializeField] private TMP_InputField emailInputField;
        [SerializeField] private TMP_Text emailPopUpText;
        [SerializeField] private ButtonManager submitButton;

        [SerializeField] private List<TMP_InputField> otherInputFields;

        private void Start()
        {
            submitButton.Interactable(false);
            if (emailInputField)
            {
                emailPopUpText.text = "";

            }

            foreach (var inputField in otherInputFields)
            {
                inputField.onValueChanged.AddListener(ValidateAllFields);
            }

            if (emailInputField)
            {
                emailInputField.onValueChanged.AddListener(ValidateAllFields);
            }
        }

        private void ValidateAllFields(string arg)
        {
            bool allFieldsFilled = true;
            foreach (var inputField in otherInputFields)
            {
                if (string.IsNullOrEmpty(inputField.text.Trim()))
                {
                    allFieldsFilled = false;
                    break;
                }
            }

            bool emailIsValid = true;
            if (emailInputField)
            {
                emailIsValid = ValidateEmail(emailInputField.text);
            }


            submitButton.Interactable(allFieldsFilled && emailIsValid);

            if (emailInputField)
            {
                if (!emailIsValid && !string.IsNullOrEmpty(emailInputField.text))
                {
                    emailPopUpText.text = "Invalid Email Address!";
                }
                else
                {
                    emailPopUpText.text = "";
                }
            }
        }

        private bool ValidateEmail(string email)
        {
            string emailPattern = @"^[^@\s]+@[^@\s]+\.[^@\s]+$";
            return Regex.IsMatch(email, emailPattern);
        }
    }
}