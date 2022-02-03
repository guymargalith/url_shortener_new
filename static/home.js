const resultURL = document.getElementById('result_url')
const copyButton = document.getElementById('copy_button')

copyButton.addEventListener('click', () => {
    navigator.clipboard.writeText(
        resultURL.textContent
      );
})
