// https://www.howtocodeschool.com/2021/12/price-range-slider-with-html-css-javascript.html
const minSlider = document.getElementById("min");
const maxSlider = document.getElementById("max");

const outputMin = document.getElementById("min-value");
const outputMax = document.getElementById("max-value");

outputMin.innerHTML = minSlider.value;
outputMax.innerHTML = maxSlider.value;

minSlider.oninput = function () {
  outputMin.innerHTML = this.value;
};

maxSlider.oninput = function () {
  outputMax.innerHTML = this.value;
};

function submitForm() {
  document.getElementById("sort-by-form").submit();
}
