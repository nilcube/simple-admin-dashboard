const usernameInput = document.getElementById("username-input");
const passwordInput = document.getElementById("password-input");
const button = document.getElementsByTagName("button")[0];

async function login() {
   const user = usernameInput.value.trim();
   const password = passwordInput.value.trim();

  const resp = await fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user, password }),
  });
  if (resp.ok && resp.status == 200) {
    window.location.href = "/";
  }
}

button.addEventListener("click", login);

usernameInput.addEventListener("keydown", (e) => {
  if (e.key == "Enter") button.click();
});

passwordInput.addEventListener("keydown", (e) => {
  if (e.key == "Enter") button.click();
});
