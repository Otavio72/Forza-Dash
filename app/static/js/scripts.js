/*!
* Start Bootstrap - Grayscale v7.0.6 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*/
// -----------------------------------------------------------------------------
// Script padrão do template "Grayscale" do Bootstrap
// Ele cuida basicamente da parte de navegação responsiva (menu em mobile)
// -----------------------------------------------------------------------------

// Quando o conteúdo da página for completamente carregado (HTML pronto)
window.addEventListener('DOMContentLoaded', event => {

    // Pega o botão que abre/fecha o menu (aquele "hambúrguer")
    const navbarToggler = document.body.querySelector('.navbar-toggler');

    // Pega todos os links dentro do menu de navegação (parte colapsável)
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );

    // Para cada link encontrado no menu responsivo...
    responsiveNavItems.map(function (responsiveNavItem) {
        // Adiciona um evento de clique
        responsiveNavItem.addEventListener('click', () => {
            // Se o botão do menu estiver visível (modo mobile)
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                // Simula um clique no botão — isso fecha o menu automaticamente
                navbarToggler.click();
            }
        });
    });

});
