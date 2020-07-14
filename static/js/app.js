const form = document.querySelector('form');
const two = document.querySelector('.two')

form.addEventListener('submit',e=>{
    e.preventDefault();

    two.style.display = 'inline-block'


})