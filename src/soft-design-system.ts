// initialization of Popovers
let popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
let popoverList: any;

// initialization of Tooltips
let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
let tooltipList: any;

// helper for adding on all elements multiple attributes
function setAttributes(el: { setAttribute: (arg0: string, arg1: any) => void; }, options: { [x: string]: any; }) {
  Object.keys(options).forEach(function(attr) {
    el.setAttribute(attr, options[attr]);
  })
}

// activate popovers
popoverTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="popover"]'));
popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  // @ts-ignore
  return new bootstrap.Popover(popoverTriggerEl)
});

// activate tooltips
tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  // @ts-ignore
  return new bootstrap.Tooltip(tooltipTriggerEl)
});

// Copy code function

function copyCode(el: { nextElementSibling: any; parentElement: { querySelector: (arg0: string) => { (): any; new(): any; remove: { (): void; new(): any; }; }; appendChild: (arg0: HTMLDivElement) => void; }; }) {
  const selection = window.getSelection();
  const range = document.createRange();
  const textToCopy = el.nextElementSibling;
  range.selectNodeContents(textToCopy);
  selection!.removeAllRanges();
  selection!.addRange(range);
  document.execCommand('copy');
  window.getSelection()!.removeAllRanges()
  if (!el.parentElement.querySelector('.alert')) {
    const alert = document.createElement('div');
    alert.classList.add('alert', 'alert-success', 'position-absolute', 'top-0', 'border-0', 'text-white', 'w-25', 'end-0', 'start-0', 'mt-2', 'mx-auto', 'py-2');
    alert.style.transform = 'translate3d(0px, 0px, 0px)'
    alert.style.opacity = '0';
    alert.style.transition = '.35s ease';
    setTimeout(function() {
      alert.style.transform = 'translate3d(0px, 20px, 0px)';
      alert.style.setProperty("opacity", "1", "important");
    }, 100);
    alert.innerHTML = "Code successfully copied!";
    el.parentElement.appendChild(alert);
    setTimeout(function() {
      alert.style.transform = 'translate3d(0px, 0px, 0px)'
      alert.style.setProperty("opacity", "0", "important");
    }, 2000);
    setTimeout(function() {
      el.parentElement.querySelector('.alert').remove();
    }, 2500);
  }
}
