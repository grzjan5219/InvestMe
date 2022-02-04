const headerBtn = document.querySelector('.header-btn');
const cryptoSection = document.querySelector('.crypto-section');

headerBtn.addEventListener('click', (e) => {
  console.log(e);
  const s1coords = cryptoSection.getBoundingClientRect();

  console.log(s1coords);

  cryptoSection.scrollIntoView({ behavior: 'smooth' });
});
