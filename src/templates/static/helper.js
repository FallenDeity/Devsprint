let prevScrollpos = window.scrollY;


function responsive() {
    if (window.outerWidth > 1000) {
        document.getElementById("menu").style.display = "none";
        document.getElementById("mobile-menu").style.display = "none";
    } else {
        document.getElementById("menu").style.display = "block";
        document.getElementById("menu").style.float = "right";
    }
}


window.addEventListener("resize", function () {
    responsive();
});


window.addEventListener("scroll", function () {
    sticky();
});


function sticky() {
    let navbar = document.getElementById("Navbar");
    if (navbar === null) {
        return;
    }
    let carousel = document.getElementById("carouselIndicators");
    const currentScrollPos = window.scrollY;
    if (prevScrollpos > currentScrollPos) {
        document.getElementById("Navbar").style.top = "0";
        if (carousel !== null) {
            document.getElementById("carouselIndicators").style.top = "80px";
        }
    } else {
        document.getElementById("Navbar").style.top = "-80px";
        if (carousel !== null) {
            document.getElementById("carouselIndicators").style.top = "0";
        }
    }
    prevScrollpos = currentScrollPos;
}


function testImage(name) {
    return new Promise(function () {
        let timeout = 5000;
        let url = document.getElementById("avatar_url").value;
        let timer, img = new Image();
        img.onerror = img.onabort = function () {
            clearTimeout(timer);
            alert("Image not found");
        };
        img.onload = function () {
            clearTimeout(timer);
            let data = JSON.stringify({username: name, avatar: url});
            let xhr = new XMLHttpRequest();
            xhr.open("POST", "/api/v1/avatar", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(data);
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                    let response = JSON.parse(xhr.responseText);
                    alert(response.message);
                    window.location.href = "/profile";
                }
            }
        };
        timer = setTimeout(function () {
            img.src = "//!!!!/test.jpg";
            alert("Image not found");
        }, timeout);
        img.src = url;
    });
}


function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function get_ip() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "https://api.ipify.org?format=json", false);
    xhr.send();
    return JSON.parse(xhr.responseText).ip;
}


function addFeedback() {
    let feedback = document.getElementById("feedback").value;
    let xhr = new XMLHttpRequest();
    let ip = get_ip();
    xhr.open("POST", "/api/v1/feedback", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ip: ip, feedback: feedback}));
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            let response = JSON.parse(xhr.responseText);
            alert(response.message);
        }
    }
}


function topNav() {
    const topNav = document.getElementById("mobile-menu");
    topNav.style.display = topNav.style.display === "flex" ? "none" : "flex";
    const menuBtn = document.getElementById("menu-btn");
    menuBtn.className = menuBtn.className === "fa-solid fa-bars" ? "fa-solid fa-xmark" : "fa-solid fa-bars";
}


function addComment(id, username, avatar) {
    let comment = document.getElementById("textAreaExample").value;
    if (comment === ""){
        alert("Please fill the comment field");
        return false;
    }
    let xhr = new XMLHttpRequest();
    let data = JSON.stringify({id: id, username: username, avatar: avatar, comment: comment});
    xhr.open("POST", "/api/v1/comment", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            let response = JSON.parse(xhr.responseText);
            alert(response.message);
            window.location.href = "/anime?anime_id=" + id;
        }
    }
    xhr.send(data);
}


function addBookmark(id, username) {
    let xhr = new XMLHttpRequest();
    let data = JSON.stringify({id: id, username: username});
    xhr.open("POST", "/api/v1/bookmark", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            let response = JSON.parse(xhr.responseText);
            alert(response.message);
            if (window.location.href.includes("/profile")){
                window.location.href = "/profile";
            }
        }
    }
    xhr.send(data);
}


function validateInput() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    if (username === "" || password === "") {
        alert("Please fill all the fields");
        return false;
    }
    if (password.length < 8) {
        alert("Password must be at least 8 characters long");
        return false;
    }
    return true;
}


function SignUp() {
    if (!validateInput()) {
        return false;
    }
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let xhr = new XMLHttpRequest();
    let ip = get_ip();
    xhr.open("POST", "/api/v1/signup", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    let data = JSON.stringify({username: username, password: password, ip: ip});
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            let response = JSON.parse(xhr.responseText);
            if (xhr.status === 400) {
                alert(response.message);
            } else {
                alert(response.message);
                window.location.href = "/login";
            }
        }
    }
    xhr.send(data);
}


function Login() {
    if (!validateInput()) {
        return false;
    }
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    let ip = get_ip();
    let body = JSON.stringify({username: username, password: password, ip: ip});
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/v1/login", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            let response = JSON.parse(xhr.responseText);
            if (xhr.status === 400) {
                alert(response.message);
            } else {
                alert(response.message);
                let redirect = new XMLHttpRequest();
                redirect.open("GET", "/api/v1/redirect", true);
                let headers = {
                    "Content-Type": "application/json",
                    "username": username,
                }
                for (let key in headers) {
                    redirect.setRequestHeader(key, headers[key]);
                }
                redirect.onreadystatechange = function () {
                    if (redirect.readyState === 4) {
                        window.location.href = "/";
                    }
                }
                redirect.send();
            }
        }
    }
    xhr.send(body);
}
