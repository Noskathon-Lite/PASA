using DG.Tweening;
using Michsky.MUIP;
using UnityEngine;

namespace BeginningUI
{
    public class SlidePanelController : MonoBehaviour
    {
        [SerializeField] private ButtonManager openingButton;
        [SerializeField] private GameObject slidePanel;
        [SerializeField] private ButtonManager closeButton;

        private RectTransform _slidePanelRectTransform;
        private Vector2 _initialAnchoredPos;

        private void Start()
        {
            _slidePanelRectTransform = slidePanel.GetComponent<RectTransform>();
            _initialAnchoredPos = _slidePanelRectTransform.anchoredPosition;

            if (openingButton)
            {
                openingButton.onClick.AddListener(OpenPanel);

            }
            if (closeButton)
            {
                closeButton.onClick.AddListener(ClosePanel);

            }
        }

        private void ClosePanel()
        {
            _slidePanelRectTransform.DOAnchorPos(_initialAnchoredPos, 0.2f).SetEase(Ease.InQuad);
        }

        public void OpenPanel()
        {
            Vector2 targetPosition = new Vector2(0, _initialAnchoredPos.y);
            _slidePanelRectTransform.DOAnchorPos(targetPosition, 0.3f).SetEase(Ease.OutQuad);
        }
    }
}