"use strict";

const temaDoSistema = window.matchMedia("(prefers-color-scheme: dark)");
const raiz = document.documentElement;
const botaoTema = document.querySelector("[data-theme-toggle]");
const chaveTema = "manager-school-theme";

function temaAtivo() {
    return raiz.dataset.theme || (temaDoSistema.matches ? "dark" : "light");
}

function atualizarGraficos(tema) {
    document.querySelectorAll("[data-theme-chart]").forEach((imagem) => {
        const endereco = new URL(imagem.src, window.location.href);
        endereco.searchParams.set("theme", tema);
        imagem.src = endereco.toString();
    });
}

function atualizarBotaoTema() {
    if (!botaoTema) return;
    const tema = temaAtivo();
    botaoTema.textContent = tema === "dark" ? "Tema claro" : "Tema escuro";
    botaoTema.setAttribute("aria-label", `Ativar tema ${tema === "dark" ? "claro" : "escuro"}`);
    botaoTema.setAttribute("aria-pressed", String(raiz.dataset.theme !== undefined));
}

const temaSalvo = window.localStorage.getItem(chaveTema);
if (temaSalvo === "light" || temaSalvo === "dark") {
    raiz.dataset.theme = temaSalvo;
}

if (botaoTema) {
    botaoTema.hidden = false;
    atualizarBotaoTema();
    botaoTema.addEventListener("click", () => {
        const novoTema = temaAtivo() === "dark" ? "light" : "dark";
        raiz.dataset.theme = novoTema;
        window.localStorage.setItem(chaveTema, novoTema);
        atualizarBotaoTema();
        atualizarGraficos(novoTema);
    });
}

const acompanharSistema = (evento) => {
    if (raiz.dataset.theme === undefined) {
        atualizarBotaoTema();
        atualizarGraficos(evento.matches ? "dark" : "light");
    }
};
if (temaDoSistema.addEventListener) {
    temaDoSistema.addEventListener("change", acompanharSistema);
} else if (temaDoSistema.addListener) {
    temaDoSistema.addListener(acompanharSistema);
}
atualizarGraficos(temaAtivo());

const seletorAluno = document.querySelector("[data-student-select]");
const camposNovoAluno = document.querySelector("[data-new-student-fields]");
const seletorTurmaRelatorio = document.querySelector("[data-class-select]");
const seletorAlunoRelatorio = document.querySelector("#report-student");

// Ao mudar de turma, limpa um aluno que pode pertencer à turma anterior.
if (seletorTurmaRelatorio && seletorAlunoRelatorio) {
    seletorTurmaRelatorio.addEventListener("change", () => {
        seletorAlunoRelatorio.value = "";
        seletorTurmaRelatorio.form?.requestSubmit();
    });
}

function atualizarCamposNovoAluno() {
    if (!seletorAluno || !camposNovoAluno) return;
    const cadastrarNovo = seletorAluno.value === "novo";
    camposNovoAluno.hidden = !cadastrarNovo;
    camposNovoAluno.querySelectorAll("input").forEach((campo) => {
        campo.required = cadastrarNovo;
    });
}

if (seletorAluno) {
    seletorAluno.addEventListener("change", atualizarCamposNovoAluno);
    atualizarCamposNovoAluno();
}

document.querySelectorAll("form[data-loading-form]").forEach((formulario) => {
    formulario.addEventListener("submit", (evento) => {
        const confirmacao = formulario.dataset.confirm;
        if (confirmacao && !window.confirm(confirmacao)) {
            evento.preventDefault();
            return;
        }

        const botao = evento.submitter || formulario.querySelector("button[type='submit']");
        if (!botao) return;
        botao.disabled = true;
        botao.classList.add("is-loading");
        botao.setAttribute("aria-busy", "true");
        if (botao.dataset.loadingLabel) {
            botao.textContent = botao.dataset.loadingLabel;
        }
    });
});
