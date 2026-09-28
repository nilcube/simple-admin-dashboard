


function showToast(msg) {
  const toast = document.getElementById("toast");

  const bread = document.createElement("div");
  bread.classList.add("bread");

  const text = document.createElement("p");
  text.innerHTML = msg;
  bread.appendChild(text);

  toast.appendChild(bread);

  setTimeout(() => {
    bread.remove();
  },3000);
}
