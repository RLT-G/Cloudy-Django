const wavBtn = document.querySelector('.wav');
const unlBtn = document.querySelector('.unl');
const excBtn = document.querySelector('.exc');

const wavDesc = document.querySelector('.t-wav');
const unlDesc = document.querySelector('.t-unl');
const excDesc = document.querySelector('.t-exc');

const termsBtn = document.querySelector('.terms_btn');
let termsIsOpen = false;
let andle = 180;

const buyBtn = document.querySelector('.to_cart') 

let buyType = 'wav'

wavBtn.addEventListener('click', () => {
    buyType = 'wav';
    changeClasses(wavBtn, wavBtn, unlBtn, excBtn);
    if (termsIsOpen){
        unlDesc.classList.remove('active');
        excDesc.classList.remove('active');
        wavDesc.classList.add('active');
    }
})
unlBtn.addEventListener('click', () => {
    buyType = 'unlimited';
    changeClasses(unlBtn, wavBtn, unlBtn, excBtn);
    if (termsIsOpen){
        unlDesc.classList.add('active');
        excDesc.classList.remove('active');
        wavDesc.classList.remove('active');
    }
})
excBtn.addEventListener('click', () => {
    buyType = 'exclusive';
    changeClasses(excBtn, wavBtn, unlBtn, excBtn);
    if (termsIsOpen){
        unlDesc.classList.remove('active');
        excDesc.classList.add('active');
        wavDesc.classList.remove('active');
    }
})

function changeClasses(main, rem1, rem2, rem3){
    rem1.classList.remove('active');
    rem2.classList.remove('active');
    rem3.classList.remove('active');
    main.classList.add('active');
} 


termsBtn.addEventListener('click', () => {
    termsBtn.style.transform = `rotate(${andle}deg)`;
    andle += 180;

    if (termsIsOpen){
        wavDesc.classList.remove('active');
        unlDesc.classList.remove('active');
        excDesc.classList.remove('active');
        termsIsOpen = false;
    } else if (buyType === 'wav'){
        wavDesc.classList.add('active');
        termsIsOpen = true;
    } else if (buyType === 'unlimited'){
        unlDesc.classList.add('active');
        termsIsOpen = true;
    } else {
        excDesc.classList.add('active');
        termsIsOpen = true;
    }  
})


buyBtn.addEventListener('click', () => {
    const url = cartUrl;
    const data = { 
        name: trackName, 
        license: buyType,
        csrfmiddlewaretoken: csrfmiddlewaretoken
    };
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfmiddlewaretoken
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        buyBtn.classList.add('incart');
        document.querySelector('.beat__intro__data_name-btn .to_cart.incart div:nth-child(2)').innerHTML = 'Added';
        document.querySelector('.navbar__link-basket').style = "background: url('../../static/cm_site/img/cartisnotempty.svg') no-repeat; background-size: cover;";
    })
    .catch(error => {
        console.error('Error:', error);
    });
});