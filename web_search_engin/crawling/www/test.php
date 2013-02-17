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

$sql = "SELECT * FROM  `status` WHERE  `id` =1";


$result = mysql_query($sql);
if (!$result) {
    echo 'Could not run query: ' . mysql_error();
    exit;
}
#$row = mysql_fetch_row($result);

echo "<table border='1'>
<tr>
<th>Last update time</th>
<th>crawled pages</th>
<th>keywords</th>
</tr>";

while($row = mysql_fetch_array($result))
  {
  echo "<tr>";
  echo "<td>" . $row[2] . "</td>";
  echo "<td>" . $row[1] . "</td>";
  echo "<td>" . $row[3] . "</td>";
  echo "</tr>";
  }
echo "</table>";





mysql_close();

?>