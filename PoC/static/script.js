const text = document.querySelector('.get-table');
const container = document.querySelector('.exchange');
const currentPrice = document.querySelector('.price').innerHTML.slice(0, -1);
const exchangeInput = document.querySelector('.curr-price');
const outputContainer = document.querySelector('.exchange-output');

window.addEventListener('load', (e) => {
  table = `${text.textContent}`;
  text.remove();
  container.insertAdjacentHTML('afterbegin', table);
});

exchangeInput.addEventListener('input', (e) => {
  let exchange = exchangeInput.value * parseFloat(currentPrice);
  outputContainer.innerHTML = exchange.toFixed(2);
});
