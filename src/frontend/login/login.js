const usernameInput = document.getElementById("username-input");
const passwordInput = document.getElementById("password-input");
const button = document.getElementsByTagName("button")[0];

function validate_username() {
  const msgHolder = usernameInput.parentElement.getElementsByTagName("p")[0];
  if (usernameInput.value.trim() == "") {
    usernameInput.classList.add("invalid");
    msgHolder.innerHTML = "empty user name";
    return false;
  }
  usernameInput.classList.remove("invalid");
  msgHolder.innerHTML = "";
  return true;
}

function validate_password() {
  const msgHolder = passwordInput.parentElement.getElementsByTagName("p")[0];
  if (passwordInput.value == "") {
    passwordInput.classList.add("invalid");
    msgHolder.innerHTML = "empty password";
    return false;
  }
  if (passwordInput.value.length < 6)
  {
    passwordInput.classList.add("invalid");
    msgHolder.innerHTML = "password should be at least 6 characters";
    return false;
  }

  passwordInput.classList.remove("invalid");
  msgHolder.innerHTML = "";
  return true;
}


async function login() {

  if (!validate_username() || !validate_password())
    return validate_password();
  const user = usernameInput.value.trim();
  const password = passwordInput.value.trim();

  const resp = await fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user, password }),
  });
  if (resp.status == 200) {
    window.location.href = "/";
    return;
  }
  const resp_obj = await resp.json();
  showToast(resp_obj["detail"]);
}

button.addEventListener("click", login);

usernameInput.addEventListener("keydown", (e) => {
  if (e.key == "Enter") button.click();
});

passwordInput.addEventListener("keydown", (e) => {
  if (e.key == "Enter") button.click();
});
