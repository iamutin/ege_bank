document.addEventListener('DOMContentLoaded', function () {
  const matchForms = document.querySelectorAll('.match-form');

  function showMessage(container, html) {
    container.innerHTML = '';
    void container.offsetWidth;
    container.innerHTML = html;

    const alertBox = container.querySelector('.alert');
    if (alertBox) {
      alertBox.classList.remove('flash-animation');
      void alertBox.offsetWidth;
      alertBox.classList.add('flash-animation');
    }
  }

  matchForms.forEach((form) => {
    form.addEventListener('submit', function (event) {
      event.preventDefault();

      const dropdowns = form.querySelectorAll('.custom-dropdown');
      let allCorrect = true;
      let allSelected = true;

      dropdowns.forEach((dropdown) => {
        const correctAnswerId = dropdown.dataset.correctAnswerId;
        const button = dropdown.querySelector('button.dropdown-toggle');
        const selectedAnswerId = button.dataset.selectedAnswerId;

        if (!selectedAnswerId) {
          allSelected = false;
          return;
        }

        if (String(selectedAnswerId) !== String(correctAnswerId)) {
          allCorrect = false;
        }
      });

      const messageDiv = form.nextElementSibling;

      if (!allSelected) {
        showMessage(messageDiv, '<div class="alert alert-warning">⚠️ Пожалуйста, выберите варианты для всех соответствий.</div>');
        return;
      }

      if (allCorrect) {
        showMessage(messageDiv, '<div class="alert alert-success">ВЕРНО</div>');
      } else {
        showMessage(messageDiv, '<div class="alert alert-danger">НЕВЕРНО</div>');
      }
    });
  });
});
