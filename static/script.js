document.addEventListener("DOMContentLoaded", () => {

    const buttons = document.querySelectorAll("button");

    const button_plus = document.getElementById("plus");
    const button_minus = document.getElementById("minus");
    const button_multi = document.getElementById("multi");
    const button_div = document.getElementById("div");
/*
    buttons.forEach((button) => {
        button.addEventListener("click", () => {
            window.location.href = "/input";
        });    
    });
*/
    const handleButtonClick = (value) => {  
        console.log("Sending value: ", value);
        fetch("/home", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ value: value }),
        })

        .then(response => response.json())

        .then(data => {
            if(data.status == "success") {
                window.location.href = "/input";
            }
        })

        .catch((error) => {
            console.error("Error", error);
        })
    }

    button_plus.addEventListener("click", () => handleButtonClick(1));
    button_minus.addEventListener("click", () => handleButtonClick(2));
    button_multi.addEventListener("click", () => handleButtonClick(3));
    button_div.addEventListener("click", () => handleButtonClick(4));
    

});