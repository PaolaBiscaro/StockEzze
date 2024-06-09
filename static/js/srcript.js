
const displayData = data => {
    const container = document.querySelector(".container1");
    container.innerHTML = "";
    data.forEach(e => {
        container.innerHTML += `
        <div class="produto">
            <h5>${e.codigo}</h5>
            <h3>${e.title}</h3>
            <div class="descricao_produto">
                <p>${e.descricao}</p>
            </div>
        </div>
        `
    });
}

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

function showPopup(display) {
    const popup = document.getElementById('bg-modal');
    if (display === 'flex') {
        popup.classList.add('show');
        popup.querySelector('.pop-do-dois').classList.add('show');
    } else {
        popup.classList.remove('show');
        popup.querySelector('.pop-do-dois').classList.remove('show');
    }
}

function showPopup1(display) {
    const popup = document.getElementById('bg-modal1');
    if (display === 'flex') {
        popup.classList.add('show');
        popup.querySelector('.modal-contact').classList.add('show');
    } else {
        popup.classList.remove('show');
        popup.querySelector('.modal-contact').classList.remove('show');
    }
}


/*FILTRO*/

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

//Função para alternar a visibilidade dos detalhes do produto
function showHide(id) {
    const element = document.querySelector(id);
    element.classList.toggle('ativo');
}


// function showHide(produtoId) {
//     var divProduto = document.getElementById(produtoId);
//     var divDescricao = divProduto.querySelector('.descricao_produto');

//     if (divDescricao.style.display === "none" || divDescricao.style.display === "") {
//         divDescricao.style.display = "block";
//     } else {
//         divDescricao.style.display = "none";
//     }
// }

// function showHide(elementId) {
//     var element = document.getElementById(elementId);
//     if (element.style.display === "none" || element.style.display === "") {
//         element.style.display = "block";
//     } else {
//         element.style.display = "none";
//     }
// }

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

// Função para exibir popup de forma suave
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

function showPopup1(display) {
    const modal = document.getElementById('bg-modal1');
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
