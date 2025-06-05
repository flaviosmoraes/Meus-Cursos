const player = new Plyr('#player');

player.on('ended', () => {
  console.log("Vídeo terminou!");

  // Ticka o checkbox manualmente, mas não dispara fetch por mudança no checkbox
  const checkbox = document.getElementById("checkAssistido");
  checkbox.checked = true;

  fetch(ASSISTIDO_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      video_id: VIDEO_ID,
      curso_id: CURSO_ID
    }),
  })
  .then(res => {
    if (res.ok) {
      console.log("Marcado como assistido!");
    } else {
      console.log("Erro ao marcar vídeo.");
    }
  });
});


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

document.getElementById("checkAssistido").addEventListener("change", function () {
  const method = this.checked ? 'POST' : 'DELETE';

  fetch(ASSISTIDO_URL, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      video_id: VIDEO_ID,
      curso_id: CURSO_ID
    }),
  })
  .then(res => {
    if (res.ok) {
      console.log(method === 'POST' ? "Marcado" : "Desmarcado");
    } else {
      console.error("Erro");
      this.checked = !this.checked; // volta ao estado anterior se falhar
    }
  });
});
