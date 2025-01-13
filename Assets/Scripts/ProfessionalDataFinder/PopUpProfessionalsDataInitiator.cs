using System;
using BeginningUI;
using TMPro;
using Unity.Mathematics;
using UnityEngine;

namespace ProfessionalDataFinder
{
    public class PopUpProfessionalsDataInitiator : MonoBehaviour
    {
        [Header("it is a pop up data shown")] [SerializeField]
        private GameObject professionalDataDisplayObject;

        [SerializeField] private TMP_Text professionalName;
        [SerializeField] private TMP_Text professionalExpertise;
        [SerializeField] private TMP_Text professionalBudget;


        [Header("it is a basic prefab shown in main menu")] [SerializeField]
        private GameObject professionalBasicData;

        [SerializeField] private Transform basicDataParent;

        [SerializeField] private UIPanelPopAnimation popAnimation;

        private int _count = 10;

        //here we send api calls and receive all data from it and ensure the initiator has data filled.
        //after filling data, when the button is clicked we ensure the texts to be changed and all


        private void Start()
        {
            for (int i = 0; i < _count; i++)
            {
                GameObject obj = Instantiate(professionalBasicData, transform.position, Quaternion.identity, basicDataParent);
                MainMenuProfDataInititator menuProfDataInititator = obj.GetComponent<MainMenuProfDataInititator>();

                MainMenuProfDataInititator capturedMenuProfDataInititator = menuProfDataInititator;

                capturedMenuProfDataInititator.GetCurrentButton().onClick.AddListener(() =>
                {
                    popAnimation.OpenPanel();
                });
            }
        }

    }
}