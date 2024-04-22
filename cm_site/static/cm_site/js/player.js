
        // Получение блоков
        const progressContainer = document.querySelector('.player__progress');
        const volumeControlIco = document.querySelector('.volume-ico');
        const typeBeat = document.querySelector('.player-type');
        const volumeControl = document.querySelector('.volume');
        const audio = document.querySelector('.player__audio');
        const cover = document.querySelector('.player-cover');
        const progress = document.querySelector('.player__progress');
        const title = document.querySelector('.player-name');
        const nextBtn = document.querySelector('.forward');
        const randBtn = document.querySelector('.random');
        const player = document.querySelector('.player');
        const repBtn = document.querySelector('.repeat');
        const playBtn = document.querySelector('.play');
        const prevBtn = document.querySelector('.back');
        const buyLink = document.querySelector('.player__container_other-link');
        player.classList.add('player-deactivate');
        let launshWas = false;

      
      

        function changeBlobData(songIndex) {
            const audioUrl = songs[songIndex].mp3;
            
            return fetch(audioUrl)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.blob();
                })
                .then(blob => {
                    const objectURL = URL.createObjectURL(blob);
                    songs[songIndex].scr = objectURL;
                    console.log('Audio loaded successfully:', objectURL);
                    return objectURL; // возвращаем URL для использования в следующем then
                })
                .catch(error => {
                    console.error('Error loading audio file:', error);
                    throw error; // повторно выбрасываем ошибку для обработки в следующем catch
                });
        }


        let songIndex = 0;

        function loadSong(songIndex, play=true, musicCoverLoad=null) {
            if (musicCoverLoad !== null){
                musicCoverLoad.classList.add('musicCoverLoad');
            }
            changeBlobData(songIndex)
                .then(objectURL => {
                    // Этот код выполнится после завершения changeBlobData
                    audio.src = objectURL;
                    title.innerHTML = songs[songIndex].name;
                    typeBeat.innerHTML = songs[songIndex].typeBeat;
                    cover.style.background = "url(" + songs[songIndex].cover + ")";
                    cover.style.backgroundSize = "cover";
                    cover.style.backgroundRepeat = "no-repeat";
                    buyLink.href = songs[songIndex].href;
                    if (play){
                        playSong();
                    }
                    if(launshWas === true) {
                        launshWas = false;
                        /////////////////////////////////////
                        console.log('launshWas = false ибо loadsong закончил выгрузку');
                        /////////////////////////////////////
                    }
                    if (musicCoverLoad !== null){
                        musicCoverLoad.classList.remove('musicCoverLoad');
                    }
                })
                .catch(error => {
                    // Обработка ошибок, если они возникнут в changeBlobData
                    console.error('Error in loadSong:', error);
                });
        }

        // init
        loadSong(songIndex, false);
        // Запуск Трека
        function playSong(){
            player.classList.add('playSong');
            audio.play();
            playBtn.style.background = "url(../../static/cm_site/img/p-pp.svg)";
        }
        // Пауза
        function pauseSong(){
            player.classList.remove('playSong');
            audio.pause();
            playBtn.style.background = "url(../../static/cm_site/img/p-p.svg)";
        }
        // Кнопка play
        playBtn.addEventListener('click', () => {
            const isPlaying = player.classList.contains('playSong');
            if (isPlaying){
                pauseSong();
            } else {
                playSong();
            }
        });
        // Кнопка рандома
        let isRand = false;
        function randHandler(){
            if (isRand){
                isRand = false;
                randBtn.style.background = "url('../../static/cm_site/img/p-random.svg')";
                randBtn.style.backgroundSize = "cover";
                randBtn.style.backgroundRepeat = "no-repeat";
            } else {
                isRand = true;
                randBtn.style.background = "url('../../static/cm_site/img/randActive.svg')";
                randBtn.style.backgroundSize = "cover";
                randBtn.style.backgroundRepeat = "no-repeat";
            }
        }
        randBtn.addEventListener('click', randHandler);
        // Кнопка повтора
        let isRep = false;
        function repHandler(){
            if (isRep){
                isRep = false;
                repBtn.style.background = "url('../../static/cm_site/img/p-repeat.svg')";
                repBtn.style.backgroundSize = "cover";
                repBtn.style.backgroundRepeat = "no-repeat";
            } else {
                isRep = true;
                repBtn.style.background = "url('../../static/cm_site/img/repActive.svg')";
                repBtn.style.backgroundSize = "cover";
                repBtn.style.backgroundRepeat = "no-repeat";
            }
        }
        repBtn.addEventListener('click', repHandler);
        audio.addEventListener("ended", function() {
            if (isRep){
                audio.currentTime = 0;
                audio.play();
            }
            else{
                nextSong();
            }
        });
        // Кнопка next
        function nextSong(){
            if (!launshWas){
                launshWas = true;
                songIndex++;
                if (songIndex > songs.length - 1){
                    songIndex = 0;
                }
                if (isRand){
                    songIndex = Math.floor(Math.random() * songs.length);
                }
                const musicCoverLoadFromPlayer = document.querySelector(`.music:nth-child(${songIndex + 1}) .music__cover`);
                loadSong(songIndex, true, musicCoverLoadFromPlayer);
            } else {
            /////////////////////////////////////
            console.log('Заблокировал ->');
            /////////////////////////////////////
            }
        }
        nextBtn.addEventListener('click', nextSong);
        // Кнопка prev
        function prevSong(){
            if (!launshWas){
                launshWas = true;
                songIndex--;
                if (songIndex < 0){
                    songIndex = songs.length - 1;
                }
                if (isRand){
                    songIndex = Math.floor(Math.random() * songs.length);
                }
                loadSong(songIndex);
            } else {
                /////////////////////////////////////
                console.log('Заблокировал <-');
                /////////////////////////////////////
            }
        }
        prevBtn.addEventListener('click', prevSong);

        // Движение прогресс-бара
        function updateProgress(e){
            const {duration, currentTime} = e.srcElement;
            const progressPercent = (currentTime / duration) * 100;
            progress.value = parseFloat(progressPercent.toFixed(5));
            // Получаем элемент .player__progress
            const playerProgressUp = $('.player__progress');

            if (flag){
                playerProgressUp.css('background', `linear-gradient(to right, #BA0038 0%, #BA0038 ${playerProgressUp.val()}%, #464646 ${playerProgressUp.val()}%, #464646 100%)`);

            } else {
                playerProgressUp.css('background', `linear-gradient(to right, #BA0038 0%, #BA0038 ${playerProgressUp.val()}%, transparent ${playerProgressUp.val()}%, transparent 100%)`);                
            }
            // Устанавливаем стиль
        }
        audio.addEventListener('timeupdate', updateProgress);
        progress.addEventListener('input', function() {
            const progress_value = parseFloat(this.value);
            const duration = audio.duration; 
            audio.currentTime = (progress_value / 100) * duration;
        });
        // Звук
        audio.volume = 1;
        volumeControl.addEventListener('input', function() {
            const volume = parseFloat(this.value);
            if (volume == 0){
                volumeControlIco.style.background = "url('../../static/cm_site/img/v1.svg')";
                volumeControlIco.style.backgroundSize = "cover";
                volumeControlIco.style.backgroundRepeat = "no-repeat";
            } else {
                if (volume < 0.33){
                    volumeControlIco.style.background = "url('../../static/cm_site/img/v2.svg')";
                    volumeControlIco.style.backgroundSize = "cover";
                    volumeControlIco.style.backgroundRepeat = "no-repeat";
                } else {
                    if (volume < 0.66){
                        volumeControlIco.style.background = "url('../../static/cm_site/img/v3.svg')";
                        volumeControlIco.style.backgroundSize = "cover";
                        volumeControlIco.style.backgroundRepeat = "no-repeat";
                    } else {
                        volumeControlIco.style.background = "url('../../static/cm_site/img/p-vol.svg')";
                        volumeControlIco.style.backgroundSize = "cover";
                        volumeControlIco.style.backgroundRepeat = "no-repeat";
                    }
                }
            }
            audio.volume = volume;
        });

        function coverPlay(index){
            if (!launshWas){
                launshWas = true;
                /////////////////////////////////////
                console.log('launshWas = true ибо coverplay');
                /////////////////////////////////////
                if (player.classList.contains('player-deactivate')) {
                    player.classList.remove('player-deactivate');
                    player.classList.add('player-activate');
                }
                if (songIndex != index - 1){
                    let classDel;
                    let innerClassDel;
                    for (let i = 1; i <= songs.length; i++) {
                        innerClassDel = document.querySelector(`.music:nth-child(${i}) .music__cover_button`);
                        classDel = document.querySelector(`.music:nth-child(${i})`);
                        classDel.classList.remove('operated');
                        innerClassDel.classList.remove('music__cover_button-active');
                    }
                }
                const musicButton = document.querySelector(`.music:nth-child(${index})`);
                const musicCoverLoad = document.querySelector(`.music:nth-child(${index}) .music__cover`);

                const isOperated = musicButton.classList.contains('operated');
                const musicCoverButton = document.querySelector(`.music:nth-child(${index}) .music__cover_button`);
                if (isOperated){
                    const isPlaing = musicButton.classList.contains('playSong');
                    if (isPlaing){
                        musicCoverButton.classList.remove('music__cover_button-active');
                        musicButton.classList.remove('playSong');
                        pauseSong();
                    } else {
                        musicCoverButton.classList.add('music__cover_button-active');
                        musicButton.classList.add('playSong');
                        playSong();
                    }
                    launshWas = false;
                    /////////////////////////////////////
                    console.log('launshWas = false ибо coverplay закончилось обычным запуском');
                    /////////////////////////////////////
                } else {
                    console.log('init');
                    musicButton.classList.add('operated');
                    musicButton.classList.add('playSong');
                    musicCoverButton.classList.add('music__cover_button-active');
                    songIndex = index - 1;

                    loadSong(songIndex, true, musicCoverLoad);
                }
            } else {
                /////////////////////////////////////
                console.log('Заблокировал coverplay');
                /////////////////////////////////////
            }
        }
        setTimeout(() => {
            let va = '0.00001'
            progress.value = parseFloat(va.toFixed(5));
        }, 1000);