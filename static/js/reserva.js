function fazerReserva() {
  const area = document.getElementById("area").value;
  const data = document.getElementById("data").value;
  const hora = document.getElementById("hora").value;
  
  // Cria um objeto com os dados da reserva
  const reservaData = {
      area: area,
      data: data,
      hora: hora
  };

  // Envia os dados para o servidor usando fetch
  fetch('/reservas/criar/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify(reservaData)  // Converte os dados para o formato JSON
  })
  .then(response => response.json())  // Espera a resposta do servidor
  .then(data => {
      // Aqui você pode verificar a resposta do servidor
      if (data.success) {
          alert('Reserva feita com sucesso!');
      } else {
          alert('Erro ao fazer a reserva: ' + data.error);
      }
  })
  .catch(error => {
      alert('Erro de rede: ' + error);
  });
}
