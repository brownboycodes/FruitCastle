var node = document.getElementById("output");

var converter = new showdown.Converter();

// fetch("/paypal-concept-data/v1/docs")
fetch(`${window.location.href}/v1/docs`)
  .then((response) => response.text())
  .then((text) => {
    var sampleHtml = converter.makeHtml(text);
    // console.log(sampleHtml);
    node.innerHTML = sampleHtml;
    hljs.highlightAll();
    beautifyCode();
  });
// console.log(window.location.href);
// console.log(current_data);

/* globals Chart:false, feather:false */
function beautifyCode() {
  //! needs work
  let allCodeBlocks = Array.from(document.querySelectorAll("pre"));
  console.log(allCodeBlocks);

  for (const block of allCodeBlocks) {
    let nodeAbove=block.nextSibling;
    console.log(nodeAbove);
    let wrapperDiv = document.createElement("div");
    // wrapperDiv.style.margin = "10px";
    // wrapperDiv.style.visibility = "visible";
    wrapperDiv.classList.add("code-wrapper");
    let fakeMenu = document.createElement("div");
    fakeMenu.classList.add("fakeMenu");
    fakeMenu.style.visibility = "visible";
    let fakeClose = document.createElement("div");
    fakeClose.classList.add("fakeButtons", "fakeClose");
    fakeClose.style.visibility = "visible";
    let fakeMinimize = document.createElement("div");
    fakeMinimize.classList.add("fakeButtons", "fakeMinimize");
    fakeMinimize.style.visibility = "visible";
    let fakeZoom = document.createElement("div");
    fakeZoom.classList.add("fakeButtons", "fakeZoom");
    fakeZoom.style.visibility = "visible";
    let fakeScreen = document.createElement("div");
    fakeScreen.classList.add("fakeScreen");
    fakeScreen.style.visibility = "visible";
    fakeMenu.appendChild(fakeClose);
    fakeMenu.appendChild(fakeMinimize);
    fakeMenu.appendChild(fakeZoom);
    wrapperDiv.appendChild(fakeMenu);
    fakeScreen.appendChild(block);
    // document.body.appendChild(fakeScreen);
    wrapperDiv.appendChild(fakeScreen);
    // nodeAbove.appendChild(wrapperDiv);
    node.insertBefore(wrapperDiv,nodeAbove);
    // console.log(block);
  }
  //!  needs work
}

(function () {
  "use strict";

  feather.replace({ "aria-hidden": "true" });
  /*
  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
  */
})();
