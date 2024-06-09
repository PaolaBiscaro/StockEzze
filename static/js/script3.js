document.querySelector('.add-email').addEventListener('click', function (event) {
    event.preventDefault(); // Evita o comportamento padrão do botão
    // Criar um novo elemento de input para e-mail
    var newEmailInput = document.createElement('input');
    newEmailInput.type = 'email';
    newEmailInput.name = 'email';
    newEmailInput.placeholder = 'E-mail';
    newEmailInput.classList.add('email-input');

    // Adicionar o novo input ao container de e-mails
    var emailContainer = document.querySelector('.email');
    emailContainer.insertBefore(newEmailInput, emailContainer.querySelector('.add-email'));
});

document.querySelector('.add-tel').addEventListener('click', function (event) {
    event.preventDefault(); // Evita o comportamento padrão do botão
    // Criar um novo elemento de input para telefone
    var newTelInput = document.createElement('input');
    newTelInput.type = 'tel';
    newTelInput.name = 'telefone';
    newTelInput.placeholder = 'Telefone';
    newTelInput.classList.add('telefone-input');

    // Adicionar o novo input ao container de telefones
    var telContainer = document.querySelector('.telefone');
    telContainer.insertBefore(newTelInput, telContainer.querySelector('.add-tel'));
});

// Função para formatar o CNPJ
function formatCNPJ(cnpj) {
    cnpj = cnpj.replace(/\D/g, ""); // Remove todos os caracteres não numéricos
    cnpj = cnpj.replace(/^(\d{2})(\d)/, "$1.$2");
    cnpj = cnpj.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3");
    cnpj = cnpj.replace(/\.(\d{3})(\d)/, ".$1/$2");
    cnpj = cnpj.replace(/(\d{4})(\d)/, "$1-$2");
    return cnpj;
}

// Evento para formatar o input do CNPJ
document.getElementById('cnpj').addEventListener('input', function () {
    this.value = formatCNPJ(this.value);
});


function excluirCadastro() {
    window.location.href = '/meu_estoque';
}
