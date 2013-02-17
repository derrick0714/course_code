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

$sql = "SELECT * FROM  `configuation` WHERE  `id` =1";

$result = mysql_query($sql);
if (!$result) 
{
    echo 'Could not run query: ' . mysql_error();
    exit;
}

$row = mysql_fetch_array($result);

if($row ['key_word_start'] != '1'  && $row ['status'] != '1')
{

?>
<div class="my_content2">
<h1>Loading Data</h1>

<div class="progress progress-striped active">
  <div class="bar" style="width: 40%;"></div>
</div>
</div>
<?
exit(1);
}


$sql = "SELECT * FROM  `status` WHERE  `id` =1";


$result = mysql_query($sql);
if (!$result) 
{
    echo 'Could not run query: ' . mysql_error();
    exit;
}

$row = mysql_fetch_array($result);

//var_dump($row)

?>

<div id="breadcrumb">
    <ul>
        
<li>Realtime Statistics : [<? echo number_format($row[crawled_time], 1, '.', ',')  ?>s]</li>

    </ul>
    </div>
	<div class="my_span"></div>
	<div class="my_content">
		<table class="table table-bordered">
		  <thead>
		    <tr>
		      <th olspan="2"><b>Downloader:</b></th>
		    </tr>
		  </thead>
		  <tbody>
		    <tr>
		      <td width="200"><b>crawled pages:</b></td>
		      <td> <?=$row['crawled_url_count']?></td>
		    </tr>
		    <tr>
		      <td>crawled total size:</td>
		      <td>
		      <?
		      $num = $row[crawled_size]*1.0/1024/1024;
		      echo number_format($num, 1, '.', ',')
		      ?> MB</td>
		    </tr>
		    <tr>
		      <td width="200"><b>crawled queue:</b></td>
		      <td> <?=$row['crawled_queue']?></td>
		    </tr>
		  </tbody>
		</table>	
	</div>
	<div class="my_content">
		<table class="table table-bordered">
		  <thead>
		    <tr>
		      <th olspan="2"><b>Parser:</b></th>
		    </tr>
		  </thead>
		  <tbody>
		    <tr>
		      <td width="200"><b>parsed pages:</b></td>
		      <td> <?=$row['parse_count']?></td>
		    </tr>
		    <tr>
		      <td>praser queue:</td>
		      <td> <?=$row['parse_queue']?></td>
		    </tr>
		    <tr>
		      <td width="200"><b>scheme type:</b></td>
		      <td> <?=$row['parse_scheme_type']?></td>
		    </tr>
		     <tr>
		      <td width="200"><b>cgi</b></td>
		      <td> <?=$row['parse_cgi']?></td>
		    </tr>
		     <tr>
		      <td width="200"><b>visited:</b></td>
		      <td> <?=$row['parse_visited']?></td>
		    </tr>
		     <tr>
		      <td width="200"><b>robot</b></td>
		      <td> <?=$row['parse_robot']?></td>
		    </tr>
		     <tr>
		      <td width="200"><b>nest level</b></td>
		      <td> <?=$row['parse_nestlv']?></td>
		    </tr>
		  </tbody>
		</table>	
	</div>

	<div class="my_content">
		<table class="table table-bordered AutoNewline">
		  <thead>
		    <tr>
		      <th width="500">recent download url</th>
		      <th>code</th>
		      <th>size</th>
		      <th>parent</th>
		      <th>depth</th>
		    </tr>
		  </thead>
		  <tbody>
		    <tr>
		  	<?php 
		    	$sql = "SELECT * FROM `log` order by `id` desc LIMIT 0 , 10";
				$result = mysql_query($sql);
		    	$i=1;
		    	while ($array = mysql_fetch_array($result))
				{
					echo  "<tr>";
					echo  "<td width='500'>".$array['url'].substr(1,20)."</td>";
					echo  "<td>".$array['code']."</td>";
					echo  "<td>".$array['data_size']."</td>";
					echo  "<td>".$array['parent']."</td>";
					echo  "<td>".$array['depth']."</td>";
					echo  "</tr>";
				}
		    ?>

		    </tr>
		</table>	
	</div>


 </div>



<?php

mysql_close();

?>
