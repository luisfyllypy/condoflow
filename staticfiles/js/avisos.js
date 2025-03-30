document.addEventListener('DOMContentLoaded', () => {
    const noticeList = document.getElementById('notice-list');
    const addNoticeBtn = document.getElementById('add-notice-btn');
    const noticeForm = document.getElementById('notice-form');
    const noticeInput = noticeForm.querySelector('input[name="titulo"]');
    const noticeText = noticeForm.querySelector('textarea[name="texto"]');
    const saveNoticeBtn = noticeForm.querySelector('button[type="submit"]');
    const closeBtn = document.querySelector('.close');

    // Abre o formulário ao clicar no botão "Adicionar Aviso"
    addNoticeBtn.addEventListener('click', () => {
        noticeInput.value = '';
        noticeText.value = '';
        noticeForm.classList.remove('hidden'); // Mostra o formulário
        noticeForm.action = '{% url "criar_aviso" %}'; // Ação para adicionar aviso
    });

    // Fecha o formulário ao clicar no botão de fechar
    closeBtn.addEventListener('click', () => {
        noticeForm.classList.add('hidden'); // Esconde o formulário
    });

    // Salva o aviso e atualiza a lista
    saveNoticeBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Previne o comportamento padrão do botão
        const newNoticeTitle = noticeInput.value;
        const newNoticeText = noticeText.value;
        if (newNoticeTitle.trim() !== '' && newNoticeText.trim() !== '') {
            // Verifica se o formulário está configurado para edição
            const formAction = noticeForm.action;
            if (formAction.includes("editar_aviso")) {
                // Aqui você deve fazer uma requisição para atualizar o aviso
                const id = noticeForm.dataset.id; // O ID deve ser armazenado no dataset do formulário
                updateNotice(id, newNoticeTitle, newNoticeText);
            } else {
                // Criação de um novo aviso
                createNotice(newNoticeTitle, newNoticeText);
            }
        }
    });

    // Atualiza a lista de avisos exibidos
    function updateNoticeList() {
        noticeList.innerHTML = ''; // Limpa a lista
        // Adiciona os avisos da lista notices
        // Você deve modificar aqui para pegar os dados reais do Django
        notices.forEach((notice) => {
            const noticeItem = document.createElement('li');
            noticeItem.className = 'notice-item';
            noticeItem.dataset.id = notice.id; // Adiciona o ID para a exclusão/edição
            noticeItem.innerHTML = `
                <h3>${notice.titulo}</h3>
                <p>${notice.texto}</p>
                <button onclick="showEditForm(${notice.id}, '${notice.titulo}', '${notice.texto}')">Editar</button>
                <button onclick="deleteNotice(${notice.id})">Excluir</button>
            `;
            noticeList.appendChild(noticeItem);
        });
    }

    // Função para criar um novo aviso
    function createNotice(title, text) {
        fetch('{% url "criar_aviso" %}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}', // Adiciona o token CSRF
            },
            body: JSON.stringify({ titulo: title, texto: text }),
        })
        .then(response => {
            if (response.ok) {
                response.json().then(newNotice => {
                    notices.push(newNotice); // Adiciona o aviso à lista local
                    updateNoticeList(); // Atualiza a lista
                });
            } else {
                alert('Falha ao criar aviso.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    }

    // Função para atualizar um aviso existente
    function updateNotice(id, title, text) {
        fetch(`/avisos/${id}/editar/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}', // Adiciona o token CSRF
            },
            body: JSON.stringify({ titulo: title, texto: text }),
        })
        .then(response => {
            if (response.ok) {
                // Aqui você pode encontrar o aviso atualizado e modificar a lista
                const noticeItem = notices.find(notice => notice.id === id);
                if (noticeItem) {
                    noticeItem.titulo = title;
                    noticeItem.texto = text;
                }
                updateNoticeList(); // Atualiza a lista
                noticeForm.classList.add('hidden'); // Esconde o formulário
            } else {
                alert('Falha ao atualizar aviso.');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    }

    // Função para excluir um aviso
    window.deleteNotice = function(id) {
        if (confirm('Você tem certeza que deseja excluir este aviso?')) {
            fetch(`/avisos/${id}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}', // Adiciona o token CSRF
                },
            })
            .then(response => {
                if (response.ok) {
                    // Remove o aviso da lista local
                    notices = notices.filter(notice => notice.id !== id);
                    updateNoticeList(); // Atualiza a lista
                } else {
                    alert('Falha ao excluir o aviso.');
                }
            })
            .catch(error => {
                console.error('Erro:', error);
            });
        }
    };

    // Chama a função para inicializar a lista
    updateNoticeList();
});

