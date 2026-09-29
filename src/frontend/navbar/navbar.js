async function profile() {}


async function addLogo(){
  const aTag = document.createElement("a");
  aTag.href = "/";

  const img = document.createElement("img");
  img.src = "/static/logo.png";

  aTag.appendChild(img);
  return aTag;
}

async function createNavbar(show_profile = true) {
  const nvBar = document.createElement("div");
  nvBar.id = "nav-bar";

  document.body.insertAdjacentElement("afterbegin", nvBar);

  nvBar.append(await addLogo());

  return nvBar;
}
