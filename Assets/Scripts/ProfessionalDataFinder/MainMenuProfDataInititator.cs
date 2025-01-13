using Michsky.MUIP;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace ProfessionalDataFinder
{
    public class MainMenuProfDataInititator : MonoBehaviour
    {
        [SerializeField] private TMP_Text profName;
        [SerializeField] private TMP_Text profExpertise;
        [SerializeField] private TMP_Text profBudget;
        [SerializeField] private ButtonManager profButton;

        private string _profId;


        public void SetProfName(string profNameString)
        {
            this.profName.text = profNameString;
        }

        public void SetProfId(string id)
        {
            _profId = id;
        }

        public string GetProfId()
        {
            return _profId;
        }

        public void SetProfExpertise(string expertise)
        {
            profExpertise.text = expertise;
        }

        public void SetProfBudget(string budget)
        {
            profBudget.text = budget;
        }

        public ButtonManager GetCurrentButton()
        {
            return profButton;
        }
    }
}