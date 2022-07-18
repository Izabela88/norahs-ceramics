// Control active class

function controlActiveClass() {
  let currentLocation = window.location.href;
  let menuItem = document.querySelectorAll("#menu-list li a");
  let menuLength = menuItem.length;

  for (let i = 0; i < menuLength; i++) {
    if (menuItem[i].href === currentLocation) {
      menuItem[i].classList.add("active");
      console.log(currentLocation);
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

// show/hide password
function showPassword(elemendId) {
  let passwordInput = document.getElementById(elemendId);
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
  } else {
    passwordInput.type = "password";
  }
}

const box_one = document.getElementById("show_password_one");
if (box_one) {
  box_one.addEventListener("click", function () {
    showPassword("id_password1");
  });
}

const box_two = document.getElementById("show_password_two");
if (box_two) {
  box_two.addEventListener("click", function () {
    showPassword("id_password2");
  });
}

const box_three = document.getElementById("show_password_login");
if (box_three) {
  box_three.addEventListener("click", function () {
    showPassword("id_password");
  });
}

/* After pressing sidebar links and scrolling to a given section,
      the sidebar closes automatically*/
for (const button of closeButtons) {
  let wrapperMenu = document.querySelector(".wrapper-menu");
  button.addEventListener("click", function (e) {
    if (window.innerWidth < 1150) {
      wrapperMenu.classList.toggle("open");
      openMenu();
    }
  });
}
