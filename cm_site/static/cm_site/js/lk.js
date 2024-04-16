let infoBtn = document.querySelector('.btn-info');
let purBtn = document.querySelector('.btn-purchases');
let wishlistBtn = document.querySelector('.btn-wishlist');
let supportBtn = document.querySelector('.btn-support');
let singOutBtn = document.querySelector('.btn-singout');

let infoCnt = document.querySelector('.content__info');
let purCnt = document.querySelector('.content__purchases');
let wishlistCnt = document.querySelector('.content__wishlist');
let supportCnt = document.querySelector('.content__support');

function removeClasses(className, array){
    array.forEach((element) => {
        element.classList.remove(className);
    });
}

infoBtn.addEventListener('click', () => {
    removeClasses('active', [infoBtn, purBtn, wishlistBtn, supportBtn, singOutBtn, infoCnt, purCnt, wishlistCnt, supportCnt]);
    infoBtn.classList.add('active');
    infoCnt.classList.add('active');
})

purBtn.addEventListener('click', () => {
    removeClasses('active', [infoBtn, purBtn, wishlistBtn, supportBtn, singOutBtn, infoCnt, purCnt, wishlistCnt, supportCnt]);
    purBtn.classList.add('active');
    purCnt.classList.add('active');
})

wishlistBtn.addEventListener('click', () => {
    removeClasses('active', [infoBtn, purBtn, wishlistBtn, supportBtn, singOutBtn, infoCnt, purCnt, wishlistCnt, supportCnt]);
    wishlistBtn.classList.add('active');
    wishlistCnt.classList.add('active');
})

supportBtn.addEventListener('click', () => {
    removeClasses('active', [infoBtn, purBtn, wishlistBtn, supportBtn, singOutBtn, infoCnt, purCnt, wishlistCnt, supportCnt]);
    supportBtn.classList.add('active');
    supportCnt.classList.add('active');
})
singOutBtn.addEventListener('click', () => {
    console.log('click on singOunt');
})