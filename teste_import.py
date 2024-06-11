HTML:

                <section class="container1">
                    {% for produto in produtos %}
                    <div class="produto" onclick="showHide('produto{{ produto[0] }}')" data-name="{{ produto[1] }}" data-code="{{ produto[3] }}" data-quantity="{{ produto[4] }}" data-stock="{{ produto[5] }}">
                        <!-- Conteúdo do produto -->
                        <div class="ajuste-produto">
                            <div class="produto-titulo">
                                <h5>{{ produto[3] }}</h5>
                                <h3>{{ produto[1] }}</h3>
                            </div>
                            <div class="ajuste-qtd">
                                <div class="qtd">
                                    <span class="separador"></span>
                                    <h5>QTN</h5>
                                    <p>{{ produto[4] }}</p>
                                </div>
                                <div class="lote">
                                    <a href="{{ url_for('lotes_produto', produto_id=produto_id) }}">
                                        <div class="lote-img"></div>
                                    </a>
                                    <div class="seta">
                                        {% if produto[5] == 'low' %}
                                        <img src="{{ url_for('static', filename='../static/img/seta-para-baixo.png') }}" alt="Seta para baixo">
                                        {% else %}
                                        <img src="{{ url_for('static', filename='../static/img/seta-para-cima.png') }}" alt="Seta para cima">
                                        {% endif %}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="descricao_produto" id="produto{{ produto[0] }}">
                            <p>{{ produto[2] }}</p>
                            {% for lote in lotes %}
                            </div>
                            {% endfor %}
                            <div class="botoes">
                                <button class="btn-excluir">Excluir Cadastro</button>
                                <div class="vermelhos">
                                    <button class="btn-retirar">Retirar</button>
                                    <button class="btn-adicionar">Adicionar</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
        </section>

CSS:

.container1 .descricao_produto{
    transition: .1s;
    height: 0;
    overflow: hidden;
    display: none;
}
.container1 .descricao_produto.ativo{
    height: 80%;
    transition: .1s;
    display: block;
}
.container1 .descricao_produto p{
    transition: .1s;
    padding: 20px;
}
.produto .produto-titulo h3{
    font-weight: 600;
}

.produto{
    border: 1px solid #c2c2c2;
    padding: 10px;
    cursor: pointer;
    margin: 10px;
    border-radius: 5px;

}
.produto .ajuste-produto{
    flex-direction: row;
    display: flex;
    justify-content: space-between;
    margin-left: 5px;

}       
.produto .ajuste-produto .ajuste-qtd{
    display: flex;
    flex-direction: row;
    margin: 5px;
}

 /divisão dos blocos dentro da descrição/
 .linha{
    justify-content: center;
    display: flex;
    flex-flow: row wrap;
    padding:10px;
}
.lote{
    display: flex;
    margin: auto 20px;
    flex-direction: row;
    justify-content: space-around;

}
.lote-img{
    width: 32px;
    background-image: url(../img/caixa-aberta.png);
    background-size: contain;
    background-repeat: no-repeat;
    height: 32px;
    margin: 5px;

}
.seta img{
    width: 27px;
    height: 27px;
    margin: 5px;
}

.separador::before{
    width: 2px;
    height: 40px;
    position: absolute;
    content: '';
    background-color: #b4b4b4;
    margin-left: 35px;
}
/botoes/
 .botoes{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    padding: 20px;
}
.btn-excluir{
    border: none;
    background: none;
    color: blue;
    cursor: pointer;
}
.btn-retirar{
    border: 1px solid red;
    background-color: transparent;
    border-radius: 5px;
    width: 120px;
    font-size: 12pt;
    height: 35px;
    color: red;
    margin-right: 5px;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
}
.btn-excluir:hover{
    color: #7676f5;
}
.btn-adicionar:hover{
    background-color: #f55e5e;
    border: #f55e5e;
    transform: scale(1.1);
}
.btn-retirar:hover{
    background-color: #e3e1e1;
    transform: scale(1.1);
}

.btn-adicionar{
    border: 1px solid red;
    background-color: red;
    border-radius: 5px;
    width: 120px;
    font-size: 12pt;
    height: 35px;
    color: #fff;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
} 


app.py:

@app.route('/meuestoque')
def meu_estoque():
    conn = conexao_bd()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM produto')
    produtos = cursor.fetchall()

    cursor.execute('SELECT * FROM fornecedor')
    fornecedores = cursor.fetchall()

    cursor.execute('SELECT lote.*, produto_id, estoque_minimo FROM lote JOIN produto ON lote.produto_id = produto_id')
    lotes = cursor.fetchall()

    cursor.close()
    conn.close()

    produtos_com_estado = []
    for produto in produtos:
        if produto[4] < 100:
            estado = "low"
        else:
            estado = "high"
        print(f"Produto: {produto[1]}, Estoque: {produto[4]}, Estado: {estado}")
        produtos_com_estado.append((*produto, estado))

    produto_id = 1

    return render_template('estoqueprincipal.html', produtos=produtos_com_estado, fornecedores=fornecedores, lotes=lotes, produto_id=produto_id)