document.addEventListener('DOMContentLoaded', function () {
  const dropdowns = document.querySelectorAll('.custom-dropdown');

  dropdowns.forEach(dropdown => {
    const button = dropdown.querySelector('button.dropdown-toggle');
    const menu = dropdown.querySelector('ul.dropdown-menu');

    button.addEventListener('click', (e) => {
      e.stopPropagation();
      closeAllDropdowns();
      menu.classList.toggle('show');
    });

    menu.querySelectorAll('li').forEach(item => {
      item.addEventListener('click', () => {
        button.innerHTML = item.innerHTML;
        button.dataset.selectedAnswerId = item.dataset.value;
        menu.classList.remove('show');

        if (window.MathJax) {
          MathJax.typesetPromise();
        }
      });
    });

    document.addEventListener('click', () => {
      menu.classList.remove('show');
    });
  });

  function closeAllDropdowns() {
    document.querySelectorAll('.custom-dropdown .dropdown-menu').forEach(menu => {
      menu.classList.remove('show');
    });
  }
});
