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
    window.location.href = singOutHREF;
})


switch (redirect_on) {
    case 'support':
            removeClasses('active', [infoBtn, purBtn, wishlistBtn, supportBtn, singOutBtn, infoCnt, purCnt, wishlistCnt, supportCnt]);
            supportBtn.classList.add('active');
            supportCnt.classList.add('active');
            break;
    
    case 'info':
            removeClasses('active', [infoBtn, purBtn, wishlistBtn, supportBtn, singOutBtn, infoCnt, purCnt, wishlistCnt, supportCnt]);
            infoBtn.classList.add('active');
            infoCnt.classList.add('active');
            break;

    default:
            break;
}

const replaceData1 = document.querySelectorAll('.left__track_data__track_license');
const replaceData2 = document.querySelectorAll('.right__track_pur_data__price');

replaceData1.forEach((el) => {
    if (el.innerHTML === 'wav'){
        el.innerHTML = 'Beat - WAV License';
    } else if (el.innerHTML === 'unlimited') {
        el.innerHTML = 'Beat - Unlimited License';
    } else {
        el.innerHTML = 'Beat - Exclusive License';
    }
});
replaceData2.forEach((el) => {
    if (el.innerHTML === 'wav'){
        el.innerHTML = `$${wawPrice}`;
    } else if (el.innerHTML === 'unlimited') {
        el.innerHTML = `$${unlPrice}`;
    } else {
        el.innerHTML = `$${excPrice}`;
    }
});