import { ApiClient } from "./api.js";
import { UI } from "./ui.js";

const inputUsuario = document.getElementById("input-usuario");
const btnCarregar = document.getElementById("btn-carregar");
const menuContainer = document.getElementById("menu-container");
const osContainer = document.getElementById("os-pendentes-container");
const workspace = document.getElementById("workspace");
const tituloPagina = document.getElementById("titulo-pagina");
const sidebar = document.getElementById("sidebar");
const btnToggleMenu = document.getElementById("btn-toggle-menu");
const statusRede = document.getElementById("status-rede");

async function carregarDadosUsuario() {
    const usuario = inputUsuario.value.trim();
    if (!usuario) return;

    menuContainer.innerHTML = `<p class="empty-msg">Carregando permissões...</p>`;

    try {
        const [menus, pendentes] = await Promise.all([
            ApiClient.buscarMenus(usuario),
            ApiClient.buscarOsPendentes(usuario)
        ]);

        UI.renderizarArvoreMenus(menus, menuContainer, (sistema, transacao) => {
            UI.abrirTransacao(workspace, tituloPagina, sistema, transacao);
            sidebar.classList.remove("open");
        });

        UI.renderizarOsPendentes(pendentes, osContainer, async (idCiencia) => {
            await ApiClient.registrarCiencia(idCiencia, usuario);
            await carregarDadosUsuario(); // Recarrega menus imediatamente após o aceite
        });
    } catch (erro) {
        menuContainer.innerHTML = `<p class="empty-msg" style="color:#fca5a5;">${erro.message}</p>`;
    }
}

btnCarregar.addEventListener("click", carregarDadosUsuario);
inputUsuario.addEventListener("keypress", (e) => {
    if (e.key === "Enter") carregarDadosUsuario();
});
btnToggleMenu.addEventListener("click", () => sidebar.classList.toggle("open"));

// Monitoramento de conexão (Online/Offline)
window.addEventListener("online", () => {
    statusRede.textContent = "Online";
    statusRede.className = "badge badge-online";
});
window.addEventListener("offline", () => {
    statusRede.textContent = "Offline";
    statusRede.className = "badge badge-offline";
});

// Registro do Service Worker para transformar em PWA instalável
if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
        navigator.serviceWorker.register("/sw.js").catch((err) => {
            console.warn("Falha ao registrar Service Worker:", err);
        });
    });
}

// Carga inicial
carregarDadosUsuario();
