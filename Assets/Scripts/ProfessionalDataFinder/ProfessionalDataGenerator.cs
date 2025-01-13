using System;
using System.Collections.Generic;
using BeginningUI;
using SignIn;
using TMPro;
using Unity.Mathematics;
using UnityEngine;

namespace ProfessionalDataFinder
{
    public class ProfessionalDataGenerator : MonoBehaviour
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


        private List<GameObject> objs = new List<GameObject>();
        public void SpawnProfessionalData(ProfessionalsData professionalsData)
        {
            if (objs.Count>0)
            {
                return;
            }
            
            foreach (var profDatta in professionalsData.professionalDataCollection)
            {
                GameObject obj = Instantiate(professionalBasicData, transform.position, Quaternion.identity,
                    basicDataParent);
                objs.Add(obj);
                MainMenuProfDataInititator menuProfDataInititator = obj.GetComponent<MainMenuProfDataInititator>();

                menuProfDataInititator.SetProfName(profDatta.name);
                menuProfDataInititator.SetProfBudget(profDatta.budget);
                menuProfDataInititator.SetProfExpertise(profDatta.summary);


                MainMenuProfDataInititator capturedMenuProfDataInititator = menuProfDataInititator;


                capturedMenuProfDataInititator.GetCurrentButton().onClick.AddListener(() =>
                {
                    popAnimation.OpenPanel();
                    professionalName.text = capturedMenuProfDataInititator.GetProfName();
                    professionalExpertise.text = capturedMenuProfDataInititator.GetExpertise();
                    professionalBudget.text = capturedMenuProfDataInititator.GetBudget();
                });
            }
        }
    }
}