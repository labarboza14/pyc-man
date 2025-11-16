````markdown
# PYc-Man — Pac-Man (Esquenta Hackathon Python Floripa / IFSC)

> Comentário (cole no início do `pacman.py` se quiser):  
> `# Esquenta para Hackathon Python Floripa / IFSC — vamos testar lógica, requisitos e clima retrô. Todo mundo conhece Pac-Man — sabia que dá pra fazer com Python? Dá pra fazer também em outras linguagens (JavaScript, Java, C#, etc). Esse projeto é um exercício prático para juniors.`

---

## Sumário
- [O que é este projeto](#o-que-é-este-projeto)  
- [Para quem é](#para-quem-é)  
- [Pré-requisitos](#pré-requisitos)  
- [Instalação e execução (passo a passo)](#instalação-e-execução-passo-a-passo)  
- [Como o código está organizado](#como-o-código-está-organizado)  
- [Tecnologias e por que foram usadas](#tecnologias-e-por-que-foram-usadas)  
- [Como o jogo funciona (visão de alto nível)](#como-o-jogo-funciona-visão-de-alto-nível)  
- [Principais trechos de código e o que fazem](#principais-trechos-de-código-e-o-que-fazem)  
- [Dicas para debugar problemas comuns](#dicas-para-debugar-problemas-comuns)  
- [Sugestões de melhorias (ótimas para o hackathon)](#sugestões-de-melhorias-ótimas-para-o-hackathon)  
- [Como contribuir / entregar no hackathon](#como-contribuir--entregar-no-hackathon)  
- [Licença e créditos](#licença-e-créditos)

---

## O que é este projeto
**PYc-Man** é uma implementação simples e retrô de Pac-Man feita em Python usando **Pygame**.  
O objetivo principal é **praticar pensamento computacional, lógica de jogo, estruturas de dados simples (matrizes/mapas), e integração com bibliotecas externas** — tudo em preparação para o Hackathon Python Floripa / IFSC.

---

## Para quem é
- Pessoas iniciando em Python (juniors) que querem um projeto prático.  
- Times procurando um *esquenta* rápido antes do hackathon.  
- Quem quer entender como transformar regras de negócio (movimento, colisão, IA simples) em código.

---

## Pré-requisitos
- Windows / macOS / Linux com Python 3.8+ instalado.  
- Acesso ao terminal (PowerShell, Terminal ou similar).  
- Recomendo um editor de código (VS Code, PyCharm, etc).

### Pacotes Python necessários
- `pygame`

Instale com:

```bash
python -m pip install pygame
````

> Se der erro no `pip`, experimente `python -m ensurepip --upgrade` ou verifique o `python --version` para garantir que está usando a versão correta do Python.

---

## Instalação e execução (passo a passo)

1. **Clone o repositório** (ou faça download do ZIP):

```bash
git clone https://github.com/labarboza14/pyc-man.git
cd pyc-man
```

2. **Crie um ambiente virtual (opcional, mas recomendado)**

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

3. **Instale dependências**

```bash
python -m pip install --upgrade pip
python -m pip install pygame
```

4. **Rode o jogo**

```bash
python pacman.py
```

* Na tela inicial, pressione **ENTER**.
* Segure as setas para mover (Opção B — movimento contínuo).
* Objetivo: comer todas as bolinhas (pellets).
* Ao vencer, aparece a tela "VOCÊ VENCEU!".
* Ao perder todas as vidas, aparece a tela "GAME OVER".

---

## Como o código está organizado

* `pacman.py` — arquivo principal contendo tudo: mapa, lógica, sprites simples, loop do jogo.
* `README.md` — este documento.
* `ranking.txt` — gerado pelo jogo (se a versão incluir ranking).
* (opcional) `assets/` — ícones, sons (se você adicionar).

> Mantivemos o projeto num único arquivo `.py` para facilitar o entendimento e o deploy rápido. Em projetos maiores vale separar em módulos.

---

## Tecnologias e por que foram usadas

* **Python 3** — linguagem popular, ótima para ensino e prototipagem rápida.
* **Pygame** — biblioteca madura para 2D em Python; permite abrir janelas, desenhar formas, capturar teclado, tocar som.
* **Git / GitHub** — versionamento e hospedagem do código; excelente para colaboração no hackathon e pra entregar projeto.

Por que essas escolhas:

* Ferramentas simples para aprender conceitos de jogos (movimento, colisão, IA básica) sem overhead de frameworks complexos.
* Fácil de rodar em laptops comuns dos participantes.

---

## Como o jogo funciona (visão de alto nível)

1. **Mapa**: uma matriz (lista de listas) onde `1 = parede` e `0 = caminho`. Cada célula é um tile quadrado (TILE px).
2. **Pellets**: set de coordenadas que representam bolinhas para comer.
3. **Pac-Man**: sprite circular que se move enquanto a tecla é pressionada; colisões são checadas pelos cantos do círculo.
4. **Fantasma**: IA simples (BFS) que recalcula rota a cada 1s e segue poucos passos (modo F4, propositalmente “menos esperto”).
5. **HUD**: exibe pontos, vidas e tempo.
6. **Condições**: ganha ao comer todos os pellets; perde quando acaba as vidas.

---

## Principais trechos de código e o que fazem (para juniors lerem)

* **Mapa (matrix)** — define onde Pac-Man pode andar. Entender isso é essencial: é só uma grade.
* **Função `point_is_wall(px, py)`** — converte pixel → tile e responde se há parede. Usada em todas checagens de colisão.
* **Classe `Pacman`**

  * `move(dx, dy)`: tenta mover em pixels, checando colisões nos quatro cantos do círculo.
  * `tile()`: retorna a tile atual (útil para comer pellets).
* **Classe `RedGhost`**

  * `bfs(start, goal)`: busca em largura para achar um caminho simples entre tiles (BFS é fácil, determinístico e suficiente).
  * `update(pac_pos)`: recalcula a cada 1s e segue passos curtos (isso evita perseguição perfeita).
* **Loop principal**

  * Lê o teclado (`pygame.key.get_pressed()`), move Pac-Man, atualiza ghost, checa colisões, desenha tudo.

---

## Dicas para debugar problemas comuns (juniors)

* **Janela fecha imediatamente**: sign of script finishing. Verifique se falta o loop principal ou se há `sys.exit()` antes. Rode pelo terminal e leia mensagens de erro.
* **Pygame não instalado**: instale com `python -m pip install pygame`. Confira `python --version`.
* **Pac-Man preso em corredores**: ajuste `radius` e a lógica de colisão (já tratada na versão atual).
* **Erro `no module named pygame`**: seu `pip` pode estar instalando em outro Python. Use `python -m pip install pygame` para garantir.


---

## Licença e créditos

Sinta-se livre para usar e modificar o código para aprender e compartilhar. Recomendo adicionar uma licença permissiva ao repositório, por exemplo **MIT License**.
