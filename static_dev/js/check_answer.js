document.addEventListener('DOMContentLoaded', function () {
  const forms = document.querySelectorAll('.answer-form');

  function showMessage(container, html) {
    container.innerHTML = '';
    void container.offsetWidth; // перезапуск анимации
    container.innerHTML = html;

    const alertBox = container.querySelector('.alert');
    if (alertBox) {
      alertBox.classList.remove('flash-animation');
      void alertBox.offsetWidth;
      alertBox.classList.add('flash-animation');
    }
  }

  forms.forEach((form) => {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      const messageDiv = this.nextElementSibling;

      // --- Текстовая задача ---
      const input = this.querySelector('input[type="text"][name="answer"]');
      if (input !== null) {
        const userAnswer = (input.value || "").trim();
        const correctAnswer = (this.dataset.correctAnswer || "").trim();

        if (!userAnswer) {
          showMessage(messageDiv, '<div class="alert alert-warning">⚠️ Введите ответ.</div>');
          return;
        }

        if (userAnswer === correctAnswer) {
          showMessage(messageDiv, '<div class="alert alert-success">ВЕРНО</div>');
        } else {
          showMessage(messageDiv, '<div class="alert alert-danger">НЕВЕРНО</div>');
        }

        this.reset();
        return;
      }

      // --- Match-задача ---
      const selects = this.querySelectorAll('select.answer-select');
      if (selects.length > 0) {
        let allSelected = true;
        let allCorrect = true;

        selects.forEach((select) => {
          const correctAnswerId = select.dataset.correctAnswerId || "";
          const selectedAnswerId = select.value || "";

          if (!selectedAnswerId) {
            allSelected = false;
          } else if (selectedAnswerId !== correctAnswerId) {
            allCorrect = false;
          }
        });

        if (!allSelected) {
          showMessage(messageDiv, '<div class="alert alert-warning">⚠️ Выберите все варианты.</div>');
          return;
        }

        if (allCorrect) {
          showMessage(messageDiv, '<div class="alert alert-success">ВЕРНО</div>');
        } else {
          showMessage(messageDiv, '<div class="alert alert-danger">НЕВЕРНО</div>');
        }

        return;
      }

      // --- Если форма неизвестная ---
      console.warn("⚠️ Неизвестный тип формы!", this);
      showMessage(messageDiv, '<div class="alert alert-warning">⚠️ Неизвестный тип формы.</div>');
    });
  });
});
