const sideBar = document.querySelector(".sidebar")
const menuBar = document.getElementById("menubar")
const closeSidebar = document.getElementById("close-sidebar")
const mainContent = document.querySelector(".main-content")
const subMenu = document.querySelector(".user-menu")
const subMenuBg = document.querySelector(".user-menu-bg")
const userNameItem = document.querySelector(".userNameItem")
const theming = document.querySelector(".theming")
menuBar.onclick = ()=>{
    sideBar.classList.toggle("respond")
    mainContent.classList.toggle("respond")
}
closeSidebar.onclick = ()=>{
    sideBar.classList.remove("respond")
}
userNameItem.onclick = ()=>{
    subMenu.classList.remove("hidden")
    subMenuBg.classList.remove("hidden")
}
subMenuBg.onclick = ()=>{
    subMenu.classList.add("hidden")
    subMenuBg.classList.add("hidden")
}
window.addEventListener("DOMContentLoaded",()=>{
    if(localStorage.getItem("ctheming") == "dark"){
        // currentTheme = localStorage.getItem("ctheming")
        document.body.classList.add("dark")
    }
})
theming.onclick = ()=>{
    document.body.classList.toggle("dark")
    if(document.body.classList.contains("dark")){
        localStorage.setItem("ctheming","dark")
    }else{        
        localStorage.setItem("ctheming","light")
    }
}



// loader
const loader = document.querySelector(".loader-wrap")
function showLoader(){
    loader.classList.remove("hidden")
}
function hideLoader(){
    loader.classList.add("hidden")
}