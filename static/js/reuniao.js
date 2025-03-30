function enviarReuniao() {
  const assunto = document.getElementById("assunto").value;
  const local = document.getElementById("local").value;
  const data = document.getElementById("data").value;
  const urgencia = document.getElementById("urgencia").value;
  const descricao = document.getElementById("descricao").value;
  const mensagem = document.getElementById("mensagem").value;
  const destinatarios = document.getElementById("destinatarios").value;

  fetch('/enviar-reuniao/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ assunto, local, data, urgencia, descricao, mensagem, destinatarios })
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          alert('Reunião enviada com sucesso!');
      } else {
          alert('Erro ao enviar reunião.');
      }
  });
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}