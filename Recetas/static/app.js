const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");

searchForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const userInput = searchInput.value;
  fetch(`/search?user_input=${userInput}`)
    .then((response) => response.json())
    .then((data) => {
      const recipeTitles = data.recipe_titles;
      const message = data.message;
      const recipeList = document.getElementById("recipe-list");
      recipeList.innerHTML = "";
      const messageElement = document.getElementById("message");
      messageElement.innerHTML = message;
      if (recipeTitles.length > 0) {
        const list = document.createElement("ul");
        recipeList.appendChild(list);
        for (let i = 0; i < recipeTitles.length; i++) {
          const listItem = document.createElement("li");
          listItem.innerHTML = recipeTitles[i];
          list.appendChild(listItem);
        }
      }
    })
    .catch((error) => console.log(error));
});

const searchBar = document.getElementById("search-bar");
const searchIcon = document.getElementById("search-icon");

searchIcon.addEventListener("click", () => {
  searchBar.classList.toggle("active");
  searchInput.focus();
});

searchInput.addEventListener("blur", () => {
  if (!searchInput.value) {
    searchBar.classList.remove("active");
  }
});

searchInput.addEventListener("keydown", (event) => {
  if (event.keyCode === 13) {
    event.preventDefault();
    searchForm.submit();
  }
});