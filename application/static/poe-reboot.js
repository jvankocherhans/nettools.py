var process_bar = document.getElementById("process_bar");
var main = body.querySelector(".main")
var process_bar_toggle = body.querySelector(".process_bar_toggle");
var isOpen = false;

process_bar_toggle.addEventListener("click", function () {
  if (isOpen) {
    process_bar.classList.remove("open");
    main.classList.remove("close")
    isOpen = false;
  } else {
    process_bar.classList.add("open");
    main.classList.add("close")
    isOpen = true;
  }
});

