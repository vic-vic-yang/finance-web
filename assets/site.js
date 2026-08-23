const modal = document.querySelector('#download-modal');
const openButtons = document.querySelectorAll('.download-open');
const closeButtons = modal?.querySelectorAll('[data-close]') ?? [];

function setModal(open) {
  if (!modal) return;
  modal.classList.toggle('open', open);
  modal.setAttribute('aria-hidden', String(!open));
  document.body.classList.toggle('modal-open', open);
  if (open) modal.querySelector('.modal-close').focus();
}

openButtons.forEach((button) => button.addEventListener('click', () => setModal(true)));
closeButtons.forEach((button) => button.addEventListener('click', () => setModal(false)));
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && modal?.classList.contains('open')) setModal(false);
});

const wechatContacts = document.querySelectorAll('.wechat-contact');
const wechatIcon = `
  <svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20">
    <path fill="currentColor" d="M9.45 3.5C5.35 3.5 2 6.22 2 9.58c0 1.9 1.08 3.62 2.82 4.73l-.68 2.05 2.42-1.2c.9.31 1.87.5 2.89.5.35 0 .7-.03 1.03-.07a5.52 5.52 0 0 1-.2-1.45c0-3.22 2.93-5.84 6.55-5.84h.06C16.17 5.56 13.16 3.5 9.45 3.5Zm-2.5 3.14a.94.94 0 1 1 0 1.88.94.94 0 0 1 0-1.88Zm5 0a.94.94 0 1 1 0 1.88.94.94 0 0 1 0-1.88Z"/>
    <path fill="currentColor" d="M22 14.14c0-2.72-2.32-4.92-5.17-4.92s-5.17 2.2-5.17 4.92 2.32 4.92 5.17 4.92c.72 0 1.4-.14 2.02-.39l1.86.94-.5-1.62C21.3 17.1 22 15.69 22 14.14Zm-6.92-1.3a.78.78 0 1 1 0 1.56.78.78 0 0 1 0-1.56Zm3.5 0a.78.78 0 1 1 0 1.56.78.78 0 0 1 0-1.56Z"/>
  </svg>`;

wechatContacts.forEach((contact) => {
  const toggle = contact.querySelector('.wechat-toggle');
  const qrImage = contact.querySelector('.wechat-popover img');
  toggle.innerHTML = wechatIcon;
  if (qrImage) qrImage.src = '/assets/wechat-vic-qr.png';
  toggle.addEventListener('click', (event) => {
    event.stopPropagation();
    const open = !contact.classList.contains('open');
    wechatContacts.forEach((item) => {
      item.classList.remove('open');
      item.querySelector('.wechat-toggle').setAttribute('aria-expanded', 'false');
    });
    contact.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
  });
});

document.addEventListener('click', () => {
  wechatContacts.forEach((contact) => {
    contact.classList.remove('open');
    contact.querySelector('.wechat-toggle').setAttribute('aria-expanded', 'false');
  });
});
