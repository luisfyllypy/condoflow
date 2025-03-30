function enviarConvocacao() {
    const assunto = document.getElementById("assunto").value;
    const local = document.getElementById("local").value;
    const data = document.getElementById("data").value;
    const destinatarios = document.getElementById("destinatarios").value;
  
    // Aqui você pode realizar a lógica para enviar a convocação, por exemplo, exibindo um alerta
    alert(`Convocação enviada!\nAssunto: ${assunto}\nLocal: ${local}\nData: ${data}\nDestinatários: ${destinatarios}`);
  }
  