export const ApiClient = {
    async buscarMenus(usuario) {
        const resp = await fetch(`/api/menus?usuario=${encodeURIComponent(usuario)}`);
        const dados = await resp.json();
        if (!resp.ok) throw new Error(dados.erro || "Erro ao buscar menus.");
        return dados;
    },

    async buscarOsPendentes(usuario) {
        const resp = await fetch(`/api/os/pendentes?usuario=${encodeURIComponent(usuario)}`);
        const dados = await resp.json();
        if (!resp.ok) throw new Error(dados.erro || "Erro ao buscar Ordens de Serviço.");
        return dados;
    },

    async registrarCiencia(idordemservicociencia, usuario) {
        const resp = await fetch("/api/os/ciencia", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ idordemservicociencia, usuario })
        });
        const dados = await resp.json();
        if (!resp.ok) throw new Error(dados.erro || "Erro ao confirmar ciência.");
        return dados;
    }
};
