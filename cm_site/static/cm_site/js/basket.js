let mergedSongs = [];
let mainPromo = '';

songs.forEach(song => {
    const matchingSong = songsData.find(data => data.name === song.name);
    if (matchingSong) {
        const mergedSong = {
            name: song.name,
            license: song.license,
            price: song.price,
            typeBeat: matchingSong.typeBeat,
            cover: matchingSong.cover
        };
        mergedSongs.push(mergedSong);
    }
});
let mergedSongLength = mergedSongs.length;

const targetElement = document.querySelector('.cart_is_full');
const totalCountElement = document.querySelector('.summary__total-count');
const totalPriceElement = document.querySelector('.summary__total-price');
const checkoutBtn = document.querySelector('.summary__checkout');
const fee = document.querySelector('.summary__total_fee_price');
let deleteButtons;

function tracksFill(discount=null){
    let innerhtml = '';
    let totalCount = 0;
    let totalPrice = 0;
    mergedSongs.forEach((song, index, array) => {
        innerhtml += `
        <div class="cart_is_full__beat">
            <div class="beat_left">
                <div class="beat_left__cover" style="background: url('../../../media/${song.cover}') no-repeat; background-size: cover;"></div>
                <div class="beat_left__data">
                    <div class="beat_left__data-name">${song.name}</div>
                    <div class="beat_left__data-license">${song.license === "wav" ? 'Beat - WAV License' : song.license === "unlimited" ? 'Beat - Unlimited License' : 'Beat - Exclusive License'}</div>
                    <a href="../media/${song.license === "wav" ? contractLinks[0] : song.license === "unlimited" ? contractLinks[1] : contractLinks[2]}" class="beat_left__data-review">Review License</a>
                </div>
            </div>
            <div class="beat_right">
                <div class="beat_right__price">${song.price}$</div>
                <button class="beat_right__del ${index}"></button>
            </div>
        </div>
        `;
        if (index !== array.length - 1){
            innerhtml += `<div class="cart_is_full__line"></div>`;
        }
        totalCount += 1;
        totalPrice += parseInt(song.price) * 100;
    });
    targetElement.innerHTML = innerhtml;
    totalCountElement.innerHTML = `Total (${totalCount} items)`;
    totalPriceElement.innerHTML = `$${totalPrice / 100}.00`;
    if (discount != null){
        totalPrice = (totalPrice - Math.floor(totalPrice * (discount / 100)));
        totalPriceElement.innerHTML = `$${(totalPrice / 100).toFixed(2)}`;        
    }
    fee.innerHTML = `$${(Math.ceil(totalPrice * 0.029 + 30) / 100).toFixed(2)}`;

    deleteButtons = document.querySelectorAll('.beat_right__del');
    deleteButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            let n = mergedSongs[parseInt(button.classList[1])].name;
            let l = mergedSongs[parseInt(button.classList[1])].license;
            const url = cartUrl;
            const data = { 
                name: n, 
                license: l,
                csrfmiddlewaretoken: csrfmiddlewaretoken
            };
            fetch(url, {
                method: 'DELETE',
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
                delete mergedSongs[parseInt(button.classList[1])];
                mergedSongLength--;
                if (mergedSongLength === 0){
                    window.location.reload();
                } else {
                    tracksFill();
                }

            })
            .catch(error => {
                console.error('Error:', error);
            });
        })
    });
    
}

if (mergedSongLength !== 0){
    tracksFill();
}

if (checkoutBtn){
    checkoutBtn.addEventListener('click', () => {
        window.location.href = `${checkoutURL}?promocode=${mainPromo}`;
    });
}

const promoOpenBtn = document.querySelector('.promo_open');
const promoContent = document.querySelector('.promo__container');
promoOpenBtn.addEventListener('click', () => {
    if (promoContent.classList.contains('close')){
        promoContent.classList.remove('close');
    } else {
        promoContent.classList.add('close');
    }
});
document.querySelector('.promo__container__close')
    .addEventListener('click', () => {
        promoContent.classList.add('close');
    });


const promoApply = document.querySelector('.promo__container__apply');
const enteredPromocode = document.querySelector('.promo__container__input');
promoApply.addEventListener('click', () => {
    const url = promoUrl;
    const data = { 
        promocode: enteredPromocode.value, 
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
        current_answer = data;
        console.log(current_answer.status);
        console.log(current_answer.data.promo_discount);
        if (current_answer.status === "OK"){
            tracksFill(current_answer.data.promo_discount);
            promoContent.classList.add('close');
            document.querySelector('.promo').innerHTML = 'Coupon appiled';
            mainPromo = enteredPromocode.value;
            document.querySelector('.promo').style = `
                font-family: Outfit;
                font-weight: 400;
                font-size: 16px;
                padding: 0;
                letter-spacing: 0.05em;
                color: #BA0038;
                text-align: end;
            `;
        } else {
            let ansItem = document.querySelector('.promo__container__title')
            let oldInnerHtml = ansItem.innerHTML;
            ansItem.innerHTML = 'Invalid coupon';
            ansItem.style.color = '#ba0038';
            setTimeout(() => {
                ansItem.innerHTML = oldInnerHtml;
                ansItem.style.color = '#FFF';
            }, 5000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    }); 
});