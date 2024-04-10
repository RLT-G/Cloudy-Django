let mergedSongs = [];


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

const targetElement = document.querySelector('.cart_is_full');
const totalCountElement = document.querySelector('.summary__total-count');
const totalPriceElement = document.querySelector('.summary__total-price');
const checkoutBtn = document.querySelector('.summary__checkout');

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
                <div class="beat_left__data-review">Review License</div>
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
    totalPrice += parseInt(song.price);
});

targetElement.innerHTML = innerhtml;
totalCountElement.innerHTML = `Total (${totalCount} items)`;
totalPriceElement.innerHTML = `$${totalPrice}.00`;

checkoutBtn.addEventListener('click', () => {
    window.location.href = checkoutURL;
})