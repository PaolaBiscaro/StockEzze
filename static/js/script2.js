document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector("#searchInput");
    const lotes = document.querySelectorAll(".lote");

    searchInput.addEventListener("keyup", () => {
        const searchValue = searchInput.value.toLowerCase();

        lotes.forEach(lote => {
            const loteTitle = lote.querySelector("h3").textContent.toLowerCase();
            if (loteTitle.includes(searchValue)) {
                lote.style.display = "";
            } else {
                lote.style.display = "none";
            }
        });
    });
});

/*FILTRO*/

// Função para ordenar os produtos
function sortProducts(criteria) {
    const loteList = document.querySelectorAll('.lote');

    const sortedLotes = Array.from(loteList).sort((a, b) => {
        const aValue = a.getAttribute(`data-${criteria}`);
        const bValue = b.getAttribute(`data-${criteria}`);

        if (criteria === 'name') {
            return aValue.localeCompare(bValue);
        } else if (criteria === 'quantity') {
            return parseInt(aValue) - parseInt(bValue);
        } else {
            return 0;
        }
    });

    const container = document.querySelector('.container2');
    container.innerHTML = '';
    sortedLotes.forEach(lote => container.appendChild(lote));
}

// Função para redefinir o filtro e mostrar todos os lotes
function resetFilter() {
    const lotes = document.querySelectorAll('.lote');
    lotes.forEach(lote => {
        lote.style.display = 'block';
    });
}
