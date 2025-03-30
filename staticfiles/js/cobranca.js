document.addEventListener('DOMContentLoaded', function () {
    const enviarCobrancaButton = document.getElementById('enviarCobranca');
  
    enviarCobrancaButton.addEventListener('click', function () {
      const moradorSelecionado = document.getElementById('moradores').value;
      const valorCobranca = document.getElementById('valor').value;
      const formaPagamento = document.getElementById('formaPagamento').value;
  
      let mensagem = `Cobrança no valor de R$${valorCobranca} enviada via ${formaPagamento}.`;
  
      if (moradorSelecionado === 'todos') {
        mensagem += ' Enviada para todos os moradores.';
      } else {
        mensagem += ` Enviada para o morador ${moradorSelecionado}.`;
      }
  
      alert(mensagem);
    });
  });
  