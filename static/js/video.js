const player = new Plyr('#player');


function ajustarPaddingNavButtons() {
    const player = document.querySelector('.player-size');
    const navButtons = document.querySelector('.nav-buttons');

    if (!player || !navButtons) return;

    const playerWidth = player.offsetWidth;
    const screenWidth = window.innerWidth;

    if (playerWidth === screenWidth) {
        navButtons.style.paddingRight = '.5rem';
    } else {
        navButtons.style.paddingRight = '';
    }
}

// Executa ao carregar a página
window.addEventListener('load', ajustarPaddingNavButtons);
// Executa ao redimensionar a janela
window.addEventListener('resize', ajustarPaddingNavButtons);

