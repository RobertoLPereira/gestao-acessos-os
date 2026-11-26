export const UI = {
    renderizarArvoreMenus(sistemas, container, onAbrirTransacao) {
        container.innerHTML = "";

        if (!sistemas || sistemas.length === 0) {
            const p = document.createElement("p");
            p.className = "empty-msg";
            p.textContent = "Nenhum acesso ativo encontrado para este usuário.";
            container.appendChild(p);
            return;
        }

        sistemas.forEach((sistema) => {
            const detailsSis = document.createElement("details");
            detailsSis.className = "sistema-item";

            const summarySis = document.createElement("summary");
            summarySis.textContent = sistema.nome;
            detailsSis.appendChild(summarySis);

            sistema.menus.forEach((menu) => {
                const detailsMod = document.createElement("details");
                detailsMod.className = "modulo-item";

                const summaryMod = document.createElement("summary");
                summaryMod.textContent = menu.nome;
                detailsMod.appendChild(summaryMod);

                const ul = document.createElement("ul");
                ul.className = "transacao-list";

                menu.transacoes.forEach((transacao) => {
                    const li = document.createElement("li");
                    const btn = document.createElement("button");
                    btn.type = "button";
                    btn.className = "transacao-btn";
                    btn.textContent = transacao.nome;

                    if (transacao.subtransacoes && transacao.subtransacoes.length > 0) {
                        const span = document.createElement("span");
                        span.className = "subtransacao-tag";
                        span.textContent = `(${transacao.subtransacoes.map(s => s.nome).join(", ")})`;
                        btn.appendChild(span);
                    }

                    btn.addEventListener("click", () => onAbrirTransacao(sistema, transacao));
                    li.appendChild(btn);
                    ul.appendChild(li);
                });

                detailsMod.appendChild(ul);
                detailsSis.appendChild(detailsMod);
            });

            container.appendChild(detailsSis);
        });
    },

    renderizarOsPendentes(ordens, container, onAceitar) {
        container.innerHTML = "";
        if (!ordens || ordens.length === 0) {
            container.classList.add("hidden");
            return;
        }

        container.classList.remove("hidden");
        const titulo = document.createElement("strong");
        titulo.textContent = `Você possui ${ordens.length} Ordem(ns) de Serviço aguardando ciência:`;
        container.appendChild(titulo);

        ordens.forEach((os) => {
            const card = document.createElement("div");
            card.className = "os-card";

            const info = document.createElement("div");
            info.innerHTML = `<strong>OS #${os.idordemservico}</strong> (Válida até ${os.datafimvalidade})<br><small>${os.corpo || ""}</small>`;

            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "btn-aceitar";
            btn.textContent = "Dar Ciência";
            btn.addEventListener("click", () => onAceitar(os.idordemservicociencia));

            card.appendChild(info);
            card.appendChild(btn);
            container.appendChild(card);
        });
    },

    abrirTransacao(workspace, tituloEl, sistema, transacao) {
        tituloEl.textContent = `${sistema.nome} › ${transacao.nome}`;
        workspace.innerHTML = "";

        const urlDestino = transacao.url || `/${transacao.nome.replace(/\s+/g, "")}`;

        const card = document.createElement("div");
        card.className = "welcome-card";
        card.innerHTML = `
            <h3>${transacao.nome}</h3>
            <p style="margin: 0.75rem 0; color: #64748b;">Rota configurada no banco: <code>${urlDestino}</code></p>
            <p>Sistema: <strong>${sistema.nome}</strong> (${sistema.sigla || ""})</p>
        `;
        workspace.appendChild(card);
    }
};
