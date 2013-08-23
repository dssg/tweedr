<?php 

$username="YOUR_USERNAME";
$password="YOUR_PASSWORD";
$database="YOUR_DATABASE";
$link = mysql_connect('HOSTNAME',$username,$password);
session_start(); 
function browser() {
  $ua = strtolower($_SERVER['HTTP_USER_AGENT']);
  // you can add different browsers with the same way ..
  if(preg_match('/(chromium)[ \/]([\w.]+)/', $ua))
    $browser = 0;//'chromium';
  elseif(preg_match('/(chrome)[ \/]([\w.]+)/', $ua))
    $browser = 1;//'chrome';
  elseif(preg_match('/(safari)[ \/]([\w.]+)/', $ua))
    $browser = 2;//'safari';
  elseif(preg_match('/(opera)[ \/]([\w.]+)/', $ua))
    $browser = 3;//'opera';
  elseif(preg_match('/(msie)[ \/]([\w.]+)/', $ua))
    $browser = 4;//'msie';
  elseif(preg_match('/(mozilla)[ \/]([\w.]+)/', $ua))
    $browser = 5;//'mozilla';
  preg_match('/('.$browser.')[ \/]([\w]+)/', $ua, $version);
return $browser;
}

$thebrowser =browser();

if (!$link) {
  die('Could not connect: ' . mysql_error());
}
if(isset($_SESSION['pagenum'])){
  $_SESSION['pagenum']=$_SESSION['pagenum']+1;
 
}else{
  $_SESSION['pagenum']=0;
  $rando = rand(1,1000000);
  //   print $rando;                                                                                                                                                                                              
  $hash = hash(sha1, $rando);
  $_SESSION['hash'] = $hash; 
}
print "<html lang=\"en\">";
//print $_SESSION['hash'];

print  "<head>                                                                                                                                                                             
    <meta charset='utf-8'>                                                                                                                                                           
    <title>QCRI Twitter Information Extraction Page</title>                                                                                                                          
    <link rel='stylesheet' type='text/css' href='http://www.zetiz.com/sitepoint/css/bootstrap.css'>                                                                                  

<style>

#myarea {
border:2px solid #000;
padding:10px;
height:50px;
width:800px;
}
</style></head>";

print "<style type='text/css'>
  .ui-widget-header {
  background-image: none !important;
  background-color: #ABFFBB !important; //Any colour can go here
}
</style>";

print "<meta charset=\"utf-8\" />                                                                                                                                          
<link rel=\"stylesheet\" href=\"http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css\" />                                                                        
<script src=\"http://code.jquery.com/jquery-1.9.1.js\"></script>                                                                                                                   
<script src=\"http://code.jquery.com/ui/1.10.3/jquery-ui.js\"></script>                                                                                                             <link rel=\"stylesheet\" href=\"/resources/demos/style.css\" />                                                                                                                                                  
  <script>";
$car = $_SESSION['pagenum'];

print "
function badtweet() {                                                                                                                                                              
    document.forms[0].elements['bad'].value = 'NO ENTITIES, CLICK SUBMIT';                                                                            }   




