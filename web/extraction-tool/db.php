<?php 
 header("Location:index.php");

$username="dssg";
$password="dssg2013";
$database="QCRI";
$link = mysql_connect('qcri.c5faqozfo86k.us-west-2.rds.amazonaws.com',$username,$password);
session_start();
if (!$link) {
  die('Could not connect: ' . mysql_error());
 }
//echo 'Connected successfully';


@mysql_select_db($database) or die( "Unable to select database");

print "<style>body {background-image:url('background.png');
  background-repeat:yes;
font-family: fontC;
 color:#111;
}



</style>";
$hash = $_SESSION['hash'];
$id_num = $_GET['tweet_id'];
$id2 = $_GET['id'];

$random = $_GET['random'];
print $tweet_id;
$sample = "";

$result = mysql_query("SELECT * FROM DamageClassification WHERE id='$id2'");



$tweet = "";
if($result === FALSE) {
    die(mysql_error()); // TODO: better error handling
}

$row = mysql_fetch_array($result);
//$tweet = $row['Tweet'];
$id = $row['DSSG_ID'];
$sample= $row['type_sample'];

if (is_null($sample)){
  $tweet = $row["Tweet"];

}else{
  if (strcmp($sample, "keyword") == 0 || strcmp($sample, "by_keyword")==0){
    $r = mysql_query("SELECT * FROM keyword_sample WHERE dssg_id = '$id' LIMIT 1");
    $row2 = mysql_fetch_array($r);
    $tweet = $row2["text"];

  }else if (strcmp($sample,"uniform")==0){
    $r = mysql_query("SELECT * FROM uniform_sample WHERE dssg_id = '$id' LIMIT 1");
    $row2 = mysql_fetch_array($r);
    $tweet = $row2["text"];

  }

}



//Pass the data in the form of url page.php?variable=value and read the values as `echo $_GET['variable']
print $tweet . "<br>";
 $tweet =  mysql_real_escape_string($tweet);


for ($i = 0; $i < 27; $i++){
$post_name = "i" . $i;
print $post_name;

$h = $_POST[$post_name];
print "bridge:";
if($h != "") {
    $t = explode(",_,_,", $h);
foreach ($t as $token) {
    print $token. ", ";
     $token =  mysql_real_escape_string($token);
$e = explode(" ", $token);
$token_start = $e[count($e)-2];
$token_end = $e[count($e)-1];
$gr = " " . $token_start . " " . $token_end;

$ra = str_replace($gr,"",$token);
print "start:" . $token_start . "<br>";
print "end:" . $token_end . "<br>";

$request= "INSERT INTO tokenized_labels values (NULL, '$id', '$tweet','$token_start', '$token_end', '$post_name', '$ra', '$hash', '$sample')";
 $results = mysql_query($request, $link);

  echo mysql_errno($link) . ": " . mysql_error($link) . "\n";



 }
 }





}
$bad_tweet = $_POST['bad'];

if (strpos($bad_tweet, "NO ENTITIES, CLICK SUBMI") !== false){

  $request = "UPDATE DamageClassification SET Infrastructure=0 WHERE id='$id2'";
  $results = mysql_query($request, $link);

  echo mysql_errno($link) . ": " . mysql_error($link) . "\n";


  $request = "UPDATE DamageClassification SET Casualty=0 WHERE id='$id2'";
  $results = mysql_query($request, $link);

  echo mysql_errno($link) . ": " . mysql_error($link) . "\n";



}




$request = "UPDATE DamageClassification SET is_extracted=is_extracted+1 WHERE id='$id2'";
$results = mysql_query($request, $link);

echo mysql_errno($link) . ": " . mysql_error($link) . "\n";



?>