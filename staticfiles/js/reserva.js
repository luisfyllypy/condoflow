function updateForm() {
  const area = document.getElementById('area').value;
  const fields = document.querySelectorAll('.reservationFields');
  fields.forEach(field => field.style.display = 'none');

  if (area === 'churrasqueira') {
      document.getElementById('churrasqueiraFields').style.display = 'block';
  } else if (area === 'piscina') {
      document.getElementById('piscinaFields').style.display = 'block';
  } else if (area === 'quadra') {
      document.getElementById('quadraFields').style.display = 'block';
  } else if (area === 'sala_jogos') {
      document.getElementById('salaJogosFields').style.display = 'block';
  } else if (area === 'salao_festas') {
      document.getElementById('salaoFestasFields').style.display = 'block';
  }
}
