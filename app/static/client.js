var el = x => document.getElementById(x);
var imgData={"data":[100,8,10,12,100,100,14,16,14,100,100,18,18,14,100,0,80,0,80,0,13,15,80,18,0],"width":"5","height":"5"};
var wid=imgData["width"],hgh=imgData["height"],data=imgData["data"];

function showPicker() {
  el("file-input").click();
  
}

function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  var reader = new FileReader();
  reader.onload = function(e) {
    el("img1").src = e.target.result;
    el("img1").className = "";
  };
  reader.readAsDataURL(input.files[0]);
}

function analyze() {
  var uploadFiles = el("file-input").files;
  if (uploadFiles.length !== 1) alert("Please select a file to analyze!");

  el("analyze-button").innerHTML = "Analyzing...";
  var xhr = new XMLHttpRequest();
  var loc = window.location;
  xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`,
    true);
  xhr.onerror = function() {
    alert(xhr.responseText);
  };
  xhr.onload = function(e) {
    if (this.readyState === 4) {
      //alert('ttt');
      var response = JSON.parse(e.target.responseText);
      //var response = e.target.responseText;
      //alert(response);
      var array = response["result"];
      array1 = array.replace('[', '');
      var array1 = array1.replace('[', '');
      var array2 = array1.replace(']', '');
      array2 = array2.replace(']', '');
      var arr = array2.split(" ");
      el("result-label").innerHTML = `Result = ${response["result"]}`;
      el("img2").style.left = arr[1] + "px";
      el("img2").style.top = arr[0] + "px";
      alert('success!!!');
      //var array = response["result"];
      //array1 = array.replace('[', '');
      //var array1 = array1.replace('[', '');
      //var array2 = array1.replace(']', '');
      //array2 = array2.replace(']', '');
      //var arr = array2.split(" ");
      //alert('ttt3');
      //alert(array.length);
      //alert(array);
    }
    el("analyze-button").innerHTML = "Analyze";
  };

  var fileData = new FormData();
  fileData.append("file", uploadFiles[0]);
  xhr.send(fileData);
}

