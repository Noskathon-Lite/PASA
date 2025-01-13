using System;
using DG.Tweening;
using Michsky.MUIP;
using UnityEngine;
using UnityEngine.UI;

namespace BeginningUI
{
    public class UIPanelPopAnimation : MonoBehaviour
    {
        [SerializeField] private ButtonManager openingButton;
        [SerializeField] private Image blackImage;
        [SerializeField] private GameObject openingPanel;
        [SerializeField] private ButtonManager closeButton;


        public void SetOpeningButton(ButtonManager manager)
        {
            openingButton = manager;
        }

        private void Start()
        {
            if (openingButton)
            {
                            openingButton.onClick.AddListener(() => { OpenPanel(); });

            }

            if (closeButton)
            {
                closeButton.onClick.AddListener(() => { ClosePanel(); });
            }


            blackImage.gameObject.SetActive(false);
            openingPanel.gameObject.SetActive(false);
        }

        private void ClosePanel()
        {
            openingPanel.transform.DOScale(Vector3.zero, 0.2f).OnComplete(() =>
            {
                openingPanel.gameObject.SetActive(false);
            });
            blackImage.DOFade(0, 0.2f).OnComplete(() => { blackImage.gameObject.SetActive(false); });
        }

        public void OpenPanel()
        {
            closeButton.Interactable(false);
            blackImage.DOFade(0, 0);
            openingPanel.transform.DOScale(Vector3.zero, 0f);
            blackImage.gameObject.SetActive(true);

            blackImage.DOFade(0.87f, 0.2f).OnComplete(() =>
            {
                openingPanel.gameObject.SetActive(true);
                openingPanel.transform.DOScale(Vector3.one, 0.3f).OnComplete(() => { closeButton.Interactable(true); });
            });
        }
    }
}