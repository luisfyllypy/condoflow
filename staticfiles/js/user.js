document.addEventListener('DOMContentLoaded', () => {
    const editModal = document.getElementById('edit-modal');
    const deleteModal = document.getElementById('delete-modal');
    const closeButtons = document.querySelectorAll('.close');
    const editForm = document.getElementById('edit-form');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
    let userIdToDelete = null;

    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', () => {
            const userId = button.getAttribute('data-id');
            console.log(`Edit button clicked for user ID: ${userId}`);
            // Fetch user data and populate the form
            fetch(`/users/${userId}/edit/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => response.json())
                .then(data => {
                    console.log('User data fetched:', data);
                    document.getElementById('edit-user-id').value = data.id;
                    document.getElementById('edit-username').value = data.username;
                    document.getElementById('edit-email').value = data.email;
                    document.getElementById('edit-user-type').value = data.user_type;
                    editModal.style.display = 'block';
                    console.log('Edit modal should be visible now');
                })
                .catch(error => {
                    console.error('Error fetching user data:', error);
                });
        });
    });

    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', () => {
            userIdToDelete = button.getAttribute('data-id');
            deleteModal.style.display = 'block';
        });
    });

    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            editModal.style.display = 'none';
            deleteModal.style.display = 'none';
        });
    });

    window.addEventListener('click', (event) => {
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
        }
    });

    confirmDeleteBtn.addEventListener('click', () => {
        fetch(`/users/${userIdToDelete}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(() => {
            deleteModal.style.display = 'none';
            location.reload();
        });
    });

    editForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const userId = document.getElementById('edit-user-id').value;
        const formData = new FormData(editForm);
        fetch(`/users/${userId}/edit/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(response => {
            if (response.ok) {
                editModal.style.display = 'none';
                location.reload();
            } else {
                alert('Erro ao atualizar o usuário.');
            }
        });
    });

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
});