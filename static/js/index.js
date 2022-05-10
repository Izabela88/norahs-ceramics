// Control active class

function controlActiveClass() {
  let currentLocation = window.location.href;
  let menuItem = document.querySelectorAll("#menu-list li a");
  let menuLength = menuItem.length;

  for (let i = 0; i < menuLength; i++) {
    if (menuItem[i].href === currentLocation) {
      menuItem[i].classList.add("active");
    } else {
      menuItem[i].classList.remove("active");
    }
  }
}

controlActiveClass();
