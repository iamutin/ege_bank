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

      const input = this.querySelector('input[type="text"][name="answer"]');
      const userAnswer = input.value;
      const correctAnswer = this.dataset.correctAnswer;
      const messageDiv = this.nextElementSibling;

      if (userAnswer === correctAnswer) {
        showMessage(messageDiv, '<div class="alert alert-success">ВЕРНО</div>');
      } else {
        showMessage(messageDiv, '<div class="alert alert-danger">НЕВЕРНО</div>');
      }

      this.reset();
    });
  });
});
