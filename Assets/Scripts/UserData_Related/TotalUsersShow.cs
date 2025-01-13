using System;
using ProfessionalDataFinder;
using UnityEngine;

namespace UserData_Related
{
    public class TotalUsersShow : MonoBehaviour
    {
        private int _count = 10;

        [SerializeField] private GameObject userDataPrefab;
        [SerializeField] private Transform instantiatinoParent;

        // PRIVATE SESSIONSTARTER SESSIONSTARTER        //class that handles session start and prompts other user that
        private void Start()
        {
            for (int i = 0; i < _count; i++)
            {
                GameObject obj = Instantiate(userDataPrefab, transform.position, Quaternion.identity, instantiatinoParent);
                UserData menuProfDataInititator = obj.GetComponent<UserData>();

                UserData capturedMenuProfDataInititator = menuProfDataInititator;

                capturedMenuProfDataInititator.GetSessionStartButton().onClick.AddListener(() =>
                {
                    
                });
                
            }
        }
    }
}
