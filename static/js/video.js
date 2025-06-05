const player = new Plyr('#player');
const nextVideoWarnDiv = document.getElementById('nextVideoWarn')
const nextVideoWarnMessage = document.getElementById('nextVideoWarnMessage')

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

      nextVideoWarnDiv.style.display = "flex";

      // Espera 1 segundo antes de começar a contagem
      setTimeout(() => {
        nextVideoWarnMessage.innerHTML = "Indo para a próxima aula em 2 segundos!";

        setTimeout(() => {
          nextVideoWarnMessage.innerHTML = "Indo para a próxima aula em 1 segundo!";

          setTimeout(() => {
            document.getElementById("proximoVideo").click();
          }, 1000); // depois de mais 1 segundo (total 3s)

        }, 1000); // depois de 1 segundo (total 2s)

      }, 1000); // espera inicial de 1 segundo
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
