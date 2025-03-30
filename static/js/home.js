document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".btn-lido").forEach(button => {
        button.addEventListener("click", function () {
            const avisoId = this.getAttribute("data-aviso-id");

            fetch(`/marcar_lido/${avisoId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();  // Recarrega a página para atualizar os avisos
                }
            });
        });
    });
});
