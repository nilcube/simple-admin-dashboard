async function isLogedIn() {
  return (await fetch("/me")).ok;
}



function hideElements() {
  const welcomeText = document.getElementById("welcome-section");
  welcomeText.style.display = "none";
}


async function createHome() {
  if (!(await isLogedIn())) return;
  hideElements();

}
