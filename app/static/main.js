// active nav buttons
if (window.location.href.includes("signup")) {
  document.querySelector("#signupBtn").classList.add("active");
} else if (window.location.href.includes("")) {
  document.querySelector(".home").classList.add("active");
}

// Login Modal
const modalBtn = document.querySelector("#loginBtn");
const modal = document.querySelector("#simpleModal");
const closeBtn = document.querySelector(".closeBtn");

modalBtn.addEventListener("click", openModal);
closeBtn.addEventListener("click", closeModal);
window.addEventListener("click", clickOutside);

function openModal() {
  modal.style.display = "block";
}
function closeModal() {
  modal.style.display = "none";
}
function clickOutside(e) {
  if (e.target === modal) {
    modal.style.display = "none";
  }
  if (window.location.href.includes("sign-up")) {
    document.querySelector("#signupBtn").classList.add("active");
  }
}

// load login modal when a route is login requierd
if (window.location.href.includes("signup?next=")) {
  openModal();
}

// Sending Login form data to back-end
const loginForm = document.querySelector("#loginForm");

loginForm.addEventListener("submit", (e) => {
  e.preventDefault();

  const inputEmail = document.querySelector("#inputEmail").value;
  const inputPassword = document.querySelector("#inputPassword").value;

  if (inputEmail !== "" && inputPassword !== "") {
    const xml = new XMLHttpRequest();
    const data = new FormData();

    data.append("email", inputEmail);
    data.append("password", inputPassword);

    xml.open("POST", "/login-request", true);
    xml.onload = function (e) {
      if (xml.status === 200) {
        window.location.href = "/user/setting";
      } else {
        document.querySelector(".login-form-message").innerHTML =
          "Something went wrong!";
        document.querySelector(".login-form-message").style.display = "block";
      }
    };
    xml.send(data);

    document.querySelector("#inputEmail").value = "";
    document.querySelector("#inputPassword").value = "";
  } else {
    document.querySelector(".login-form-message").style.display = "block";
  }
});
