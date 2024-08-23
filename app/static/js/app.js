



// Template for Analyzer Form
const tmplAnalyzerForm = () => {
    return `
        <div>
            <div class="form-group pb-3">
                <label for="article-title" class="form-label">Title</label>
                <input type="text" name="article-title" class="form-control" id="article-title" placeholder="Article Title">
            </div>
            <div class="form-group pb-3">
                <label for="article-body" class="form-label">Article Body</label>
                <textarea id="article-body" class="form-control" rows="5"></textarea>
            </div>
            <button id="btn-analyze" type="button" class="btn btn-primary w-100">Analyze</button>
        </div>
    `;
};

// Template for Analyzer Results
const tmplAnalyzerResults = (obj) => {
    return `
        <div class="results">
            <div class="my-4" style="display: flex; align-items: center;">
                <div class="icon" style="flex: 0 0 auto;">
                    <i class="far ${obj.icon} fa-lg" style="color: ${obj.color}"></i>
                </div>
                <div class="px-3 " style="flex: 1 1 auto;">
                <h4>${obj.title}</h4>
                ${obj.description}
                </div>
            </div>
            <button id="btn-back" type="button" class="btn btn-primary w-100 mt-3">Try Another</button>
        </div>
    `;
};

// Document Ready
$(document).ready(function() {
    // Event Listeners
    // Analyze Button Click Event
    $("body").on("click", "button#btn-analyze", function(event) {
        event.preventDefault();
        let article = {
            title: $("#article-title").val().trim(),
            body: $("#article-body").val().trim()
        }

        // API call to ML Article Analyzer
        $.ajax({
            url: "/api/v1.0/analyze",
            method: "POST",
            data: JSON.stringify(article),
            dataType: "json"
        }).then(function(data) {
            console.log(data);
            let results = {};

            if (data.prediction === "FAKE") {
                results = {
                    icon: "fa-angry",
                    color: "red",
                    title: "FAKE",
                    description: "The news article is Fake."
                    
                };
            } else {
                results = {
                    icon: "fa-smile",
                    color: "green",
                    title: "REAL",
                    description: "The news article is ligitimate."
                };
            }

            $("div.content-container").empty();
            $("div.content-container").html(tmplAnalyzerResults(results));
        });
    
    });
    
    // Retry Button Click Event
    $("body").on("click", "button#btn-back", function(event) {
        event.preventDefault();
        $("div.content-container").empty();
        $("div.content-container").html(tmplAnalyzerForm);
    });
});







function registerUser() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
   

 

    // Your registration API call or AJAX request here
    // Example using fetch:
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        alert('Registration successful. Please log in.');
        window.location.href = '/login';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Registration failed. Please try again.');
    });
}

function loginUser() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Your login API call or AJAX request here
    // Example using fetch:
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        alert('Login successful!');
        window.location.href = '/register';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Login failed. Please check your username and password.');
    });
}

const body = document.querySelector("body");
const darkLight = document.querySelector("#darkLight");
const sidebar = document.querySelector(".sidebar");
const submenuItems = document.querySelectorAll(".submenu_item");
const sidebarOpen = document.querySelector("#sidebarOpen");
const sidebarClose = document.querySelector(".collapse_sidebar");
const sidebarExpand = document.querySelector(".expand_sidebar");
sidebarOpen.addEventListener("click", () => sidebar.classList.toggle("close"));

sidebarClose.addEventListener("click", () => {
  sidebar.classList.add("close", "hoverable");
});
sidebarExpand.addEventListener("click", () => {
  sidebar.classList.remove("close", "hoverable");
});

sidebar.addEventListener("mouseenter", () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.remove("close");
  }
});
sidebar.addEventListener("mouseleave", () => {
  if (sidebar.classList.contains("hoverable")) {
    sidebar.classList.add("close");
  }
});

darkLight.addEventListener("click", () => {
  body.classList.toggle("dark");
  if (body.classList.contains("dark")) {
    document.setI;
    darkLight.classList.replace("bx-sun", "bx-moon");
  } else {
    darkLight.classList.replace("bx-moon", "bx-sun");
  }
});

submenuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    item.classList.toggle("show_submenu");
    submenuItems.forEach((item2, index2) => {
      if (index !== index2) {
        item2.classList.remove("show_submenu");
      }
    });
  });
});

if (window.innerWidth < 768) {
  sidebar.classList.add("close");
} else {
  sidebar.classList.remove("close");
}



