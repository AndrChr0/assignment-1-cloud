
const btn = document.querySelector('#hard-mode-btn');


btn.addEventListener('click', () => {
    const formHardMode = document.querySelector('form')
    formHardMode.classList.add('hard-mode');
    btn.style.display = 'none';
})