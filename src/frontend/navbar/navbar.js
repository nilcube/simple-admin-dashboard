async function profile() {
  const resp = await fetch("/me");

  const aTag = document.createElement("a");
  const img = document.createElement("img");

  aTag.href = "/login";
  aTag.classList.add("profile-icon");
  img.src = "/static/empty-user-profile.svg"



  if (resp.ok){
  }
  aTag.appendChild(img);
  return aTag;
}


function addLogo(){
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

  nvBar.appendChild(addLogo());
  if (show_profile)
    nvBar.appendChild(await profile());

  return nvBar;
}
