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

// Code from https://codepen.io/JoseRosario/pen/BWqMwK*
function toggleHamburgerIcon() {
  let wrapperMenu = document.querySelector(".wrapper-menu");

  wrapperMenu.addEventListener("click", function () {
    console.log("click");
    wrapperMenu.classList.toggle("open");
  });
}

toggleHamburgerIcon();

/* My code starts here
        Open and close sidebar for small devices*/
const hamburgerIcon = document.querySelector(".wrapper-menu");
const closeButtons = document.querySelectorAll(".close-sidebar");

function openMenu() {
  document.getElementById("my-sidebar").classList.toggle("open-menu");
}

hamburgerIcon.addEventListener("click", function (e) {
  openMenu();
});
