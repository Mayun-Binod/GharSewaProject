// Sidebar Toggle

function sideBar(){
    let nav = document.querySelector('.sidebar');
    
    let burger = document.querySelector('.burger');
    let content = document.querySelector('.content');

    nav.classList.toggle('active');
    burger.classList.toggle('active')
    content.classList.toggle('active');
    content.classList.toggle('shrink');

}