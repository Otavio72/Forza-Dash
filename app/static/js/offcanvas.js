(function () {
  'use strict' // Ativa o modo estrito do JavaScript (ajuda a evitar erros bestas)

  // Seleciona o botão que controla o menu lateral (aquele que abre/fecha)
  document.querySelector('#navbarSideCollapse').addEventListener('click', function () {
    // Quando o botão for clicado, alterna a classe "open" no menu lateral
    // Isso faz o menu aparecer ou desaparecer (efeito de "offcanvas")
    document.querySelector('.offcanvas-collapse').classList.toggle('open')
  })
})()

