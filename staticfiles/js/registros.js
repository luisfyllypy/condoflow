const moradorList = document.getElementById('morador-list');
const infoDiv = document.getElementById('info');

// Exemplo de dados de moradores
const moradores = [
    {
        id: 1,
        unidade: 'Bloco A, Apt 101',
        nome: 'Thiago Albernaz',
        veiculo: '',
        cpf: '123.456.789-00',
        email: 'joao@example.com',
        telefone: '(11) 1234-5678',
        engajamento: 'Ativo'
    },
    {
        id: 1,
        unidade: 'Bloco A, Apt 101',
        nome: 'João da Silva',
        veiculo: '',
        cpf: '123.456.789-00',
        email: 'joao@example.com',
        telefone: '(11) 1234-5678',
        engajamento: 'Ativo'
    },
    {
        id: 2,
        unidade: 'Bloco B, Apt 203',
        nome: 'Maria Oliveira',
        veiculo: 'Carro - ABC-1234',
        cpf: '987.654.321-00',
        email: 'maria@example.com',
        telefone: '(22) 9876-5432',
        engajamento: 'Ativo'
    },
    {
        id: 3,
        unidade: 'Bloco C, Apt 305',
        nome: 'Carlos Pereira',
        veiculo: 'Moto - XYZ-5678',
        cpf: '555.555.555-00',
        email: 'carlos@example.com',
        telefone: '(33) 5555-5555',
        engajamento: 'Inativo'
    },
    {
        id: 3,
        unidade: 'Bloco C, Apt 305',
        nome: 'Carlos Pereira',
        veiculo: 'Moto - XYZ-5678',
        cpf: '555.555.555-00',
        email: 'carlos@example.com',
        telefone: '(33) 5555-5555',
        engajamento: 'Inativo'
    },
    {
        id: 3,
        unidade: 'Bloco C, Apt 305',
        nome: 'Augusto Gabriel Rodrigues dos Santos',
        veiculo: 'Moto - XYZ-5678',
        cpf: '555.555.555-00',
        email: 'carlos@example.com',
        telefone: '(33) 5555-5555',
        engajamento: 'Inativo'
    }
    // Outros moradores...
    
];

// Adiciona moradores à lista
function populateMoradorList() {
    moradorList.innerHTML = '';
    moradores.forEach(morador => {
        const listItem = document.createElement('li');
        const link = document.createElement('a');
        link.textContent = morador.nome;
        link.addEventListener('click', () => displayMoradorInfo(morador));
        listItem.appendChild(link);
        moradorList.appendChild(listItem);
    });
}

// Mostra informações detalhadas do morador
function displayMoradorInfo(morador) {
    infoDiv.innerHTML = `
        <h2>${morador.nome}</h2>
        <p>Unidade: ${morador.unidade}</p>
        <p>Veículo: ${morador.veiculo || 'Nenhum'}</p>
        <p>CPF: ${morador.cpf}</p>
        <p>Email: ${morador.email}</p>
        <p>Telefone: ${morador.telefone}</p>
        <p>Engajamento: ${morador.engajamento}</p>
        <button id="add-veiculo-btn">Adicionar Veículo</button>`;

    const addVeiculoBtn = document.getElementById('add-veiculo-btn');
    addVeiculoBtn.addEventListener('click', () => addVeiculo(morador));
    
    infoDiv.style.display = 'block';
}

// Adiciona veículo ao morador
function addVeiculo(morador) {
    const veiculo = prompt('Digite o veículo:');
    if (veiculo !== null && veiculo.trim() !== '') {
        morador.veiculo = veiculo;
        displayMoradorInfo(morador);
    }
}

// Inicialização
populateMoradorList();