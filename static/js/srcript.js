// Exibir dados
const displayData = data => {
    const container = document.querySelector(".container1");
    container.innerHTML = "";
    data.forEach(e => {
        container.innerHTML += `
        <div class="produto" data-id="${e.id}">
            <h5>${e.codigo}</h5>
            <h3>${e.title}</h3>
            <div class="descricao_produto">
                <p>${e.descricao}</p>
            </div>
        </div>
        `;
    });
}

// Função de busca
const searchInput = document.querySelector("#searchInput");
const produtos = document.querySelectorAll(".produto");

searchInput.addEventListener("keyup", (e) => {
    const searchTerm = e.target.value.toLowerCase();
    produtos.forEach(produto => {
        const codigo = produto.querySelector("h5").textContent.toLowerCase();
        const title = produto.querySelector("h3").textContent.toLowerCase();
        const descricao = produto.querySelector(".descricao_produto p").textContent.toLowerCase();
        if (codigo.includes(searchTerm) || title.includes(searchTerm) || descricao.includes(searchTerm)) {
            produto.style.display = "block";
        } else {
            produto.style.display = "none";
        }
    });
});

// Função para exibir o popup de exclusão
function showPopup1(display, produtoId) {
    const modal = document.getElementById('bg-modal1');
    const deleteForm = document.getElementById('deleteForm');
    const produtoIdInput = document.getElementById('produtoId');

    modal.style.display = display;
    if (display === 'flex') {
        modal.style.opacity = 0;
        setTimeout(() => {
            modal.style.opacity = 1;
            modal.classList.add('show');
        }, 10);
        // Define o ID do produto no formulário
        produtoIdInput.value = produtoId;
        deleteForm.action = `/deletar/${produtoId}`;
    } else {
        modal.style.opacity = 0;
        setTimeout(() => {
            modal.classList.remove('show');
            modal.style.display = 'none';
        }, 300);
    }
}

// Função para exibir popup genérico
function showPopup(display) {
    const modal = document.getElementById('bg-modal');
    modal.style.display = display;
    if (display === 'flex') {
        modal.style.opacity = 0;
        setTimeout(() => {
            modal.style.opacity = 1;
            modal.classList.add('show');
        }, 10);
    } else {
        modal.style.opacity = 0;
        setTimeout(() => {
            modal.classList.remove('show');
            modal.style.display = 'none';
        }, 300);
    }
}

// Função para exibir popup genérico
function showPopup2(display) {
    const modal = document.getElementById('bg-modal2');
    modal.style.display = display;
    if (display === 'flex') {
        modal.style.opacity = 0;
        setTimeout(() => {
            modal.style.opacity = 1;
            modal.classList.add('show');
        }, 10);
    } else {
        modal.style.opacity = 0;
        setTimeout(() => {
            modal.classList.remove('show');
            modal.style.display = 'none';
        }, 300);
    }
}


// Função para alternar a visibilidade do dropdown
function toggleDropdown() {
    const dropdownContent = document.getElementById('dropdown-content');
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
}

// Função para ordenar os produtos
function sortProducts(criteria) {
    const productList = document.querySelector('.container1');
    const products = Array.from(document.querySelectorAll('.produto'));

    products.sort((a, b) => {
        const aValue = a.getAttribute(`data-${criteria}`);
        const bValue = b.getAttribute(`data-${criteria}`);

        if (criteria === 'name') {
            return aValue.localeCompare(bValue);
        } else if (criteria === 'quantity') {
            return parseInt(aValue) - parseInt(bValue);
        } else {
            return aValue.localeCompare(bValue);
        }
    });

    productList.innerHTML = '';
    products.forEach(product => productList.appendChild(product));
}

// Função para filtrar os produtos por nível de estoque
function filterStock(stockLevel) {
    const products = document.querySelectorAll('.produto');

    products.forEach(product => {
        const stock = product.getAttribute('data-stock');
        product.style.display = (stock === stockLevel) ? 'block' : 'none';
    });
}

// Função para redefinir o filtro e mostrar todos os produtos
function resetFilter() {
    const products = document.querySelectorAll('.produto');
    products.forEach(product => {
        product.style.display = 'block';
    });
}

// Função para alternar a visibilidade dos detalhes do produto
function showHide(id) {
    console.log("ID passado para showHide:", id);
    const element = document.getElementById(id);
    if (element) {
        console.log("Elemento encontrado:", element);
        element.classList.toggle('ativo');
    } else {
        console.log("Elemento não encontrado para o ID:", id);
    }
}

// Fechar dropdown quando clicado fora dele
document.addEventListener('click', function(event) {
    const dropdownContent = document.getElementById('dropdown-content');
    const dropdownButton = document.querySelector('.dropbtn');

    if (!dropdownButton.contains(event.target) && !dropdownContent.contains(event.target)) {
        dropdownContent.style.display = 'none';
    }
});

// Evitar o fechamento dos detalhes do produto ao clicar no dropdown
document.querySelectorAll('.produto').forEach(produto => {
    produto.addEventListener('click', function(event) {
        event.stopPropagation();
    });
});
