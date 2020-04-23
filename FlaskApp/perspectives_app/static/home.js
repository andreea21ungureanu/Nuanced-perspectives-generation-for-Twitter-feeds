function constructURL(value) {
    return 'subject/topic=' + value;
}

function onSearch() {
  if (searchBox.value == "") {
    alert("Please enter a search term");
    return;
  }

  if (searchBox.value.includes("<script>")) {
    alert("Not this time :)");
    return
  }
  
  window.location.href += constructURL(searchBox.value);
}

const searchBox = document.getElementById("subjectFill");
const searchButton = document.getElementById("submitButton");

searchButton.addEventListener("click", onSearch);
searchBox.addEventListener("keyup", (event) => {
  if (event.keyCode == 13) onSearch()
});

