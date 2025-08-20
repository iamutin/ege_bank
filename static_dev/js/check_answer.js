document.addEventListener('DOMContentLoaded', function () {
  const forms = document.querySelectorAll('.answer-form');

  function showMessage(container, html) {
    container.innerHTML = '';
    void container.offsetWidth; // перезапуск анимации
    container.innerHTML = html;

    const alertBox = container.querySelector('.alert');
    if (alertBox) {
      alertBox.classList.remove('flash-animation');
      void alertBox.offsetWidth; // форсируем перерисовку
      alertBox.classList.add('flash-animation');
    }
  }

  forms.forEach((form) => {
    form.addEventListener('submit', function (event) {
      event.preventDefault();

      const resultContainer = this.nextElementSibling;
      let isCorrect = true;

      // --- Проверка задачи на соответствие ---
      const selects = this.querySelectorAll('select.answer-select');
      if (selects.length > 0) {
        selects.forEach((select) => {
          const userAnswer = select.value;
          const correctAnswerId = select.dataset.correctAnswerId;
          if (userAnswer !== correctAnswerId) {
            isCorrect = false;
          }
        });
      }

      // --- Проверка задачи с текстовым ответом ---
      const input = this.querySelector('input[name="answer"]');
      if (input) {
        const userAnswer = input.value.trim().toLowerCase();
        const correctAnswer = this.dataset.correctAnswer.trim().toLowerCase();
        if (userAnswer !== correctAnswer) {
          isCorrect = false;
        }
        this.reset();
      }

      // --- Вывод результата с анимацией ---
      if (isCorrect) {
        showMessage(resultContainer, '<div class="alert alert-success">ВЕРНО</div>');
      } else {
        showMessage(resultContainer, '<div class="alert alert-danger">НЕВЕРНО</div>');
      }
    });
  });
});
