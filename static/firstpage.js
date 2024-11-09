function redirectToHome() {
    window.location.href = "secondpage.html";
}

var animation = bodymovin.loadAnimation({
    container: document.getElementsByClassName('container'),
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: 'https://lottie.host/d3a54590-2aab-450d-a4bd-d2839314aedb/XIJLXLFnqg.json'
  })
