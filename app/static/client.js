var el = x => document.getElementById(x);
var imgData={"data":[100,8,10,12,100,100,14,16,14,100,100,18,18,14,100,0,80,0,80,0,13,15,80,18,0],"width":"5","height":"5"};
var wid=imgData["width"],hgh=imgData["height"],data=imgData["data"];

function draw(){
  var index=-1;
  var img=document.getElementById("img");
  img.innerHTML="";
  for(var i=0;i<hgh;i++)
  {
    for(var j=0;j<wid;j++)
    {
      index++;
      var pix=data[index];
      img.innerHTML+="<span class='pixel' style='background:rgb("+pix+","+pix+","+pix+");position:absolute;top:"+(i*5)+"px;left:"+(j*5)+"px;'></span>";
    }
  }
}

function showPicker() {
  el("file-input").click();
  
}

function showPicked(input) {
  el("upload-label").innerHTML = input.files[0].name;
  var reader = new FileReader();
  reader.onload = function(e) {
    el("image-picked").src = e.target.result;
    el("image-picked").className = "";
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
      var response = JSON.parse(e.target.responseText);
      draw();
      el("result-label").innerHTML = `Result = ${response["result"]}`;
      var array = response["result"];
      var array1 = array.replace('[', '');
      var array2 = array1.replace(']', '');
      var arr = array2.split(" ");
      try {
        var number = parseInt(arr[0]);
        alert(number) ;
      } catch(e) {
        alert('error 1');
      }
      try {
        var number = parseInt(arr[10]);
        alert(number) ;
      } catch(e) {
        alert('error 2');
      }
    }
    el("analyze-button").innerHTML = "Analyze";
  };

  var fileData = new FormData();
  fileData.append("file", uploadFiles[0]);
  xhr.send(fileData);
}

