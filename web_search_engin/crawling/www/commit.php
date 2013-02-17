<?php

$host = "localhost"; 
$user = "web_search"; 
$pass = "dengxu_wangqi"; 
$db   = "web_search_engine";


$conn = mysql_connect($host, $user, $pass);

if (!$conn)
{
    echo "Could not connect to server\n";
    exit();
} 

mysql_select_db($db,$conn);

$sql = "UPDATE `configuation` SET `seed_keywords`= '".$_GET["key_words"]."',`downloader_thread` ='".$_GET["down_thread"].
"',`parser_thread` ='".$_GET["parse_thread"]."',`seed_resultnum` ='".$_GET["result_count"]."', `is_start` = 1, 
`key_word_start`=0,`status_start` = 0 WHERE id = 1";


$result = mysql_query($sql);


if (!$result) 
{
    echo 'Could not run query: ' . mysql_error();
    exit;
}
header("Location: ./realtime.html")
?>