$(function() {                                                                                                                                                                      $( \"#progressbar\" ).progressbar({                                                                                                                                                 max: 9 });
$( \"#progressbar\" ).progressbar({value:" . $car                                                                                                                                                                                                    
    . "});                                                                                                                                                                                                            
  });                                                                                                                                                                                                             

function getSelectionHtmlF(type) {                                                                                                                                                  var html = '';                                                                                                                                                                     
if (typeof window.getSelection != 'undefined') {                                                                                                                          
var sel = window.getSelection();                                                                                                                                            
var start = sel.anchorOffset;                                                                                                                                             
var end = sel.focusOffset;                                                                                                                                            
if (sel.rangeCount) {                                                                                                                                                        
var container = document.createElement('div');                                                                                                                             
for (var i = 0, len = sel.rangeCount; i < len; ++i) {                                                                                                                    
container.appendChild(sel.getRangeAt(i).cloneContents());                                                                                                                                  }       
html = container.innerHTML;                                                                                                                                                                                                                            
    }      
} else if (typeof document.selection != 'undefined') {                                                                                                                    
if (document.selection.type == 'Text') {                                                                                                                                    
html = document.selection.createRange().htmlText;                                                                                                                                     }                                                                                                                                                                                 }          
var t = document.getElementById(type).textContent;                                                                                                                      
if (t == ''){                                                                                                                                                              
document.getElementById(type).textContent += html;
var test = document.getElementById(type).textContent;
var name = 'i' + type;                                                                                                                                                             
document.forms[0].elements[name].value += html + ' ' + start + ' ' + end;                                                                                                           }else{                                                                                                                                                                              document.getElementById(type).textContent += ', ' + html;
var test = document.getElementById(type).textContent;
var name = 'i' + type;                                                                                                                                                              document.forms[0].elements[name].value += ',_,_, ' + html + ' ' + start + ' ' + end;                                                                                                                                                                         
                                                                                                                                                                                                                                                             
}                                                                                                                                                                                   window.getSelection().removeAllRanges();   
return false;
}           

function getSelectionHtml(type) {
  var html = '';

  if (typeof window.getSelection != 'undefined') {
    var sel = window.getSelection();

var start = sel.anchorOffset;
var end = sel.focusOffset;
    if (sel.rangeCount) {
      var container = document.createElement('div');
      for (var i = 0, len = sel.rangeCount; i < len; ++i) {
	container.appendChild(sel.getRangeAt(i).cloneContents());
 
      }
      html = container.innerHTML;
    }
  } else if (typeof document.selection != 'undefined') {
    if (document.selection.type == 'Text') {
      html = document.selection.createRange().htmlText;
    }
  }
var t = document.getElementById(type).innerText;
if (t == ''){
document.getElementById(type).innerText += html;
var test = document.getElementById(type).innerText;
var name = 'i' + type;
document.forms[0].elements[name].value += html + ' ' + start + ' ' + end;
}else{
document.getElementById(type).innerText += ', ' + html;
var test = document.getElementById(type).innerText;
var name = 'i' + type;
document.forms[0].elements[name].value += ',_,_, ' + html + ' ' + start + ' ' + end;

}

window.getSelection().empty();  
return false;
}

function undo(type) {
var name = 'i' + type;
var text = document.forms[0].elements[name].value; 
//var text = document.getElementById(type).innerText;
if (text.indexOf(',_,_,') != -1){
document.getElementById(type).innerText = '';
document.forms[0].elements[name].value = '';
var arr=text.split(',');
var size = arr.length-1;
arr.splice(size, 1); 
for (var i=0;i<arr.length-1;i++)
{ 
document.forms[0].elements[name].value += arr[i] + ',_,_, ';
document.getElementById(type).innerText += arr[i] + ', ';
}
document.getElementById(type).innerText += arr[arr.length-1];
document.forms[0].elements[name].value += arr[arr.length-1];
}
else{
document.getElementById(type).innerText = '';
var name = 'i' + type;
document.forms[0].elements[name].value = '';
}
}

function undoF(type) {                                                                                                                                                                                                                                        
var name = 'i' + type;                                                                                                                                                                                                                                       
var text = document.forms[0].elements[name].value;                                                                                                                                                                                                           
//var text = document.getElementById(type).textContent;                                                                                                                                                                                                        
if (text.indexOf(',_,_,') != -1){                                                                                                                                                                                                                            
document.getElementById(type).textContent = '';                                                                                                                                                                                                                
document.forms[0].elements[name].value = '';                                                                                                                                                                                                                 
var arr=text.split(',');                                                                                                                                                                                                                                     
var size = arr.length-1;                                                                                                                                                                                                                                     
arr.splice(size, 1);                                                                                                                                                                                                                                         
for (var i=0;i<arr.length-1;i++)                                                                                                                                                                                                                             
{                                                                                                                                                                                                                                                            
document.forms[0].elements[name].value += arr[i] + ',_,_, ';                                                                                                                                                                                                 
document.getElementById(type).textContent += arr[i] + ', ';                                                                                                                                                                                                    
}                                                                                                                                                                                                                                                            
document.getElementById(type).textContent += arr[arr.length-1];                                                                                                                                                                                                
document.forms[0].elements[name].value += arr[arr.length-1];                                                                                                                                                                                                 
}                                                                                                                                                                                                                                                            
else{                                                                                                                                                                                                                                                        
document.getElementById(type).textContent = '';                                                                                                                                                                                                                
var name = 'i' + type;                                                                                                                                                                                                                                       
document.forms[0].elements[name].value = '';                                                                                                                                                                                                                 
}                                      
}

</script></head>";


@mysql_select_db($database) or die( "Unable to select database");
if ($_SESSION['pagenum'] < 10){
  //  print $_SESSION['pagenum'];

//$random = rand(0,1);  

//if ($random == 1){
  $result = mysql_query("SELECT * FROM DamageClassification WHERE is_extracted < 1 ORDER BY RAND() LIMIT 1");
//}else{

  //$result = mysql_query("SELECT * FROM uniform_sample WHERE is_extracted < 1 LIMIT 1");

//}



$tweet ="";
$array = array();
$id = 0;

      $row = mysql_fetch_array($result);


  //$tweet = $row['Tweet'];
  $tweet = ""; 
 $sample_type = $row["which_sample"];
  $id = $row['DSSG_ID'];
  //print $id;
  $id2 = $row['id'];
  //print "hehehe";
  //print $sample_type;
  if (is_null($sample_type)){
      $tweet = $row["Tweet"];

    }else{  
if (strcmp($sample_type, "keyword") == 0 || strcmp($sample_type, "by_keyword")==0){
    $r = mysql_query("SELECT * FROM keyword_sample WHERE dssg_id = '$id' LIMIT 1");
    $row2 = mysql_fetch_array($r);
    $tweet = $row2["text"];

  }else if (strcmp($sample_type,"uniform")==0){
      $r = mysql_query("SELECT * FROM uniform_sample WHERE dssg_id = '$id' LIMIT 1");
      $row2 = mysql_fetch_array($r);
      $tweet = $row2["text"];

    }
  
}
//$random = rand(0,9);
$id_num = $id; //$array[0];




$delimiter = ',';

$arr = explode(" ", $tweet);

print "<body>";
   print "<div class='navbar navbar-fixed-top'>
  <div class='navbar-inner'>
    <div class='container'>
      <a class='btn btn-navbar' data-toggle='collapse' data-target='.nav-collapse'>
        <span class='icon-bar'></span>
        <span class='icon-bar'></span>
        <span class='icon-bar'></span>
      </a>
<br>
      <a class='brand' href='#'>QCRI Disaster Information Extraction Tool</a>
      <div class='nav-collapse'>

      <div id= 'progressbar'>
        <div class='bar' style='width: 16%;'></div>
      </div>
      </div><!--/.nav-collapse -->
    </div>
  </div>
</div>";



#print "<body><div id=\"progressbar\"></div>";
print "<div class='container'><form id='formid' method=\"post\" action=\"db.php?tweet_id=" . $id_num . "&random=" . $random . "&id=" . $id2 . "\">";
#print "<div id='p'></div>";
print "<TABLE WIDTH=82% HEIGHT=100% bgcolor='#FFFFFF' BORDER=0 align='center' cellpadding='15'>";

$tasks_completed = $_SESSION[pagenum];
print "<TR><TD>Number of tasks completed: " . $tasks_completed . "/10";

print "<div style='height:15px;' id=\"progressbar\"></div></TD></TR>";


print "<TR><TD><b>Select the entity in the following tweet by dragging your mouse on text box from the beginning of the word selected to the end of the word. Select the appropriate category and then the Submit button below. </b></TD></TR></div>";

print "<TR><TD><center><div id='myarea' contenteditable='false'>" . $tweet . "</div></center> <button class = 'btn btn-danger btn-mini' onclick='badtweet();'>Bad Tweet - No Entities</button><font color = 'red'><input size = \"180\" name=\"bad\" style=\"border: none; color:#FF0000\"/></input><br><br>";




if ($thebrowser == 5){
print "<font size='2' color= 'black'>Transportation: </font>";
print "<button class='btn btn-info btn-mini' onclick='getSelectionHtmlF(0);'>Bridge</button>";
print "<button class='btn btn-info btn-mini' onclick='getSelectionHtmlF(1);'>Road</button>";
print "<button class='btn btn-info btn-mini' onclick='getSelectionHtmlF(2);'>Intersection</button>";
print "<button class='btn btn-info btn-mini' onclick='getSelectionHtmlF(3);'>Highway</button>";
print "<button class='btn btn-info btn-mini' onclick='getSelectionHtmlF(4);'>Private Vehicle</button>";
print "<button class='btn btn-info btn-mini' onclick='getSelectionHtmlF(5);'>Train</button>";
print "<button class='btn btn-info btn-mini' onclick='getSelectionHtmlF(6);'>Bus</button>";
print "<button class='btn btn-info btn-mini' onclick='getSelectionHtmlF(7);'>Airplane</button>";
print "<button class='btn btn-info btn-mini' onclick='getSelectionHtmlF(24);'>Other Transportation</button><br>";
print "<br/><br/><br><font size='2' color = 'black'>Infrastructures: </font>";
print "<button class='btn btn-success btn-mini' onclick='getSelectionHtmlF(8);'>Hospital/Health</button>";
print "<button class='btn btn-success btn-mini' onclick='getSelectionHtmlF(9);'>Evacuation Center</button>";
print "<button class='btn btn-success btn-mini' onclick='getSelectionHtmlF(10);'>School</button>";
print "<button class='btn btn-success btn-mini' onclick='getSelectionHtmlF(11);'>Fire/Police Departments</button>";
print "<button class='btn btn-success btn-mini' onclick='getSelectionHtmlF(12);'>Homes/Residential</button>";
print "<button class='btn btn-success btn-mini' onclick='getSelectionHtmlF(21);'>Religious Institution</button>";
print "<button class='btn btn-success btn-mini' onclick='getSelectionHtmlF(23);'>Other Building</button><br>";
print "<br><font size='2' color= 'black'>Damage Type: </font>";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(13);'>Fire</button>";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(14);'>Flood</button>";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(26);'>Snow</button>&nbsp";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(25);'>Electricity Loss</button>&nbsp";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(15);'>Wind Damage</button>";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(16);'>Building Collapse</button>";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(17);'>Vehicular Impact</button>";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(18);'>Casualties</button>";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(19);'>Injured Persons</button>";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(20);'>Missing Persons</button>";
print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtmlF(22);'>Other Damage</button>";

print "<script>$('button').on('click', function(ev) { ev.preventDefault();})</script>";
}else{

  print "<font size='2' color= 'black'>Transportation: </font>";
  print "<button class='btn btn-info btn-mini' onclick='getSelectionHtml(0);'>Bridge</button>&nbsp";
  print "<button class='btn btn-info btn-mini' onclick='getSelectionHtml(1);'>Road</button>&nbsp";
  print "<button class='btn btn-info btn-mini' onclick='getSelectionHtml(2);'>Intersection</button>&nbsp";
  print "<button class='btn btn-info btn-mini' onclick='getSelectionHtml(3);'>Highway</button>&nbsp";
  print "<button class='btn btn-info btn-mini' onclick='getSelectionHtml(4);'>Private Vehicle</button>&nbsp";
  print "<button class='btn btn-info btn-mini' onclick='getSelectionHtml(5);'>Train</button>&nbsp";
  print "<button class='btn btn-info btn-mini' onclick='getSelectionHtml(6);'>Bus</button>&nbsp";
  print "<button class='btn btn-info btn-mini' onclick='getSelectionHtml(7);'>Airplane</button>&nbsp";
  print "<button class='btn btn-info btn-mini' onclick='getSelectionHtml(24);'>Other Transportation</button><br>";
  print "<br><font size='2' color = 'black'>Infrastructures: </font>";
  print "<button class='btn btn-success btn-mini' onclick='getSelectionHtml(8);'>Hospital/Health</button>&nbsp";
  print "<button class='btn btn-success btn-mini' onclick='getSelectionHtml(9);'>Evacuation Center</button>&nbsp";
  print "<button class='btn btn-success btn-mini' onclick='getSelectionHtml(10);'>School</button>&nbsp";
  print "<button class='btn btn-success btn-mini' onclick='getSelectionHtml(11);'>Fire/Police Departments</button>&nbsp";
  print "<button class='btn btn-success btn-mini' onclick='getSelectionHtml(12);'>Homes/Residential</button>&nbsp";
  print "<button class='btn btn-success btn-mini' onclick='getSelectionHtml(21);'>Religious Institution</button>&nbsp";
  print "<button class='btn btn-success btn-mini' onclick='getSelectionHtml(23);'>Other Building</button><br>";
  print "<br><font size='2' color= 'black'>Damage Type: </font>";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(13);'>Fire</button>&nbsp";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(14);'>Flood</button>&nbsp";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(26);'>Snow</button>&nbsp";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(25);'>Electricity Loss</button>&nbsp";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(15);'>Wind Damage</button>&nbsp";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(16);'>Building Collapse</button>&nbsp";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(17);'>Vehicular Impact</button>&nbsp";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(18);'>Casualties</button>&nbsp";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(19);'>Injured Persons</button>&nbsp";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(20);'>Missing Persons</button>&nbsp";
  print "<button class='btn btn-warning btn-mini' onclick='getSelectionHtml(22);'>Other Damage</button>&nbsp";
  print "<script>$('button').on('click', function(ev) { ev.preventDefault();})</script>";

}

print "<input type=\"hidden\" name=\"i0\" /></input>";
print "<input type=\"hidden\" name=\"i1\" /></input>";
print "<input type=\"hidden\" name=\"i2\" /></input>";
print "<input type=\"hidden\" name=\"i3\" /></input>";
print "<input type=\"hidden\" name=\"i4\" /></input>";
print "<input type=\"hidden\" name=\"i5\" /></input>";
print "<input type=\"hidden\" name=\"i6\" /></input>";
print "<input type=\"hidden\" name=\"i7\" /></input>";
print "<input type=\"hidden\" name=\"i8\" /></input>";
print "<input type=\"hidden\" name=\"i9\" /></input>";
print "<input type=\"hidden\" name=\"i10\" /></input>";
print "<input type=\"hidden\" name=\"i11\" /></input>";
print "<input type=\"hidden\" name=\"i12\" /></input>";
print "<input type=\"hidden\" name=\"i13\" /></input>";
print "<input type=\"hidden\" name=\"i14\" /></input>";
print "<input type=\"hidden\" name=\"i15\" /></input>";
print "<input type=\"hidden\" name=\"i16\" /></input>";
print "<input type=\"hidden\" name=\"i17\" /></input>";
print "<input type=\"hidden\" name=\"i18\" /></input>";
print "<input type=\"hidden\" name=\"i19\" /></input>";
print "<input type=\"hidden\" name=\"i20\" /></input>";
print "<input type=\"hidden\" name=\"i21\" /></input>";
print "<input type=\"hidden\" name=\"i22\" /></input>";
print "<input type=\"hidden\" name=\"i23\" /></input>";
print "<input type=\"hidden\" name=\"i24\" /></input>";
print "<input type=\"hidden\" name=\"i25\" /></input>";
print "<input type=\"hidden\" name=\"i26\" /></input>";
print "<br><br><center><TABLE cellpadding= '2'>";

//print "<div class='row'><div class='span8'>";
if ($browser == 5){
print "<TR><TD><b>Bridges:</b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(0);'>Undo</button><div id='0' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD>";
print "<b>Roads: </b><button align= 'right' class='btn btn-danger btn-mini' onclick='undoF(1);'>Undo</button><div id='1' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR><TD>";
print "<b>Intersections: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(2);'>Undo</button><div id='2' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD>";
print "<b>Highways: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(3);'>Undo</button><div id='3' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR><TD>";
print "<b>Private Vehicles: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(4);'>Undo</button><div id='4' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD>";
print "<b>Trains: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(5);'>Undo</button><div id='5' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR><TD>";
print "<b>Buses: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(6);'>Undo</button><div id='6' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD>";
print "<b>Airplanes: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(7);'>Undo</button><div id='7' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR><TD>";
print "<b>Other Transportation: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(24);'>Undo</button><div id='24' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD>";
print "<b>Hospital/Health Services: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(8);'>Undo</button><div id='8' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD></TR
><TR><TD>";
print "<b>Evacuation Centers: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(9);'>Undo</button><div id='9' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>School: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(10);'>Undo</button><div id='10' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR>";
print "<TD><b>Fire/Police Department: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(11);'>Undo</button><div id='11' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>Homes/Residential: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(12);'>Undo</button><div id='12' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TR><TR>";
print "<TD><b>Religious Institutions: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(21);'>Undo</button><div id='21' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script>";
print "</TD><TD><b>Other Building: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(23);'>Undo</button><div id='23' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.p\
reventDefault();})</script></TD>";
print "</TR><TR><TD><b>Fire: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(13);'>Undo</button><div id='13' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>Flood: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(14);'>Undo</button><div id='14' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR>";
print "<TD><b>Wind/Projectile Damage: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(15);'>Undo</button><div id='15' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>Building Collapse: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(16);'>Undo</button><div id='16' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR>";
print "<TR><TD><b>Vehicular Impact: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(17);'>Undo</button><div id='17' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>Death/Casualties: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(18);'>Undo</button><div id='18' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TR><TD><b>Injured Persons: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(19);'>Undo</button><div id='19' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>Missing Persons: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(20);'>Undo</button><div id='20' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR>";
print "<TD><b>Other Damage: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(22);'>Undo</button><div id='22' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><br><br></center>";
print "<TD><b>Electricity Loss: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(25);'>Undo</button><div id='25' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR>";
print "<TD><b>Snow: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undoF(26);'>Undo</button><div id='26' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR></TABLE><br><br></center>"; 

}else{
  print "<TR><TD><b>Bridges:</b><div id='0' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(0);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD>";    
  print "<b>Roads: </b><div id='1' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(1);'>Undo</button></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR><TD>";
  print "<b>Intersections: </b><div id='2' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(2);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD>";
  print "<b>Highways: </b><div id='3' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(3);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR><TD>";
  print "<b>Private Vehicles: </b><div id='4' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(4);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD>";
  print "<b>Trains: </b><div id='5' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(5);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR><TD>";
  print "<b>Buses: </b><div id='6' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(6);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD>";
  print "<b>Airplanes: </b><div id='7' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(7);'>Undo</button></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR><TD>";
  print "<b>Other Transportation: </b><div id='24' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(24);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD>";
print "<b>Hospital/Health Services: </b><div id='8' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(8);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><TD></TR><TR><TD>";
print "<b>Evacuation Centers: </b><div id='9' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(9);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>School: </b><div id='10' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(10);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR>";
print "<TD><b>Fire/Police Department: </b><div id='11' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(11);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>Homes/Residential: </b><div id='12' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(12);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TR><TR>";
print "<TD><b>Religious Institutions: </b><div id='21' style='color:#FF0000'></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(21);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script>";
print "</TD><TD><b>Other Building: </b><div id='23' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(23);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "</TR><TR><TD><b>Fire: </b><div id='13' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(13);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>Flood: </b><div id='14' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(14);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR>";
print "<TD><b>Wind/Projectile Damage: </b><div id='15' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(15);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>Building Collapse: </b><div id='16' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(16);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR>";
print "<TR><TD><b>Vehicular Impact: </b><div id='17' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(17);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TD><b>Death/Casualties: </b><div id='18' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(18);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";
print "<TR><TD><b>Injured Persons: </b><div id='19' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(19);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD>";

print "<TD><b>Missing Persons: </b><div id='20' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(20);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR>";
print "<TD><b>Other Damage: </b><div id='22' style='color:#FF0000'></div></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(22);'>Undo</button><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD><br><br></center>";
print "<TD><b>Electricity Loss: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(25);'>Undo</button><div id='25' style='color:#FF0000'></div><script>$('button').on('click', function(ev) { ev.preventDefault();})</script></TD></TR><TR>";
print "<TD><b>Snow: </b></TD><TD><button class='btn btn-danger btn-mini' onclick='undo(26);'>Undo</button><div id='26' style='color:#FF0000'></div><script>$('button').on('click',function(ev) { ev.preventDefault();})</script></TD></TR></TABLE><br><br></center>";




}
//print "</div></div>";

print "<center><input class='btn btn-primary btn-large' type='submit' value='Submit'></input></form>"; 
print "</center>
</TD> </TR></table>


  <div class='row'>   
<div class='footer'>";                                                       

print "<font size='3' color= 'black'><b>Examples: </b></font><br><font size='2' color='black'>@weatherchannel: Sad news to report.<FONT                                              
style='BACKGROUND-COLOR: yellow'>3</FONT> more people passed away recently due to injuries sustained during the #JoplinTornado. Total fa ...                                         
  <br> <b>3: death/casualties</b><br>                                                                                                                                                  
  Stunning  @BlairMiller9 CNN reports: X-rays from <font style='background-color: yellow'>St. John's Hospital</font> found 70 miles from #Joplin<br><b>                                
St. John's Hospital: Hospital/Health Services</b><br>                                                                                                                                
  @stormchaser4850: Edmond, OK woman dies in <font style='background-color: yellow'>car accident</font> while driving to beat tornado http://bit.ly/kWzV3x                             
  <br><b>car accident: Vehicular Impact</b>                                                                                                                                            
</font><br><br>";                                            
  print "<p>&copy; Data Science for Social Good 2013. Interface created by Zahra Ashktorab</p>                                                                                                   
                                                                </div>                                                                                                               
                                                              </div>                                                                                                                 </div>
                                                                      

</body></html>";

}else{

  print "<html>";
   print  "<body>";
   //   $rando = rand(1,1000000);
   //   print $rando;
   // $hash = hash(sha1, $rando);

print "<TABLE WIDTH=82% HEIGHT=50% bgcolor='#FFFFFF' BORDER=0 align='center'>                                                                                                                    
<TR><TD><center><b>Copy and paste the code below into the Mechanical Turk:</b></center></TD></TR>                                                                                                                                                                                                                   
<TR><TD><center>"  . $_SESSION['hash'] . "</center></TD></TR></TABLE>";
  
   print "</body></html>";
   unset($_SESSION['hash']);
   unset($_SESSION['pagenum']);
 }
print "<script scr='http://qcri.dssg.io/bootstrap/session2/dist/js/bootstrap.js'></script>"; 


?>