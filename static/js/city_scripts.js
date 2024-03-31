// Get the current day
let date = new Date();
let currentDay = date.getDay();

// Array to hold the names of the days of the week
let daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
let removeDays = [];

// New array to hold the current day and the next three days
let keepNextThreeDays = [];
for (let i = 0; i < 3; i++) {
    keepNextThreeDays.push(daysOfWeek[(currentDay + i) % 7]);
}
daysOfWeek.forEach(function(day) {
    if (!keepNextThreeDays.includes(day)) {
        removeDays.push(day);
    }
})
console.log(`next three days: ${keepNextThreeDays}`)
console.log(`removed days: ${removeDays}`)
// Assign elements to variables
// let daySelectorTabs = document.getElementById('day-btns');
let parentElement = document.getElementById('day-btns');
for (let index = parentElement.children.length; index > 0; index--) {
    // let printable = parentElement.children[index - 1].innerHTML
    if (removeDays.includes(parentElement.children[index - 1].innerHTML)) {
        parentElement.removeChild(parentElement.children[index - 1])
    }
}
console.log(parentElement.children)
let buttons = Array.from(parentElement.children);
// buttons.sort((a,b) => {
//     if (a.innerHTML === daysOfWeek[currentDay]) return -1;
//     if (b.innerHTML === daysOfWeek[currentDay]) return 1;
//     return a.innerHTML.localeCompare(b.innerHTML);
// });

while (parentElement.firstChild) {
    parentElement.removeChild(parentElement.firstChild);
}
buttons.forEach(button => console.log(button.textContent))
buttons.forEach(button => parentElement.appendChild(button));
