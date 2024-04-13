const navBtn = document.querySelectorAll('.account__nav-btn');


function removeActiveClasses(){
    navBtn.forEach((el) => {
        el.classList.remove('active');
    })
}

navBtn.forEach((btn, index) => {
    btn.addEventListener('click', () => {
        removeActiveClasses();
        btn.classList.add('active');
    });
});
