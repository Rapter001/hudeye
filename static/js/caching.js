        // Function to load files from localStorage or fetch from server
        function loadMediaFiles() {
            const mediaContainer = document.getElementById('media-container');
            const cachedData = JSON.parse(localStorage.getItem('files'));
            const cacheExpirationTime = 3600000;
            const currentTime = new Date().getTime();

            if (cachedData && (currentTime - cachedData.timestamp < cacheExpirationTime)) {
                cachedData.files.forEach(file => {
                    let mediaElement;
                    if (file.endsWith('.mp4')) {
                        mediaElement = document.createElement('video');
                        mediaElement.classList.add('media');
                        mediaElement.setAttribute('autoplay', 'true');
                        mediaElement.setAttribute('controls', 'true');
                        mediaElement.innerHTML = `<source src="${file}" type="video/mp4">Your browser does not support the video tag.`;
                    } else if (file.endsWith('.jpg') || file.endsWith('.png') || file.endsWith('.gif')) {
                        mediaElement = document.createElement('img');
                        mediaElement.src = file;
                        mediaElement.alt = file;
                    } else {
                        mediaElement = document.createElement('a');
                        mediaElement.href = file;
                        mediaElement.textContent = file;
                    }
                    const mediaItem = document.createElement('div');
                    mediaItem.classList.add('media-item');
                    mediaItem.appendChild(mediaElement);
                    mediaContainer.appendChild(mediaItem);
                });
            } else {
                fetchFilesFromServer();
            }
        }

        function fetchFilesFromServer() {
            fetch('/get_files')
                .then(response => response.json())
                .then(data => {
                    const filesWithTimestamp = {
                        timestamp: new Date().getTime(),
                        files: data.files
                    };
                    localStorage.setItem('files', JSON.stringify(filesWithTimestamp));
                    loadMediaFiles();
                })
                .catch(error => console.error('Error fetching files:', error));
        }

        document.addEventListener('DOMContentLoaded', loadMediaFiles);