document.querySelector('#categoryInput').addEventListener('keydown', function(e) {
  if (e.keyCode === 13) {
    e.preventDefault();
    let categoryName = this.value;
    addNewCategory(categoryName);
    updateCategoryString();
    this.value = ''
  }
})

function addNewCategory(name){
  document.querySelector('#categoriesContainer').insertAdjacentHTML('beforeend',
  `<li class="category">
    <span class="name">${name}</span>
    <span onclick="removeCategory(this)" class="btnRemove bold">X</span>
  </li>`)
}

function updateCategoryString() {
  let categoryArray = []
  document.querySelectorAll('.category').forEach(element => {
    name = element.querySelector('.name').innerHTML
    categoryArray.push(name);
    document.querySelector('input[name="categoriesString"]').value = categoryArray.join(',')
  });
}

function removeCategory(e) {
  e.parentElement.remove()
  updateCategoryString()
}
