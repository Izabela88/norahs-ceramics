// https://codepen.io/im1tta/pen/QGmYmN
// multistep form
var msf_getFsTag = document.getElementsByTagName("fieldset");

// declaring the active fieldset & the total fieldset count
var msf_form_nr = 0;
var fieldset = msf_getFsTag[msf_form_nr];
fieldset.className = "msf_show";

// creates and stores a number of bullets
var msf_bullet_nr = "<div class='msf_bullet'></div>";
var msf_length = msf_getFsTag.length;
for (var i = 1; i < msf_length; ++i) {
  msf_bullet_nr += "<div class='msf_bullet'></div>";
}
// injects bullets
var msf_bullet_o = document.getElementsByClassName("msf_bullet_o");
for (var i = 0; i < msf_bullet_o.length; ++i) {
  var msf_b_item = msf_bullet_o[i];
  msf_b_item.innerHTML = msf_bullet_nr;
}

// removes the first back button & the last next button
document.getElementsByName("back")[0].className = "msf_hide";
document.getElementsByName("next")[msf_bullet_o.length - 1].className =
  "msf_hide";

// Makes the first dot active
var msf_bullets = document.getElementsByClassName("msf_bullet");
msf_bullets[msf_form_nr].className += " msf_bullet_active";

// Validation loop & goes to the next step
function msf_btn_next() {
  var msf_val = true;

  var msf_fs = document.querySelectorAll("fieldset")[msf_form_nr];
  var msf_fs_i_count = msf_fs.querySelectorAll("input").length;

  for (i = 0; i < msf_fs_i_count; ++i) {
    var msf_input_s = msf_fs.querySelectorAll("input")[i];
    if (msf_input_s.getAttribute("type") === "button") {
      // nothing happens
    } else {
      if (msf_input_s.value === "") {
        msf_input_s.style.border = "1px solid red";
        msf_val = false;
      } else {
        if (msf_val === false) {
        } else {
          msf_val = true;
          msf_input_s.style.border = "1px solid #9cebbf";
        }
      }
    }
  }
  if (msf_val === true) {
    // goes to the next step
    var selection = msf_getFsTag[msf_form_nr];
    selection.className = "msf_hide";
    msf_form_nr = msf_form_nr + 1;
    var selection = msf_getFsTag[msf_form_nr];
    selection.className = "msf_show";
    // refreshes the bullet
    var msf_bullets_a = msf_form_nr * msf_length + msf_form_nr;
    msf_bullets[msf_bullets_a].className += " msf_bullet_active";
  }
}

// goes one step back
function msf_btn_back() {
  msf_getFsTag[msf_form_nr].className = "msf_hide";
  msf_form_nr = msf_form_nr - 1;
  msf_getFsTag[msf_form_nr].className = "msf_showhide";
}

// https://stackoverflow.com/questions/16262155/shipping-address-same-as-billing

function sameAddressess() {
  const checkBox = document.getElementById("myCheck");
  const shipAdd = document.getElementById("address-ship");
  const shipAddTwo = document.getElementById("address-ship-two");
  const codeShip = document.getElementById("code-ship");
  const townShip = document.getElementById("town-ship");
  const countyShip = document.getElementById("county-ship");
  const countryShip = document.getElementById("country-ship");
  const billingAdd = document.getElementById("address-billing");
  const billingAddTwo = document.getElementById("address-billing-two");
  const codeBilling = document.getElementById("code-billing");
  const townBilling = document.getElementById("town-billing");
  const countyBilling = document.getElementById("county-billing");
  const countryBilling = document.getElementById("country-billing");
  if (checkBox.checked == true) {
    billingAdd.value = shipAdd.value;
    billingAddTwo.value = shipAddTwo.value;
    codeBilling.value = codeShip.value;
    townBilling.value = townShip.value;
    countyBilling.value = countyShip.value;
    countryBilling.value = countryShip.value;
  } else {
    billingAdd.value = "";
    billingAddTwo.value = "";
    codeBilling.value = "";
    townBilling.value = "";
    countyBilling.value = "";
    countryBilling.value = "";
  }
}

// Get Stripe publishable key
fetch("/checkout/config/")
  .then((result) => {
    return result.json();
  })
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // new
    // Event handler
    document.querySelector("#submitBtn").addEventListener("click", () => {
      // Get Checkout Session ID
      fetch("/checkout/create-checkout-session/")
        .then((result) => {
          return result.json();
        })
        .then((data) => {
          console.log(data);
          // Redirect to Stripe Checkout
          return stripe.redirectToCheckout({ sessionId: data.sessionId });
        })
        .then((res) => {
          console.log(res);
        });
    });
  });
