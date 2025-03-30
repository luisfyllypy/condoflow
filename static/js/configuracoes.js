function showAppearance() {
    hideAllConfigurations();
    document.getElementById("config-panel").innerHTML = "Configurações de Aparência serão exibidas aqui.";
    document.getElementById("config-panel").style.display = "block";
}

function showPrivacy() {
    hideAllConfigurations();
    document.getElementById("config-panel").innerHTML = "Configurações de Privacidade e Segurança serão exibidas aqui.";
    document.getElementById("config-panel").style.display = "block";
}

function showImportData() {
    hideAllConfigurations();
    document.getElementById("config-panel").innerHTML = "Opções de Importação de Dados serão exibidas aqui.";
    document.getElementById("config-panel").style.display = "block";
}

function showGenerateReport() {
    hideAllConfigurations();
    document.getElementById("config-panel").innerHTML = "Opções para Gerar Relatórios serão exibidas aqui.";
    document.getElementById("config-panel").style.display = "block";
}

function hideAllConfigurations() {
    document.getElementById("config-panel").style.display = "none";
}
