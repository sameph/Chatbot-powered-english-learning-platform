
  // Function to search and filter words
  function searchWords() {
    const searchInput = document.getElementById('searchBox').value.toLowerCase();
    const wordListItems = document.getElementById('wordList').getElementsByTagName('li');

    for (let i = 0; i < wordListItems.length; i++) {
      const word = wordListItems[i].textContent || wordListItems[i].innerText;
      if (word.toLowerCase().indexOf(searchInput) > -1) {
        wordListItems[i].style.display = '';
      } else {
        wordListItems[i].style.display = 'none';
      }
    }
  }
  function searchWords() {
    const searchInput = document.getElementById('searchBox').value.toLowerCase();
    const wordListItems = document.getElementById('wordList').getElementsByTagName('li');

    for (let i = 0; i < wordListItems.length; i++) {
      const word = wordListItems[i].textContent || wordListItems[i].innerText;
      if (word.toLowerCase().indexOf(searchInput) > -1) {
        wordListItems[i].style.display = '';
      } else {
        wordListItems[i].style.display = 'none';
      }
    }
  }

  